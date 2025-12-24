"""Enhanced CSV Cleaner - Uses logic from all working providers"""
import csv
import pandas as pd
from utils.universal_4d_extractor import clean_row, is_valid_4d

def clean_csv_file(input_file='4d_results_history.csv', output_file='clean_4d_training_data.csv'):
    """Clean CSV using universal extraction logic"""
    results = []
    errors = 0
    
    print(f"🔄 Processing {input_file}...")
    
    try:
        with open(input_file, encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                try:
                    cleaned = clean_row(row)
                    if cleaned:
                        results.append(cleaned)
                    else:
                        errors += 1
                except Exception as e:
                    errors += 1
                    continue
                
                if idx % 1000 == 0:
                    print(f"  Processed {idx} rows... ({len(results)} valid)")
    
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    if not results:
        print("❌ No valid data extracted!")
        return False
    
    # Create DataFrame and clean
    df = pd.DataFrame(results)
    
    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['date', 'provider', '1st', '2nd', '3rd'])
    after = len(df)
    
    # Sort by date
    df = df.sort_values('date', ascending=False)
    
    # Save
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ SUCCESS!")
    print(f"📊 Total rows processed: {idx}")
    print(f"✅ Valid 4D rows: {after}")
    print(f"🗑️  Duplicates removed: {before - after}")
    print(f"❌ Invalid rows: {errors}")
    print(f"📁 Saved to: {output_file}")
    print(f"\n📈 Providers: {df['provider'].nunique()}")
    print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
    
    return True

if __name__ == "__main__":
    clean_csv_file()
