
import os

def clear_cache():
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            for file in os.listdir(cache_path):
                file_path = os.path.join(cache_path, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            os.rmdir(cache_path)
