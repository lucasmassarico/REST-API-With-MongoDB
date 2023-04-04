from flask import jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PWD")
connection_string = f'mongodb+srv://{username}:{password}@cluster.5ougas6.mongodb.net/?retryWrites=true&w=majority'


class ComputerModel:
    client = MongoClient(connection_string)
    db = client['apiwithmongo']
    try:
        db.validate_collection('Computer')
    except Exception as e:
        print(e)
    computer_collection = db['Computer']

    def __init__(self, computer_id, responsavel, departamento, tipo, processador, memoria, tp_arm, qnt_arm, modelo,
                 ultimo_dono, data_transferencia):
        self._id = computer_id
        self.responsavel = responsavel
        self.departamento = departamento
        self.tipo = tipo
        self.processador = processador
        self.memoria = memoria
        self.tp_arm = tp_arm
        self.qnt_arm = qnt_arm
        self.modelo = modelo
        self.ultimo_dono = ultimo_dono
        self.data_transferencia = data_transferencia

    def json(self):
        return {
            '_id': self._id,
            'responsavel': self.responsavel,
            'departamento': self.departamento,
            'tipo': self.tipo,
            'processador': self.processador,
            'memoria': self.memoria,
            'tp_arm': self.tp_arm,
            'qnt_arm': self.qnt_arm,
            'modelo': self.modelo,
            'ultimo_dono': self.ultimo_dono,
            'data_transferencia': self.data_transferencia
        }

    @classmethod
    def find_computer(cls, computer_id):
        computer = cls.computer_collection.find_one({"_id": computer_id})
        if computer:
            # gambiarra
            # computer['data_transferencia'] = computer['data_transferencia'].strftime("%d-%m-%Y")
            return computer
        return None

    @classmethod
    def find_all_computers(cls):
        computers = list(cls.computer_collection.find())
        if computers:
            return computers
        return None

    def save_computer(self):
        self.computer_collection.insert_one({
            "_id": self._id,
            "responsavel": self.responsavel,
            "departamento": self.departamento,
            "tipo": self.tipo,
            "processador": self.processador,
            "memoria": self.memoria,
            "tp_arm": self.tp_arm,
            "qnt_arm": self.qnt_arm,
            "modelo": self.modelo,
            "ultimo_dono": self.ultimo_dono,
            "data_transferencia": self.data_transferencia
        })
        return jsonify(self.json())

    def update_computer(self):
        computer = self.computer_collection.update_one({"_id": self._id}, {'$set': {
            "responsavel": self.responsavel,
            "departamento": self.departamento,
            "tipo": self.tipo,
            "processador": self.processador,
            "memoria": self.memoria,
            "tp_arm": self.tp_arm,
            "qnt_arm": self.qnt_arm,
            "modelo": self.modelo,
            "ultimo_dono": self.ultimo_dono,
            "data_transferencia": self.data_transferencia
        }
        })
        return computer

    @classmethod
    def delete_computer(cls, computer_id):
        return cls.computer_collection.delete_one({"_id": computer_id})

    # com a evolução do sistema, podemos criar um POST que realiza o update da validação do documento
    @classmethod
    def update_collection_validator(cls):
        computer_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "title": "Computer Object Validation",
                "required": ["_id", "responsavel", "departamento"],
                "properties": {
                    "_id": {
                        "bsonType": "int",
                        "description": "'_id' must be a integer and is required"
                    },
                    "responsavel": {
                        "bsonType": "string",
                        "description": "'responsavel' must be a string and is required",
                        "pattern": "^[A-Za-z]+$"
                    },
                    "departamento": {
                        "bsonType": "string",
                        "description": "'departamento' must be a string and is required"
                    },
                    "tipo": {
                        "bsonType": "string",
                        "description": "'tipo' must be a string"
                    },
                    "processador": {
                        "bsonType": "string",
                        "description": "'processador' must be a string"
                    },
                    "memoria": {
                        "bsonType": "int",
                        "description": "'memoria' must be a int"
                    },
                    "tp_arm": {
                        "bsonType": "string",
                        "description": "'tp_arm' must be a string"
                    },
                    "qnt_arm": {
                        "bsonType": "int",
                        "description": "'qnt_arm' must be a int"
                    },
                    "modelo": {
                        "bsonType": "string",
                        "description": "'modelo' must be a string"
                    },
                    "ultimo_dono": {
                        "bsonType": "string",
                        "description": "'ultimo_dono' must be a string"
                    },
                    "data_transferencia": {
                        "bsonType": "string",
                        "description": "'data_transferencia' must be a string"
                    }
                }
            }
        }
        cls.db.command("collMod", "Computer", validator=computer_validator)
