import subprocess
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import queue
import json
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}
container_request_queue = queue.Queue()

# Định nghĩa hàm xử lý hàng đợi
def process_container_requests():
    while True:
        request_data = container_request_queue.get()
        if request_data is None:
            break
        socket_id = request_data['socket_id']
        container_id, port = create_container()
        if container_id:
            connected_users[socket_id] = {'container_id': container_id, 'port': port}
            #socketio.emit('server_response', {'message': f'Connected. Container ID: {container_id}, Port: {port} '}, to=socket_id)
        else:
            socketio.emit('server_response', {'message': ''}, to=socket_id)
        container_request_queue.task_done()

# Khởi tạo luồng để xử lý hàng đợi
container_creation_thread = threading.Thread(target=process_container_requests)
container_creation_thread.start()

@app.route('/')
def index():
    return "Flask Socket.IO Server"
#Này dùng để nhận tin nhắn từ người dùng 

@socketio.on('client_event')
def handle_client_event(json_data):
    print('Received event: ' + str(json_data))
    socket_id = request.sid
    print(f"Event received from {socket_id}: {json_data}")
    # Lấy tin nhắn từ dữ liệu JSON
    message = json_data.get('data', '')
    if message:
        # Kiểm tra xem socket_id có trong connected_users không
        if socket_id in connected_users:
            container_info = connected_users[socket_id]
            port = container_info['port']
            try:
                url = f"http://localhost:{port}/generate"
                print(f"URL: {url}")
                
                # Tạo payload từ tin nhắn
                payload = json.dumps({
                    "question": message
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                
                # Gửi yêu cầu POST đến URL
                response = requests.post(url, headers=headers, data=payload)
                
                # Xử lý phản hồi
                response_data = response.json()
                print(response_data)
                response_message = response_data.get('response', '')
                socketio.emit('server_response', {'message':  f'{response_message}'}, to=socket_id)
            except requests.RequestException as e:
                print(f"Error sending request: {e}")
                socketio.emit('server_response', {'message': 'Server is starting please try again in a few seconds'}, to=socket_id)
        else:
            socketio.emit('server_response', {'message': ''}, to=socket_id)
    else:
        socketio.emit('server_response', {'message': ''}, to=socket_id)


@socketio.on('connect')
def connect(auth=None):
    socket_id = request.sid
    container_request_queue.put({'socket_id': socket_id})

@socketio.on('disconnect')
def disconnect():
   socket_id = request.sid
   if socket_id in connected_users:
       container_info = connected_users[socket_id]
       remove_container(container_info['container_id'])
       del connected_users[socket_id]
   print(f"User {socket_id} disconnected.")
   print_connected_users()

@socketio.on('repeat')
def repeat():
    socket_id = request.sid
    container_info = connected_users[socket_id]
    port = container_info['port']
    print(f"Port: {port}")
    print(f"Socket ID: {socket_id}")
    try:
        url = f"http://localhost:{port}/generate"
        print(f"url: {url}")
        payload = json.dumps({
            "question": "Please answer that question again"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        
        response_data = response.json()
        message = response_data.get('response', '')
        socketio.emit('server_response', {'message': f'{message}'}, to=socket_id)
    except requests.RequestException as e:
        print(f"Error sending repeat request: {e}")
        socketio.emit('server_response', {'message': ''}, to=socket_id)
    print_connected_users()

# send tin nhắn phản hồi 
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message', '')
    socket_id = request.sid
    if message:
        socketio.emit('server_response', {'message': message})  
        print(f"Message sent to {socket_id}: {message}")
        return jsonify({'status': 'success', 'message': 'Message sent!'})
    else:
        return jsonify({'status': 'failure', 'message': 'No message provided'}), 400

@app.route('/connected_users', methods=['GET'])
def get_connected_users():
    return jsonify(connected_users)

def print_connected_users():
    print("Connected users:")
    for socket_id, container_info in connected_users.items():
         print(f"Socket ID: {socket_id}, Container ID: {container_info['container_id']}, Port: {container_info['port']}")



def create_container():
    try:
        # Lấy danh sách container IDs cho service-ai
        ps_command = ['docker','compose','ps', '-q', 'service-ai']
        print(f"Running ps command: {' '.join(ps_command)}")
        result = subprocess.run(ps_command, capture_output=True, text=True, check=True)
        print("PS command output:", result.stdout)
        print("PS command error output:", result.stderr)

        container_ids = result.stdout.strip().split('\n')
        current_count = len(container_ids)
        new_count = current_count + 1
        print(f"Current number of service-ai containers: {current_count}")
        print(f"Scaling to: {new_count} containers")

        # Tăng số lượng container của service-ai
        scale_command = [
            'docker','compose','up', '-d', 
            '--scale', f'service-ai={new_count}',
            '--scale', 'proxy=0', 
        ]
        
        print("Running scale command:", ' '.join(scale_command))
        result = subprocess.run(scale_command, capture_output=True, text=True)
        print("Scale command output:", result.stdout)
        result.check_returncode()

        # Lấy danh sách container IDs mới cho service-ai
        result = subprocess.run(ps_command, capture_output=True, text=True, check=True)
        print("Updated PS command output:", result.stdout)
        print("Updated PS command error output:", result.stderr)

        container_ids = result.stdout.strip().split('\n')
        if not container_ids:
            print("No containers found for service-ai.")
            return None, None

        container_id = container_ids[-1]
        print(f"Newest container ID: {container_id}")

        # Inspect container để lấy port
        inspect_command = [
            'docker', 'inspect',
            '--format',
            '{{range $p, $conf := .NetworkSettings.Ports}}{{if $conf}}{{(index $conf 0).HostPort}}{{end}} {{end}}',
            container_id
        ]
        print(f"Running inspect command: {' '.join(inspect_command)}")
        result = subprocess.run(inspect_command, capture_output=True, text=True, check=True)
        print("Inspect command output:", result.stdout)
        print("Inspect command error output:", result.stderr)

        host_ports = result.stdout.strip().split()
        if not host_ports:
            print("No host ports found for the container.")
            return container_id, None

        host_port = host_ports[0]
        print(f"Host port for container {container_id}: {host_port}")

        return container_id, host_port

    except subprocess.CalledProcessError as e:
        print(f"Error creating container: {e}")
        return None, None
def remove_container(container_id):
    try:
        subprocess.run(['docker', 'stop', container_id], check=True)
        subprocess.run(['docker', 'rm', container_id], check=True)
        print(f"Container {container_id} removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi chạy lệnh Docker Compose: {e}")
        print(f"Đầu ra lỗi: {e.stderr}")
        print(f"Mã lỗi: {e.returncode}")

if __name__ == '__main__':
    socketio.run(app, debug=True)
