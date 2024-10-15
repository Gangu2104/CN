import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
import json
import base64

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 16161

# Dictionary to store client names and public keys
clients = {}
videos=["video_1","video_2"]
# Function to handle client connections
def handle_client(client_socket, client_address):
    # Receive client's name and public key
    name = client_socket.recv(4096).decode()
    public_key = client_socket.recv(4096).decode()
    
    # Store client's name and public key in the dictionary
    clients[name] = (public_key, client_socket)
    
    # Broadcast message that a new client has joined
    broadcast_new_client_message(name,client_socket)
    
    print(f"Client {name} connected from {client_address}")
    send_clients_data()
    # Handle client communication
    while True:
        try:
            # Receive client's message
            message = client_socket.recv(4096).decode()
            
            if not message:
                break
            
            if message == '3':
                broadcast_clients_names(client_socket)
            
            elif message.lower() == 'quit':
                break
            
            # Handling encryption request
            elif message == "encrypt":
                
                
                # message1 = client_socket.recv(4096).decode('utf-8','ignore')
                # k=message1.split('$')[0]
                # if k not in clients.keys():
                #     client_socket.send("your receiver is not in the dicussion .please choose again".encode())
                # else:
                #     encrypted_message = encrypt_message(clients[k][0], message1)
                #     broadcast_message(name, encrypted_message)
                message1 = client_socket.recv(4096)
                broadcast_message(name, message1)
                
            elif message == 'video':
                global videos
                vi_list=""
                for k in videos:
                    vi_list+=k + " "
                print(vi_list)
                client_socket.send("#".encode())
                video_transmit(client_socket,vi_list,0)

        except Exception as e:
            print(f"Error: {e}")
            break
    
    # Remove client from dictionary, broadcast client exit, and close client socket
    del clients[name]
    broadcast_client_exit(name)
    send_clients_data()
    client_socket.close()

# Function to broadcast the established client names to all clients
def broadcast_clients_names(conn):
    client_names = ", ".join(clients.keys())
    for client_socket in clients.values():
        if conn==client_socket[1]:
            client_socket[1].send("clients".encode())
            client_socket[1].send(client_names.encode())

# Function to broadcast a message to all connected clients
def broadcast_message(sender_name, message):
    for client_socket in clients.values():
        if client_socket[0] != sender_name:
            client_socket[1].send("decrypt".encode())
            client_socket[1].send(message)
            # client_socket[1].send(sender_name.encode())
            

# Function to broadcast a message that a new client has joined
def broadcast_new_client_message(client_name,conn):
    message = f"{client_name} has joined in the discussion."
    for client_socket in clients.values():
        if client_socket[1] !=conn :
            client_socket[1].send(message.encode())

# Function to broadcast client exit to all connected clients
def broadcast_client_exit(client_name):
    for client_socket in clients.values():
        client_socket[1].send(f"{client_name} has exited.".encode())
        
        
def encrypt_message(public_key_str, message):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message
def send_clients_data():
    clients_serializable = {}
    for name, (public_key, _) in clients.items():
        # public_key_base64 = base64.b64encode(public_key).decode('utf-8')
        clients_serializable[name] = public_key
    
    clients_json = json.dumps(clients_serializable)
    for client_socket in clients.values():
        # client_socket[1].send("D".encode())
        client_socket[1].send(clients_json.encode())  
    



# def video_transmit(connect, files_video,k):
#     global videos
#     connect.send(files_video.encode())
#     v_num = int(connect.recv(4096).decode())
#     connect.send(f"Playing Video: video_{v_num}.mp4".encode())
#     k=k+1
#     try:
#         i=[240,720,1080]
#         current_file_index = 0
#         for x in i:
#             files_video = f"video_{v_num}_{x}_30fps.mp4"
#             # while current_file_index < len(files_video):
#             cap = cv2.VideoCapture(files_video)
#             total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#             start_frame = (total_frames // 3)*current_file_index
#             end_frame = (total_frames // 3) * (current_file_index+1)
#             cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
#                 frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
#                 connect.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)
#                 if  current_frame >= end_frame:
#                     current_file_index += 1
#                     if current_file_index == 3:
#                         connect.send(b'0')
#                     break
#             cap.release()
#     except Exception as e:
#         print(f"Error: {e}")



def video_transmit(conn, video_files, k):
    conn.send(video_files.encode())
    video_num = int(conn.recv(4096).decode())
    conn.send(f"Playing Video: video_{video_num}.mp4".encode())
    k += 1
    try:
        resolutions = [240, 720, 1080]
        section_index = 0
        for resolution in resolutions:
            file_name = f"video_{video_num}_{resolution}.mp4"
            cap = cv2.VideoCapture(file_name)

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frames_per_section = total_frames //3 

            start_frame = frames_per_section * section_index
            end_frame = frames_per_section * (section_index + 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame=cv2.resize(frame, (1080, 720))
                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
                conn.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)

                if current_frame >= end_frame:
                    break

            if section_index == 2:
                conn.send(b'0')
                cap.release()
            section_index += 1 
            print(f'played the video with resolution of {resolution} ...')
            print()
            
    except Exception as e:
        print(f"Error: {e}")


# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

# Accept incoming client connections
while True:
    client_socket, client_address = server_socket.accept()
    
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
