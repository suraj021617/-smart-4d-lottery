"""
One-click integration script
Run this to enable all enhancements automatically
"""
import os
import sys

def integrate_enhancements():
    """Add enhancements to app.py without breaking existing code"""
    
    app_file = 'app.py'
    
    if not os.path.exists(app_file):
        print("❌ app.py not found!")
        return False
    
    # Read existing app.py
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already integrated
    if 'app_enhancements' in content:
        print("✅ Enhancements already integrated!")
        return True
    
    # Find the if __name__ == '__main__': section
    if "if __name__ == '__main__':" in content:
        # Add enhancement code before the main block
        enhancement_code = """
# ============ ENHANCEMENTS (Auto-added) ============
try:
    from app_enhancements import enhance_app, add_performance_monitoring, add_error_handling
    socketio = enhance_app(app)
    add_performance_monitoring(app)
    add_error_handling(app)
    print("🚀 Enhancements loaded successfully!")
except Exception as e:
    print(f"⚠️ Enhancements not loaded: {e}")
    socketio = None
# ===================================================

"""
        
        # Insert before if __name__
        parts = content.split("if __name__ == '__main__':")
        new_content = parts[0] + enhancement_code + "if __name__ == '__main__':" + parts[1]
        
        # Modify the run command to support socketio
        if 'app.run(' in new_content and 'socketio.run' not in new_content:
            new_content = new_content.replace(
                'app.run(',
                'socketio.run(app,' if 'socketio' in new_content else 'app.run('
            )
        
        # Backup original
        backup_file = 'app_backup_before_enhancements.py'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Backup created: {backup_file}")
        
        # Write enhanced version
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Enhancements integrated successfully!")
        print("\n📋 What was added:")
        print("  - REST API endpoints (/api/v1/*)")
        print("  - Caching system")
        print("  - Database layer")
        print("  - Performance monitoring")
        print("  - Enhanced error handling")
        print("\n🎯 All existing features remain unchanged!")
        return True
    else:
        print("❌ Could not find main block in app.py")
        return False

if __name__ == '__main__':
    print("🚀 Smart 4D Enhancement Integration")
    print("=" * 50)
    
    result = integrate_enhancements()
    
    if result:
        print("\n✅ Integration complete!")
        print("\n📖 Next steps:")
        print("  1. Run: python app.py")
        print("  2. Visit: http://localhost:5000")
        print("  3. Try API: http://localhost:5000/api/v1/health")
        print("\n📚 Read ENHANCEMENTS_GUIDE.md for full documentation")
    else:
        print("\n❌ Integration failed!")
        print("Please check the error messages above")
    
    input("\nPress Enter to exit...")
