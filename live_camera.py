import socket
import cv2
import numpy as np
import struct

# Configuration
HOST = ''  # Listen on all interfaces (use '0.0.0.0' or '' for all)
PORT = 8080  # Use the same port as your Android sender

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Listening on port {PORT}...")

try:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    data = b''
    payload_size = struct.calcsize(">L")

    while True:
        # Receive message length first
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                print("Client disconnected.")
                raise ConnectionAbortedError
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        # Receive frame data
        while len(data) < msg_size:
            packet = conn.recv(4096)
            if not packet:
                print("Client disconnected.")
                raise ConnectionAbortedError
            data += packet
        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Decode and show frame
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('Live Video', frame)
        else:
            print("Failed to decode frame.")

        if cv2.waitKey(1) == 27:  # ESC to quit
            print("ESC pressed. Exiting.")
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'conn' in locals():
        conn.close()
    server_socket.close()
    cv2.destroyAllWindows()


# How to use:
# Run this script on your PC.
# On your Android device, use an app or script to capture camera frames, encode them as JPEG, and send them to your PC's IP and port using the same protocol (length-prefixed JPEG frames).
# Android Sender Example:
# You can use apps like IP Webcam (streams over HTTP, not raw sockets) or write a simple script in Python (with QPython or Pydroid) or Java/Kotlin.
# If you want a sample Python sender for Android, let me know!
# Note:
# Both devices must be on the same WiFi network.
# You may need to allow the port through your PC's firewall.
# Let me know if you need the Android sender code or have any questions!