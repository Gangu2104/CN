import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
import numpy as np
import json
import base64
# Server configuration
SERVER_HOST = '127.0.0.1'  # localhost
SERVER_PORT = 16161
complete = False
# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
clients={}
# Function to receive and print broadcasted information from the server
def receive_broadcast():
    global clients
    while True:
        try:
            broadcast_info = client_socket.recv(4096).decode()
            
            if not broadcast_info:
                break
            
            elif broadcast_info == "decrypt":
                # print("decrypt")
                broadcast_info1 = client_socket.recv(4096)
                # print(broadcast_info1)
                decrypted_message = decrypt_message(broadcast_info1, private_key)
                if decrypted_message is not None:
                    # print("hi")
                    decrypted_message_extracted = decrypted_message.decode()
                    name_extracted = decrypted_message_extracted.split('$')[0]
                    msg_extracted = decrypted_message_extracted.split('$')[1]
                    print("\nFrom:" + name_extracted)
                    print()
                    print(f"Received Message:{ msg_extracted}")
            elif broadcast_info=="#":
                data = client_socket.recv(4096).decode()
                video_extract(data) 
            elif broadcast_info[0]=="{":
                
                # clients_json = client_socket.recv(4096).decode()
                # clients = json.loads(clients_json)
                receive_clients_data(broadcast_info)
            elif broadcast_info=="clients":
                broadcast_info1 = client_socket.recv(4096).decode()
                print(f"clients in the discussion: {broadcast_info1}")
            else: 
                print(f"Broadcasted Info: {broadcast_info}")
        
        except UnicodeDecodeError as e:
            print(f"Error decoding data: {e}")
            continue  # Continue loop if decoding error occurs
            
        except OSError as e:
            print(f"Error receiving broadcast: {e}")
            break


# Start a thread to receive and print broadcasted information
broadcast_thread = threading.Thread(target=receive_broadcast)
broadcast_thread.start()

# Function to send name and public key to the server
def generate_key_pair():
    key = RSA.generate(1024)
    return key.publickey(), key  

public_key, private_key = generate_key_pair()
public_key_str = public_key.export_key().decode()

# def send_name_and_key():
client_name = input("Enter your name: ")
client_socket.send(client_name.encode())
client_socket.send(public_key_str.encode())
# public_key_base64 = base64.b64encode(public_key_str).decode('utf-8')
    
# client_socket.send(public_key_base64.encode())

# Send name and public key to the server
# send_name_and_key()

def encrypt_message(public_key_str, message):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, private_key):
    try:
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message
    except ValueError as e:
        return None
def video_extract(data):
    global complete
    print(data)
    user_video = input("Enter the video number you want to watch(ex:1 in video_1 like that): ")
    client_socket.send(user_video.encode())
    response = client_socket.recv(4096).decode()
    print(response)
    while True:
        frame_size_data = client_socket.recv(16)
        if not frame_size_data:
            break
        frame_size = int(frame_size_data.strip())
        if frame_size == 0:
            break
        frame_data = b''
        while len(frame_data) < frame_size:
            remaining_bytes = frame_size - len(frame_data)
            frame_data += client_socket.recv(remaining_bytes)
        frame_np = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (1080, 720))
        cv2.imshow('Video Stream', frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    complete=True
def receive_clients_data(clients_json):
    global clients
    # clients_json = client_socket.recv(4096).decode()
    clients = json.loads(clients_json)
# Function to send messages to the server
def send_message():
    global complete
    global clients
    while True:
        # print(clients)
        
        
        print("-----------------------------------------------------")
        print("choose the options:")
        print(" option 1: send message to a client.")
        print(" option 2: quit from the discussion.")
        print(" option 3: to know about the participants in the discussion.")
        print(" option 4 : video playback")
        print(" option 5 : clients dictionary in client side")
        print("-----------------------------------------------------")
        
        choose = input("choose an option: ")
        
        if choose == '1':
            receiver = input("enter the receiver name:")
            message = client_name + "$" + input("Enter message to send: ")
            client_socket.send("encrypt".encode())
            # if receiver not in clients:
            if receiver not in clients:
                print("please recheck the name of the receiver:")
            else:
                encrypted_message = encrypt_message(clients[receiver], message)
                client_socket.send(encrypted_message)   

        elif choose == '2':
            message = "quit"
            client_socket.send(message.encode())
            break
        
        elif choose == '3':
            client_socket.send(choose.encode())
        elif choose == '4':
            client_socket.send('video'.encode())
            while not complete:
                pass
            complete = False
        elif choose=='5':
            # print('hi')
            for x in clients:
                print(x)
                # print(clients[x])
        else:
            print("please choose from the above options only. ")

    # Close the client socket when "QUIT" message is sent
    client_socket.close()

# Start a thread to send messages
send_message()

