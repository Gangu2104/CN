initially we have to run the server file using command: python 210010036_server.py

after that run simultaneously client files using command :python 210010036_client.py
to get multiple clients.

after that enter the name of each client in corresponding terminal, by that we can send the name of client and public key to the server.

then choose the options displayed in terminal.
         option 1: send message to a client.
         option 2: quit from the discussion.
         option 3: to know about the participants in the discussion.
         option 4 : video playback
         option 5 : clients dictionary in client side


if you want to send a message to participant in the discussion ,for that 
choose option 1
and then send the receiver name,
encrypt the message and send the message to server and it will broadcast to every client.

when we encrypt the message via public key of receiver, when it broadcast only the receiver can decrypt the message and understand  the message properly.

if you want to quit the discussion enter the option 2 we will send a message quit to the server to remove the connection between server and client.

if you want to know about the people who are in the discussion then enter the option 3

if you want to play the video which is on server choose option 4

then enter the video number you want to choose 

by that it will transmit the video by server and you will receive the video,by that it will displayed.
in the server side side we can see whether the displayed video with corresponding pixels.

also there is some naming convention for videos which we run should be in the format {video_1_240,video_1_720,video_1_1080}

if you want to check whether the dictionary containing name and public key sent by the server are updating in the client side or not 
choose option 5

if the internet speed is slow then some times it in the terminal the displaying messages should be delayed.
also when ever the videoes are running dont try to enter a new client.(assumption)




Overview

This project implements a socket programming system where a server manages client connections, 
maintains client information securely, 
and facilitates secure communication and video streaming among clients

Features

Client Connection Management:

Clients can connect to the server, providing their name and generated public key.
The server maintains a dictionary mapping client names to their public keys and broadcasts this information to all connected clients.
Clients can disconnect by sending a 'QUIT' message to the server, which removes their entry from the dictionary and notifies other clients.


Secure Communication Management:

Clients can securely communicate with each other using public-key cryptography.
The server broadcasts encrypted messages among clients, ensuring only the intended recipient can decrypt and read the message.


Video Streaming Management:

The server streams video files to clients without saving them locally.
Clients can request a list of available videos and play a selected video file


used libraries

OpenCV (for video streaming)
PyCryptoDome (for RSA encryption)

---------------------------------
I have implemented the steps as asked in the problem statement.

client side 
-----------
1)first the name of the client will be asked.
Enter Your name:

2)The generated public will be sent to server and the dictionary named clientsdata will store 
the name and corresponding public key in the dictionary

3)This dictionary will be brodacasted to the every client in the connection.

4)I have provided the following options for the client as asked in problem statement

 demovideo:

 https://drive.google.com/file/d/1ReeRto6iS-wSWJvir1MfV_G4Vk40onoq/view?usp=sharing

Thankyou