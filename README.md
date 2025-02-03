# YouTube Video Preview App

A simple web application that allows devices on the same network to share and preview YouTube videos.

## Features
- Add YouTube videos by pasting their URLs
- Preview videos directly in the browser
- Responsive design that works on all devices
- Real-time updates across all connected devices

## Setup and Running

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the application:
- From your computer: `http://localhost:5001` or `http://youtube-queue.local:5001`
- From other devices on the same network: `http://youtube-queue.local:5001`

Note: The `.local` domain uses mDNS/Bonjour for automatic discovery. This works on:
- iOS devices
- macOS devices
- Most modern browsers on other devices

If the `.local` domain doesn't work on your device, you can still use the IP address directly: `http://<your-computer-ip>:5001`

## Usage
1. Paste a YouTube video URL into the input field
2. Click "Add Video" to add it to the preview grid
3. The video will be immediately available for preview on all connected devices
