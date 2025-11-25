import os
import json

#
def create_upload_packet(file_path, patient_id):

    # dictionary which contains information about the file we want to upload
    file_info = {
        "action": "upload_dicom",
        "patient_id": patient_id,
        # file name to save the file in the srever correctly
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path)
    }
    # converting dictionary to Jsons string(sends before file bytes)
    return json.dumps(file_info)

# The function saves DICOM file to the Server
def save_dicom_file(file_bytes, save_dir, file_name):

    # Create the folder if it does not exist and building file path
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file_name)

    # Write the bytes from the socket
    with open(file_path, 'wb') as f:
        f.write(file_bytes)

    # return the puth in store to Data Base
    return file_path
