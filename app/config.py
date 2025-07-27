import os
class Config:
    SECRET_KEY = 'snort-secret-key'
    LOG_ROOT_DIR = r"D:\DevTools\Projects\Snort-Alert-Visualizer\uploads"  # <--- updated
    UPLOAD_FOLDER = LOG_ROOT_DIR
    ALLOWED_EXTENSIONS = {'log', 'ids'}
