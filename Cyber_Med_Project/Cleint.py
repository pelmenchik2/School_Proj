import os
import socket
import json
from Protocol import create_upload_packet

HOST = '127.0.0.1'
PORT = 65432

patient_id = "123"
folder_path = r"D:\Cyber_Project_School\140_DICOM_viewer"

def send_file(file_path):
    # Packet preperation
    json_packet = create_upload_packet(file_path, patient_id)

    # Building connection to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # converting from Jsons text to bytes
    sock.send(json_packet.encode())

    # waiting for the response of the Server
    if sock.recv(1024) != b"READY":
        print("Server is not ready.")
        sock.close()
        return

    # size of the file
    file_size = os.path.getsize(file_path)
    sent = 0

    print(f"\nUploading {file_path} ...")

    # sending the file by paths
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sock.send(chunk)
            sent += len(chunk)

            percent = (sent / file_size) * 100
            print(f"\rProgress: {percent:.1f}%", end="")

    # Response from server
    response = sock.recv(4096).decode()
    data = json.loads(response)

    print(f"\nUpload complete! File ID = {data['file_id']}")

    sock.close()

# We sendind all DICOM files
for file in os.listdir(folder_path):
    if file.lower().endswith(".dcm"):
        send_file(os.path.join(folder_path, file))


