# Third party libraries
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Python
import uuid
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=30)
jwt = JWT(app, authenticate, identity)


agendas = [
    {
        "agenda_name": "Pedro",
        "agenda_contact": [
            {
                "name": "Pedro",
                "address": "1234 Nw Weston",
                "phoneN": 7143241254,
                "id": str(uuid.uuid4())
            }
        ]
    }
]


class Agenda_List(Resource):
    @jwt_required()
    def get(self):
        return agendas

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("agenda_name",
                            type=str,
                            required=True,
                            help="Please use a valid name")
        data = parser.parse_args()
        agenda_name = next(filter(
            lambda agenda: agenda["agenda_name"] == data["agenda_name"], agendas), None)
        if agenda_name:
            return {"message": "This agenda name already exist"}
        else:
            new_agenda = {
                "agenda_name": data["agenda_name"],
                "agenda_contact": []
            }
            agendas.append(new_agenda)
            return new_agenda


class Agenda(Resource):
    def get(self, name):
        contact = next(
            filter(lambda contact: contact["agenda_name"] == name, agendas), None)
        if contact:
            return contact
        else:
            return {"message": "Sorry this contact does not exist"}

    def delete(self, name):
        global agendas
        for agenda in agendas:
            if agenda["agenda_name"] == name:
                agendas = list(
                    filter(lambda agenda: agenda["agenda_name"] != name, agendas))
                return agendas
        return {"message": "Sorry this contact does not exist"}


class Contact(Resource):

    def get(self, name):
        agenda = next(
            filter(lambda contact: contact["agenda_name"] == name, agendas), None)
        if agenda:
            return agenda["agenda_contact"]
        else:
            return {"message": "Sorry this contact does not exist"}

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("name",
                            type=str,
                            required=True,
                            help="Somethin went wrong please check name")
        parser.add_argument("address",
                            type=str,
                            required=True,
                            help="Somethin went wrong please check addres")
        parser.add_argument("phoneN",
                            type=int,
                            required=True,
                            help="Somethin went wrong please check phone number")
        data = parser.parse_args()
        data.update({"id": str(uuid.uuid4())}),
        agenda = next(
            filter(lambda agenda: agenda["agenda_name"] == name, agendas), None)
        if agenda:
            contact = next(filter(
                lambda contact: contact["name"] == data["name"], agenda["agenda_contact"]), None)
            if contact:
                return {"message": "Sorry contact already exist"}
            else:
                agenda["agenda_contact"].append(data)
                return agenda
        else:
            return {"message": "Sorry this agenda does not exist"}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("name",
                            type=str,
                            required=True,
                            help="Somethin went wrong please check name")
        parser.add_argument("address",
                            type=str,
                            required=True,
                            help="Somethin went wrong please check addres")
        parser.add_argument("phoneN",
                            type=int,
                            required=True,
                            help="Somethin went wrong please check phone number")
        parser.add_argument("id",
                            type=str,
                            required=True,
                            help="Please provide an id to update contact")
        data = parser.parse_args()
        agenda = next(
            filter(lambda agenda: agenda["agenda_name"] == name, agendas), None)
        if agenda:
            contact = next(filter(
                lambda contact: contact["id"] == data["id"], agenda["agenda_contact"]), None)
            if contact:
                contact.update(data)
                return contact
            else:
                return {"message": "Sorry no contact was found with that id "}
        else:
            return {"message": "Sorry this agenda does not exist"}


api.add_resource(Agenda_List, '/agenda')
api.add_resource(Agenda, '/agenda/<string:name>')
api.add_resource(Contact, '/agenda/<string:name>/contact')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
