from bson import json_util
import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST
from models.usuario import UserModel
import hmac

atributos = reqparse.RequestParser()
atributos.add_argument('username', type=str, required=True, help="The field 'username' cannot be left blank.")
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")


class User(Resource):
    def get(self, username):
        user = UserModel.find_user(username)
        if user:
            return json.loads(json_util.dumps(user))
        return {"message": "User not found."}, 404

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_user(username)
        print(user)
        if user:
            try:
                UserModel.delete_user(username)
            except:
                return {'message': 'An error occurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    # / cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_user(dados['username']):
            return {'message': "The username '{}' already exists.".format(dados['username'])}
        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_user(dados['username'])
        if user and hmac.compare_digest(user['password'], dados['password']):
            token_de_acesso = create_access_token(identity=user['username'])
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
