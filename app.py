import os

from flask import Flask, jsonify
from flask_restful import Api
from resources.computer import Computers, Computer
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

secret_key = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app=app)
jwt = JWTManager(app)


@app.route('/')
def home():
    return "Hello Flask!!"


@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalido(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401


api.add_resource(Computers, '/computers')
api.add_resource(Computer, '/computers/<int:computer_id>')
api.add_resource(User, '/usuarios/<string:username>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    app.run(debug=True, port=6500)
