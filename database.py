"""
Database layer for Smart 4D System
Adds SQLite support while keeping CSV as backup
"""
import sqlite3
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='lottery_data.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lottery_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                provider TEXT NOT NULL,
                draw_info TEXT,
                number_1st TEXT,
                number_2nd TEXT,
                number_3rd TEXT,
                special TEXT,
                consolation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, provider, number_1st)
            )
        ''')
        
        # Predictions cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prediction_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT UNIQUE,
                predictions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        # User predictions tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_date TIMESTAMP,
                draw_date TEXT,
                provider TEXT,
                predicted_numbers TEXT,
                actual_numbers TEXT,
                hit_status TEXT DEFAULT 'pending',
                confidence REAL,
                method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def import_from_csv(self, csv_path='4d_results_history.csv'):
        """Import CSV data into database"""
        try:
            df = pd.read_csv(csv_path, on_bad_lines='skip')
            conn = sqlite3.connect(self.db_path)
            
            # Import only if table is empty
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM lottery_results")
            count = cursor.fetchone()[0]
            
            if count == 0:
                df.to_sql('lottery_results', conn, if_exists='append', index=False)
                logger.info(f"Imported {len(df)} rows from CSV")
            
            conn.close()
            return True
        except Exception as e:
            logger.error(f"CSV import error: {e}")
            return False
    
    def get_results(self, provider=None, start_date=None, end_date=None, limit=1000):
        """Get lottery results with filters"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM lottery_results WHERE 1=1"
        params = []
        
        if provider and provider != 'all':
            query += " AND provider = ?"
            params.append(provider)
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += f" ORDER BY date DESC LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def cache_prediction(self, cache_key, predictions, ttl_minutes=60):
        """Cache prediction results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expires_at = datetime.now().timestamp() + (ttl_minutes * 60)
        
        cursor.execute('''
            INSERT OR REPLACE INTO prediction_cache (cache_key, predictions, expires_at)
            VALUES (?, ?, ?)
        ''', (cache_key, str(predictions), expires_at))
        
        conn.commit()
        conn.close()
    
    def get_cached_prediction(self, cache_key):
        """Get cached prediction if not expired"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT predictions FROM prediction_cache 
            WHERE cache_key = ? AND expires_at > ?
        ''', (cache_key, datetime.now().timestamp()))
        
        result = cursor.fetchone()
        conn.close()
        
        return eval(result[0]) if result else None
