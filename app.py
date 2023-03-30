from flask import Flask
from flask_restful import Api
from resources.computer import Computers, Computer

app = Flask(__name__)
api = Api(app=app)


@app.route('/')
def home():
    return "Hello Flask!!"


api.add_resource(Computers, '/computers')
api.add_resource(Computer, '/computers/<int:computer_id>')

if __name__ == '__main__':
    app.run(debug=True, port=6500)
