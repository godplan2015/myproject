from flask import Flask
import os

SECRET_KEY = os.environ.get('SECRET_KEY')



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kola.db'
# app.config.from_object('app.config.Config')



