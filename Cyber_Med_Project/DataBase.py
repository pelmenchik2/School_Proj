import sqlite3
import os

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dicom_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        file_name TEXT,
        file_path TEXT,
        size INTEGER
    )
    ''')

    conn.commit()
    conn.close()


def insert_dicom(patient_id, file_name, file_path, size):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO dicom_files (patient_id, file_name, file_path, size) VALUES (?, ?, ?, ?)",
        (patient_id, file_name, file_path, size)
    )

    conn.commit()
    file_id = cursor.lastrowid
    conn.close()

    return file_id


def get_files_by_patient(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, file_name, file_path, size FROM dicom_files WHERE patient_id = ?",
        (patient_id,)
    )

    results = cursor.fetchall()
    conn.close()
    return results
