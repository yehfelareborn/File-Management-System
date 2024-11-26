from flask import Blueprint, request, jsonify, send_file, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from minio import Minio
from models import File, db
from flask_cors import CORS
from flask import Flask
import os


file_mgmt = Blueprint('file_mgmt', __name__)

app = Flask(__name__)
CORS(app)  

minio_client = Minio(
    "127.0.0.1:9000",  # MinIO 服務地址
    access_key="minioadmin",  # 用戶名
    secret_key="minioadmin",  # 密碼
    secure=False  # 設置為 False 表示使用 http 協議
)


MINIO_BUCKET = "mybucket"


if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)

@file_mgmt.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"message": "No file part!"}), 400
    
    file = request.files['file']
    file_name = file.filename


    try:
        file.seek(0, os.SEEK_END)  # Move the pointer to the end to get the file size
        file_size = file.tell()    # Get the file size
        file.seek(0)

        minio_client.put_object(MINIO_BUCKET, file_name, file, file_size)
        
        new_file = File(filename=file_name, user_id=current_user, filepath=f'{MINIO_BUCKET}/{file_name}')
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error uploading file: {str(e)}"}), 500

@file_mgmt.route('/list', methods=['GET'])
@jwt_required()
def list_files():
    try:
        
        objects = minio_client.list_objects(MINIO_BUCKET)
        file_names = [obj.object_name for obj in objects]

        return jsonify({"files": file_names}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching file list: {str(e)}"}), 500

@file_mgmt.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download_file(filename):
    try:
        
        file_data = minio_client.get_object(MINIO_BUCKET, filename)
        
        return Response(
            file_data.read(),
            mimetype='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        return jsonify({"message": f"Error downloading file: {str(e)}"}), 500

@file_mgmt.route('/sync', methods=['POST'])
@jwt_required()
def sync_file():
    data = request.json
    return jsonify({"message": "File sync successful!", "data": data}), 200
