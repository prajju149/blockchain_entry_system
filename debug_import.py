import sys
import importlib.util

# Load utils directly
spec = importlib.util.spec_from_file_location("utils", "server/utils.py")
utils = importlib.util.module_from_spec(spec)
print(f"Before exec: {dir(utils)}")
try:
    spec.loader.exec_module(utils)
    print(f"After exec: {dir(utils)}")
except Exception as e:
    print(f"Error executing utils: {e}")
    import traceback
    traceback.print_exc()
