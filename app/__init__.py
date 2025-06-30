from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# ☝️ Au lieu de app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes