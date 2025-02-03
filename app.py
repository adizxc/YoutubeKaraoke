from flask import Flask, render_template, request, jsonify
import re
from datetime import datetime
import socket
import netifaces
from googleapiclient.discovery import build
import os

# YouTube API setup
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'AIzaSyBqAheDHND8YvKDRP03MxmZ5APIM_c7h_8')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

app = Flask(__name__)

def get_local_ip():
    try:
        # Get the default gateway interface
        gws = netifaces.gateways()
        default_interface = gws['default'][netifaces.AF_INET][1]
        
        # Get the IP address for this interface
        addrs = netifaces.ifaddresses(default_interface)
        return addrs[netifaces.AF_INET][0]['addr']
    except:
        # Fallback method
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 1))
            local_ip = s.getsockname()[0]
        except:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        return local_ip

# Store videos and queue in memory (for demonstration purposes)
videos = []
queue = []

def extract_video_id(url):
    """Extract YouTube video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\?\/]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/singer')
def singer():
    return render_template('singer.html', queue=queue)

@app.route('/screen')
def screen():
    return render_template('screen.html', videos=videos, queue=queue)

@app.route('/add_video', methods=['POST'])
def add_video():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    video_data = {
        'id': video_id,
        'url': url,
        'embed_url': f'https://www.youtube.com/embed/{video_id}',
        'added_at': datetime.now().isoformat(),
        'position': len(queue)
    }
    
    if video_data not in videos:
        videos.append(video_data)
    
    # Add to queue if not already in queue
    if not any(v['id'] == video_id for v in queue):
        queue.append(video_data)
    
    return jsonify({'success': True, 'video': video_data, 'queue': queue})

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify({'queue': queue})

@app.route('/queue/remove', methods=['POST'])
def remove_from_queue():
    video_id = request.form.get('video_id')
    if not video_id:
        return jsonify({'error': 'No video ID provided'}), 400
    
    global queue
    queue = [v for v in queue if v['id'] != video_id]
    # Update positions
    for i, video in enumerate(queue):
        video['position'] = i
    
    return jsonify({'success': True, 'queue': queue})

@app.route('/queue/reorder', methods=['POST'])
def reorder_queue():
    video_id = request.form.get('video_id')
    new_position = request.form.get('new_position')
    
    if not video_id or new_position is None:
        return jsonify({'error': 'Missing video_id or new_position'}), 400
    
    try:
        new_position = int(new_position)
    except ValueError:
        return jsonify({'error': 'Invalid position'}), 400
    
    video_to_move = None
    for video in queue:
        if video['id'] == video_id:
            video_to_move = video
            break
    
    if not video_to_move:
        return jsonify({'error': 'Video not found in queue'}), 404
    
    queue.remove(video_to_move)
    new_position = max(0, min(new_position, len(queue)))
    queue.insert(new_position, video_to_move)
    
    # Update positions
    for i, video in enumerate(queue):
        video['position'] = i
    
    return jsonify({'success': True, 'queue': queue})

@app.route('/youtube/search', methods=['GET'])
def youtube_search():
    query = request.args.get('q', '')
    page_token = request.args.get('pageToken', None)
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    try:
        search_params = {
            'q': query,
            'part': 'snippet',
            'maxResults': 10,
            'type': 'video'
        }
        
        if page_token:
            search_params['pageToken'] = page_token
        
        search_response = youtube.search().list(**search_params).execute()
        
        videos = [{
            'id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'thumbnail': item['snippet']['thumbnails']['medium']['url'],
            'channel': item['snippet']['channelTitle'],
            'url': f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        } for item in search_response['items']]
        
        return jsonify({
            'videos': videos,
            'nextPageToken': search_response.get('nextPageToken'),
            'prevPageToken': search_response.get('prevPageToken')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = 5002
    local_ip = get_local_ip()
    print(f"\nApp is accessible at:")
    print(f"Local access:     http://localhost:{port}")
    print(f"Network access:   http://{local_ip}:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=True)
