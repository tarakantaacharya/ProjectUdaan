import os
import importlib.util
import inspect

services_path = os.path.join(os.path.dirname(__file__), 'services')

print(f"📁 Inspecting 'services' directory: {services_path}\n")

# List all Python files in the services folder
for filename in os.listdir(services_path):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]
        file_path = os.path.join(services_path, filename)
        
        print(f"🔍 File: {filename}")

        try:
            spec = importlib.util.spec_from_file_location(f"services.{module_name}", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print("   📌 Top-level contents:")
            for name, value in inspect.getmembers(module):
                if not name.startswith("__"):
                    print(f"     - {name} ({type(value).__name__})")

        except Exception as e:
            print(f"   ⚠️ Error importing {filename}: {e}")
        
        print()
