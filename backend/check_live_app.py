"""Check what's actually in the running app"""
import sys
import importlib

# Force reload of modules
if 'app.main' in sys.modules:
    del sys.modules['app.main']
if 'app.api.v1.ai_analysis' in sys.modules:
    del sys.modules['app.api.v1.ai_analysis']

# Now import fresh
from app.main import app

print("Routes in app:")
for route in app.routes:
    if hasattr(route, 'path') and '/ai/' in route.path:
        print(f"  ✅ {route.path} - {route.methods if hasattr(route, 'methods') else 'N/A'}")

# Check if any AI routes exist
ai_routes = [r for r in app.routes if hasattr(r, 'path') and '/ai/' in r.path]
if ai_routes:
    print(f"\n✅ Found {len(ai_routes)} AI routes!")
else:
    print("\n❌ No AI routes found!")
    
# Try to import the router directly
try:
    from app.api.v1 import ai_analysis
    print(f"\n✅ ai_analysis module imported successfully")
    print(f"   Router: {ai_analysis.router}")
    print(f"   Routes in router: {[r.path for r in ai_analysis.router.routes]}")
except Exception as e:
    print(f"\n❌ Failed to import ai_analysis: {e}")
