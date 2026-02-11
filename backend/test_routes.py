from app.main import app

print("All routes in the app:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  {route.path}")
    if hasattr(route, 'methods'):
        print(f"    Methods: {route.methods}")
