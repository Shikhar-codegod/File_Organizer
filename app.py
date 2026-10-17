import os
import shutil
import time
import webbrowser
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CATEGORY_MAP = {
    'Images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'ico', 'tiff', 'heic'],
    'Documents': ['pdf', 'docx', 'doc', 'txt', 'rtf', 'xlsx', 'xls', 'pptx', 'ppt', 'csv', 'odt', 'epub'],
    'Audio': ['mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a', 'wma'],
    'Videos': ['mp4', 'mkv', 'flv', 'avi', 'mov', 'wmv', 'webm', 'm4v'],
    'Archives': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'iso'],
    'Code': ['py', 'js', 'html', 'css', 'json', 'cpp', 'c', 'java', 'cs', 'php', 'ts', 'sh', 'sql', 'xml'],
    'Executables': ['exe', 'msi', 'bat', 'cmd', 'apk'],
}

def get_unique_path(dest_dir, file_name):
    base, ext = os.path.splitext(file_name)
    dest_path = os.path.join(dest_dir, file_name)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{base} ({counter}){ext}")
        counter += 1
    return dest_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/browse')
def browse():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        selected_folder = filedialog.askdirectory(title="Select Folder to Organize")
        root.destroy()
        return jsonify({'folder': selected_folder.replace('/', '\\') if selected_folder else ''})
    except Exception as e:
        return jsonify({'error': str(e), 'folder': ''})

@app.route('/api/quick-path')
def quick_path():
    path_type = request.args.get('type', 'Downloads')
    home = Path.home()
    
    if path_type == 'Downloads':
        target = home / 'Downloads'
    elif path_type == 'Documents':
        target = home / 'Documents'
    elif path_type == 'Desktop':
        target = home / 'Desktop'
    elif path_type == 'Current':
        target = Path.cwd()
    else:
        target = home

    return jsonify({'path': str(target) if target.exists() else str(home)})

@app.route('/api/open-folder', methods=['POST'])
def open_folder():
    data = request.get_json() or {}
    folder = data.get('folder', '')
    if folder and os.path.exists(folder):
        try:
            os.startfile(folder)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': False, 'error': 'Folder does not exist'})

@app.route('/api/organize', methods=['POST'])
def organize():
    start_time = time.time()
    data = request.get_json() or {}
    folder = data.get('folder', '').strip()
    mode = data.get('mode', 'extension')  # 'extension' or 'category'

    if not folder:
        return jsonify({'success': False, 'error': 'Please provide a valid folder path.'}), 400

    if not os.path.exists(folder):
        return jsonify({'success': False, 'error': f'The folder does not exist: "{folder}"'}), 400

    if not os.path.isdir(folder):
        return jsonify({'success': False, 'error': f'The specified path is not a directory: "{folder}"'}), 400

    try:
        entries = os.listdir(folder)
    except PermissionError:
        return jsonify({'success': False, 'error': 'Permission denied accessing this directory.'}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    # System and protected files to ignore
    ignore_files = {'desktop.ini', 'thumbs.db', '.ds_store', 'file_organizer.py', 'app.py'}

    moved_count = 0
    folders_created = set()
    breakdown = {}
    moved_files = []

    for item in entries:
        item_path = os.path.join(folder, item)

        # Only process files, skip directories
        if not os.path.isfile(item_path):
            continue

        if item.lower() in ignore_files or item.startswith('.'):
            continue

        filename, extension = os.path.splitext(item)
        ext_clean = extension[1:].lower() if extension.startswith('.') else extension.lower()

        # Determine target folder name based on mode
        if mode == 'category':
            target_folder_name = 'Other'
            for category, ext_list in CATEGORY_MAP.items():
                if ext_clean in ext_list:
                    target_folder_name = category
                    break
            breakdown_key = target_folder_name
        else:
            target_folder_name = ext_clean.lower() if ext_clean else 'No_Extension'
            breakdown_key = ext_clean.lower() if ext_clean else 'none'

        target_dir = os.path.join(folder, target_folder_name)

        # Create target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            folders_created.add(target_folder_name)
        else:
            folders_created.add(target_folder_name)

        # Determine destination path safely without overwrite collisions
        dest_path = get_unique_path(target_dir, item)
        shutil.move(item_path, dest_path)

        moved_count += 1
        breakdown[breakdown_key] = breakdown.get(breakdown_key, 0) + 1
        moved_files.append({
            'file': item,
            'dest': f"{target_folder_name}/{os.path.basename(dest_path)}"
        })

    elapsed = round(time.time() - start_time, 2)

    msg = f"Successfully organized {moved_count} file{'s' if moved_count != 1 else ''} into {len(folders_created)} folder{'s' if len(folders_created) != 1 else ''}!"
    if moved_count == 0:
        msg = "No files found to organize. All items may already be organized or inside subfolders."

    return jsonify({
        'success': True,
        'message': msg,
        'total_files': moved_count,
        'folders_created': len(folders_created),
        'breakdown': breakdown,
        'moved_files': moved_files,
        'time_taken': elapsed
    })

def open_browser():
    time.sleep(1.2)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    print("==================================================")
    print(" 🚀 File Organizer Web UI is running!")
    print(" 🌐 Opening browser at: http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=False)
