# SnapPic

SnapPic is a Flask-based web application that allows users to upload images with comments and view them in a gallery. Images are visible for 5 seconds, then fade out over 10 seconds before being automatically deleted. The gallery supports a maximum of 10 images at a time, following a FIFO principle. The app is designed as a Progressive Web App (PWA) with offline capabilities, mobile-first responsive design, and Material Design principles.

## Features

- **Upload Interface:** Take photos via smartphone camera or select from gallery, add a short comment (max 100 characters).
- **Gallery View:** Automatically updates every 2 seconds, with fade-out animations for expiring images.
- **PWA Support:** Installable on devices, works offline via Service Worker, includes manifest and icon.
- **Backend Logic:** Handles uploads, validates file types (JPG, PNG, WEBP), size (max 5MB), and manages image lifecycle with automatic cleanup.
- **Data Storage:** Metadata in `data.json`, images in `uploads/` folder.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd snappic
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python app.py
```

- Access the upload interface at `http://localhost:5000/`.
- View the gallery at `http://localhost:5000/gallery`.

## Technical Details

- Built with Flask (Python) for the backend.
- Vanilla HTML/CSS/JavaScript for the frontend.
- Uses threading for background cleanup.
- Compatible with Python 3.8+.

This app was created with aider v0.85.2dev and grok4 'one-shot' based on the prompt. The one-shot costs $0.05 using api call (creating the README was an extra call)
