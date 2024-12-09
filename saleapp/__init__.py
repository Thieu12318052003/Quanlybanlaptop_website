from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/qlLapTop?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key='@aoas9%@$jiUug9SIhjsuihwd'
app.config['PAGE_SIZE'] = 10
#tao ra bien login (truyen app), xong vao model kee thua user login
login=LoginManager(app=app)

db = SQLAlchemy(app=app)

admin = Admin(app=app,name='Quản Trị LapTop', template_mode='bootstrap4')

