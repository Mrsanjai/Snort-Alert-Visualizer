import os
from config import Config

def read_all_snort_logs(base_directory=None):
    """
    Recursively read .log and .ids files from the given base directory including all subdirectories.
    """
    if base_directory is None:
        base_directory = Config.LOG_ROOT_DIR

    log_entries = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(('.log', '.ids')):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', errors='ignore') as f:
                        lines = f.readlines()
                        log_entries.append({
                            'file_path': full_path,
                            'file_name': os.path.basename(full_path),
                            'log_preview': lines[-20:] if len(lines) > 20 else lines
                        })
                except Exception as e:
                    log_entries.append({
                        'file_path': full_path,
                        'file_name': os.path.basename(full_path),
                        'log_preview': [f'Error reading file: {e}']
                    })
    return log_entries
