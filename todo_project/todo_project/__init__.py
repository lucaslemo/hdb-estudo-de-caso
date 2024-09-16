import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from logging.handlers import SysLogHandler

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = '3a318cf0a511464396dfcd2b7e9df9a2' #os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

syslog_handler = SysLogHandler(address='/dev/log')
syslog_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(name)s]: [PID:%(process)d] [%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s')
syslog_handler.setFormatter(formatter)

app.logger.addHandler(syslog_handler)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# Always put Routes at end
from todo_project import routes