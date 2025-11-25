import socket
import os
import json
from Protocol import save_dicom_file
import DataBase

HOST = '127.0.0.1'
PORT = 65432
SAVE_ROOT = "dicom_files"

# Initialization of Data Base
DataBase.init_db()


def log(text):
    print(f"[SERVER] {text}")

# Creation of the socket communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
log(f"Server running on {HOST}:{PORT}")


while True:
    client_socket, addr = server_socket.accept()
    log(f"Client connected: {addr}")

    # 1.receiving the packet
    json_meta = client_socket.recv(4096).decode()
    meta = json.loads(json_meta)

    patient_id = meta["patient_id"]
    file_name = meta["file_name"]
    file_size = meta["file_size"]

    log(f"Receiving: {file_name} ({file_size} bytes) from {patient_id}")

    client_socket.send(b"READY")

    # 2. Receiving the file
    received_bytes = b""
    while len(received_bytes) < file_size:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        received_bytes += chunk

    # 3. Saving the file
    save_dir = os.path.join(SAVE_ROOT, patient_id)
    save_path = save_dicom_file(received_bytes, save_dir, file_name)

    # 4. Saving to Data Base
    file_id = DataBase.insert_dicom(
        patient_id,
        file_name,
        save_path,
        file_size
    )

    # 5. Sending to Client answer
    response = json.dumps({"status": "OK", "file_id": file_id})
    client_socket.send(response.encode())

    log(f"Saved: {save_path}, ID={file_id}")
    client_socket.close()


