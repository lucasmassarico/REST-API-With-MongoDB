from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.computer import ComputerModel
from pymongo.errors import WriteError


# localhost:6500/computers
class Computers(Resource):
    def get(self):
        computers = ComputerModel.find_all_computers()
        if computers:
            return {'computers': [computer for computer in computers]}
        return {'message': "Dont have any 'computer' document in collection."}


# localhost:6500/computers/<id>
class Computer(Resource):
    atributos = reqparse.RequestParser()
    # atributos.add_argument('_id', type=int, required=True, help="The field '_id' cannot be left blank.")
    atributos.add_argument('responsavel', type=str, required=True, help="The field 'responsavel' cannot be left blank.")
    atributos.add_argument('departamento', type=str, required=True, help="The field 'departamento' cannot be left "
                                                                         "blank.")
    atributos.add_argument('tipo', type=str)
    atributos.add_argument('processador', type=str)
    atributos.add_argument('memoria', type=int)
    atributos.add_argument('tp_arm', type=str)
    atributos.add_argument('qnt_arm', type=int)
    atributos.add_argument('modelo', type=str)
    atributos.add_argument('ultimo_dono', type=str)
    # atributos.add_argument('data_transferencia', type=lambda x: datetime.strptime(x, "%d-%m-%Y"))
    atributos.add_argument('data_transferencia', type=str)

    def get(self, computer_id):
        computer = ComputerModel.find_computer(computer_id)
        if computer:
            print(type(computer))
            return computer
        return {"message": 'Computer not found.'}, 404

    @jwt_required()
    def post(self, computer_id):
        if ComputerModel.find_computer(computer_id):
            return {"message": "Computer id '{}' already exists.".format(computer_id)}, 400  # Bad Request
        dados = Computer.atributos.parse_args()
        computer = ComputerModel(computer_id, **dados)
        try:
            computer.save_computer()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' computer.", "error": error}, 500
        return computer.json(), 201

    @jwt_required()
    def put(self, computer_id):
        dados = Computer.atributos.parse_args()
        computer = ComputerModel(computer_id, **dados)
        found_computer = ComputerModel.find_computer(computer_id)
        if found_computer:
            try:
                computer.update_computer()
                return computer.json(), 200
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'create' computer.", "error": error}, 500
        try:
            computer.save_computer()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' computer.", "error": error}, 500
        return computer.json(), 201

    @jwt_required()
    def delete(self, computer_id):
        found_computer = ComputerModel.find_computer(computer_id)
        if found_computer:
            try:
                ComputerModel.delete_computer(computer_id)
            except:
                return {"message": "An error occurred trying to 'delete' computer."}, 500
            return {'message': 'Computer deleted.'}
        return {'message': 'Computer not found.'}, 404
