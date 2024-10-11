import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import queue
import json
import requests
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app)

connected_users = {}
container_request_queue = queue.Queue()
path = "http://35.238.176.124"

# Tạo uid 
def generate_user_id():
    return str(uuid.uuid4())

# Định nghĩa hàm xử lý hàng đợi
def process_container_requests():
    while True:
        request_data = container_request_queue.get()
        print(f"Request data: {request_data}")
        if request_data is None:
            print("break")
            break
        print(f"Iam here")
        uid = request_data['uid']
        container_id, port = create_container()
        if container_id and uid:
            connected_users[uid] = {'container_id': container_id, 'port': port}
        else :
            print("fail")
        container_request_queue.task_done()

# Khởi tạo luồng để xử lý hàng đợi
container_creation_thread = threading.Thread(target=process_container_requests)
container_creation_thread.start()

@app.route('/')
def index():
    return "Flask HTTP Server"

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'  # Ngăn lưu vào cache
    return response
    
# Route để nhận sự kiện từ người dùng
@app.route('/client_event', methods=['POST'])
def handle_client_event():
    json_data = request.get_json()
    print('Received event: ' + str(json_data))
    uid = request.args.get('uid')
    print(f"Event received from {uid}: {json_data}")
    message = json_data.get('data', '')
    if message:
        # Kiểm tra xem uid có trong connected_users không
        if uid in connected_users:
            message = message + ".If the answer is not in the context, do not give information not mentioned in the CONTEXT INFORMATION and can say that you do not know or something like that. Always response in Vietnamese"
            container_info = connected_users[uid]
            port = container_info['port']
            try:
                url = f"{path}:{port}/generate"
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
                return jsonify({'message': response_message})
            except requests.RequestException as e:
                print(f"Error sending request: {e}")
                return jsonify({'message': 'Server is starting please try again in a few seconds'}), 500
        else:
            return jsonify({'message': 'User not connected'}), 404
    else:
        return jsonify({'message': 'No message provided'}), 400

# Kết nối container cho người dùng
@app.route('/connect', methods=['GET'])
def connect():
    uid = request.args.get('uid')
    if not uid:
        uid = generate_user_id()
        container_request_queue.put({'uid': uid })
        return jsonify({'status': uid})
    return jsonify({'status': 'no uid provided'}), 400

@app.route('/check-container', methods=['GET'])
def check():
    uid = request.args.get('uid')
    
    # Kiểm tra sự tồn tại của uid trong connected_users
    if uid in connected_users and connected_users[uid] is None:
        return 'False'  # Trả về 'False' nếu người dùng không được kết nối
    elif uid in connected_users:
        return 'True'   # Trả về 'True' nếu người dùng đã được kết nối
    return 'False'  # Nếu uid không tồn tại trong connected_users, trả về 'False'

# Ngắt kết nối và xóa container
@app.route('/disconnect', methods=['POST'])
def disconnect():
   uid = request.args.get('uid')
   if uid in connected_users:
       container_info = connected_users[uid]
       remove_container(container_info['container_id'])
       del connected_users[uid]
   print(f"User {uid} disconnected.")
   print_connected_users()
   return jsonify({'status': 'disconnected'})

@app.route('/connected_users', methods=['GET'])
def get_connected_users():
    return jsonify(connected_users)

def print_connected_users():
    for uid, container_info in connected_users.items():
        print(f"Socket ID: {uid}, Container ID: {container_info['container_id']}, Port: {container_info['port']}")

def create_container():
    try:
        # Lấy danh sách container IDs cho service-ai
        ps_command = ['docker','compose','ps', '-q', 'service-ai']
        result = subprocess.run(ps_command, capture_output=True, text=True, check=True)
        print("PS command output:", result.stdout)
        container_ids = result.stdout.strip().split('\n')
        current_count = len(container_ids)
        new_count = current_count + 1
        print(f"Current number of service-ai containers: {current_count}")
        print(f"Scaling to: {new_count} containers")

        # Tăng số lượng container của service-ai
        scale_command = [
            'docker','compose','up', '-d', '--scale', f'service-ai={new_count}', '--scale', 'proxy=1',
        ]
        print("Running scale command:", ' '.join(scale_command))
        result = subprocess.run(scale_command, capture_output=True, text=True)
        print("Scale command output:", result.stdout)
        result.check_returncode()

        # Lấy danh sách container IDs mới cho service-ai
        result = subprocess.run(ps_command, capture_output=True, text=True, check=True)
        print("Updated PS command output:", result.stdout)

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

# 
@app.route('/repeat', methods=['GET'])
def repeat():
    uid = request.args.get('uid')
    if uid in connected_users:
        container_info = connected_users[uid]
        port = container_info['port']
        print(f"Port: {port}")
        print(f"ID: {uid}")
        try:
            url = f"{path}:{port}/generate"
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
            return jsonify({'message': message})
        except requests.RequestException as e:
            print(f"Error sending repeat request: {e}")
            return jsonify({'message': 'Error'}), 500
    else:
         return jsonify({'message': 'User not connected'}), 404

# Gửi tin nhắn phản hồi
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message', '')
    uid = request.args.get('uid')
    if message:
        print(f"Message sent to {uid}: {message}")
        return jsonify({'status': 'success', 'message': 'Message sent!'})
    else:
        return jsonify({'status': 'failure', 'message': 'No message provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)