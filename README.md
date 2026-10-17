# 📁 Smart File Organizer (Python & HTML)

A sleek, modern file organizer built with Python and an HTML/CSS glassmorphic frontend. Quickly sort cluttered directories (like Downloads, Desktop, or Documents) into neatly organized subfolders by file extension or file category with a single click.

![File Organizer](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![UI](https://img.shields.io/badge/Frontend-HTML%20%2F%20CSS%20%2F%20JS-brightgreen)
![Framework](https://img.shields.io/badge/Backend-Flask-purple)

---

## ✨ Features

- **🎨 Sleek Modern UI**: Dark glassmorphic interface with vibrant gradients, frosted glass panels, and smooth animations.
- **📂 Folder Location Input**: Paste a path or use the built-in native **Browse** dialog.
- **⚡ Quick Select Shortcuts**: One-click quick shortcuts for `Downloads`, `Documents`, `Desktop`, and `Current Folder`.
- **🗂️ Multiple Organization Modes**:
  - **By Extension**: Groups files into folders matching their extension (`pdf`, `png`, `zip`, `docx`, etc.).
  - **By Category**: Groups files into high-level categories (`Images`, `Documents`, `Audio`, `Videos`, `Archives`, `Code`, `Executables`).
- **🛡️ Safe & Conflict-Proof**:
  - Automatically avoids moving directories into themselves.
  - Safe duplicate renaming (`file (1).ext`) to prevent accidental overwrites.
  - Ignores system files like `desktop.ini`, `Thumbs.db`, `.DS_Store`.
- **📊 Real-time Analytics & Logs**: Live count of files moved, folders created, time elapsed, file breakdown tags, and an **"Open Folder in File Explorer"** button.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You can run either:
```bash
python File_organizer.py
```
or
```bash
python app.py
```

The application will automatically start the server and open your default browser at `http://127.0.0.1:5000`.

---

## 📁 Project Structure

```
File_Organizer/
├── app.py                  # Flask server and file organization engine
├── File_organizer.py       # Main entry point to launch the web UI
├── templates/
│   └── index.html          # Sleek glassmorphic HTML/CSS/JS frontend
├── requirements.txt        # Python package dependencies
├── .gitignore              # Ignored files
└── README.md               # Documentation
```
