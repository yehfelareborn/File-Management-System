from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from auth import auth
from file_management import file_mgmt
from models import db
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
CORS(app)  # 啟用跨域支持

@app.route('/')
def home():
    return "Flask API is testing!"

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(file_mgmt, url_prefix='/file')

with app.app_context():
    db.create_all()  # 初始化數據庫

if __name__ == '__main__':
    app.run(debug=True)
