import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:senha@mysql:3306/certificados_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
