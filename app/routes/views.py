from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import os
import threading
import time
import json
from werkzeug.utils import secure_filename
from app.log_reader import parse_snort_logs
from app.config import Config


views_bp = Blueprint('views_bp', __name__)

UPLOAD_FOLDER = Config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ======= Global cache for logs & thread lock ========
log_cache = []
cache_lock = threading.Lock()


# ========== Directory Watcher Thread ==========
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class SnortLogHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.log', '.ids')):
            # Refresh cache on any log file change/addition/deletion
            update_log_cache()


def update_log_cache():
    global log_cache
    with cache_lock:
        log_cache = parse_snort_logs()

        # Save to realtime_alerts.json
        try:
            with open('realtime_alerts.json', 'w') as f:
                json.dump(log_cache, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Could not write to realtime_alerts.json: {e}")


def start_watcher():
    event_handler = SnortLogHandler()
    observer = Observer()
    # Watch BOTH live Snort logs folder and uploads folder recursively
    observer.schedule(event_handler, Config.LOG_ROOT_DIR, recursive=True)
    observer.schedule(event_handler, Config.UPLOAD_FOLDER, recursive=True)
    observer.start()
    print(f"Started watchdog observer on:")
    print(f" - {Config.LOG_ROOT_DIR}")
    print(f" - {Config.UPLOAD_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Start the watcher thread only once on module import
watcher_thread = threading.Thread(target=start_watcher, daemon=True)
watcher_thread.start()

# Initial cache load
update_log_cache()


# ----------- Dashboard Route ----------
@views_bp.route('/')
def dashboard():
    return render_template('dashboard.html')


# ----------- Explorer Route -----------
@views_bp.route('/explorer', methods=['GET'])
def explorer():
    date_filter = request.args.get('date')
    ip_filter = request.args.get('ip')
    severity_filter = request.args.get('severity')

    with cache_lock:
        logs = log_cache.copy()

    if date_filter:
        logs = [log for log in logs if log.get('timestamp', '').startswith(date_filter)]

    if ip_filter:
        logs = [
            log for log in logs
            if ip_filter in (log.get('src_ip', '') + log.get('dest_ip', ''))
        ]

    if severity_filter:
        logs = [
            log for log in logs
            if log.get('severity', '').lower() == severity_filter.lower()
        ]

    return render_template('explorer.html', logs=logs)


# ----------- Upload Route -------------
@views_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'logfile' not in request.files:
            flash('⚠️ No file part in the request.')
            return redirect(request.url)

        file = request.files['logfile']

        if file.filename == '':
            flash('⚠️ No file selected.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            full_path = os.path.join(UPLOAD_FOLDER, filename)

            try:
                file.save(full_path)
                flash(f'✅ File uploaded successfully!')
                # Update cache with new uploaded logs
                update_log_cache()
            except Exception as e:
                flash(f'❌ Error saving file: {str(e)}')
                return redirect(request.url)

            return redirect(url_for('views_bp.explorer'))

        flash('❌ Invalid file type. Only .log and .ids files allowed.')
        return redirect(request.url)

    return render_template('upload.html')


# ---------- Real-Time Alerts API ----------
@views_bp.route('/api/realtime-alerts')
def realtime_alerts():
    try:
        with open('realtime_alerts.json', 'r') as f:
            alerts = json.load(f)
    except Exception:
        alerts = []
    return jsonify(alerts)
