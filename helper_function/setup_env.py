import os
import sys
from dotenv import load_dotenv

def setup_project_env():
    """Loads environment variables and sets up the project's Python path."""
    # Load .env file from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    load_dotenv(dotenv_path=os.path.join(project_root, '.env'))

    # Read PYTHONPATH from .env and add to sys.path
    pythonpath = os.getenv('PYTHONPATH')
    if pythonpath:
        # Split multiple paths if necessary (e.g., if you set PYTHONPATH=path1:path2)
        paths = pythonpath.split(os.pathsep)
        for path in paths:
            abs_path = os.path.abspath(os.path.join(project_root, path))
            if abs_path not in sys.path:
                sys.path.insert(0, abs_path)
                print(f"Added '{abs_path}' to Python path.")