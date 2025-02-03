# YouTube Karaoke Queue

A web application that allows devices on the same network to share and queue YouTube videos for karaoke sessions.

## Features
- Add YouTube videos by pasting their URLs or searching directly
- Two modes: Singer (for adding videos) and Screen (for displaying)
- Drag-and-drop queue management
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
- From your computer: `http://localhost:5002`
- From other devices on the same network: `http://<your-computer-ip>:5002`

## Usage
1. Open the welcome page and choose your mode:
   - Singer Mode: For adding and managing videos
   - Screen Mode: For displaying the video queue

2. In Singer Mode:
   - Search for videos using the search bar
   - Add videos to the queue
   - Reorder videos using drag and drop

3. In Screen Mode:
   - View the current video queue
   - Videos play automatically in sequence
