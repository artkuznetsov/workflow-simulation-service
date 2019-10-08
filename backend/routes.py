from datetime import datetime

from flask import Flask, request, Response, stream_with_context
from flask_classful import FlaskView, route

from models import *
from views.simulation import SimulationWrapper
import asyncio
import threading

app = Flask(__name__)

# api_v1 = Blueprint("api_v1", __name__)


class ModelView(FlaskView):
    __abstract__ = True
    __model__ = BaseModel
    route_prefix = 'api/v1/'

    def index(self):
        response = jsonify(self.__model__.filter(**request.args))
        return app.make_response(response)

    def get(self, id: int):
        return app.make_response(jsonify(self.__model__.filter(id=id)))

    def post(self):
        entity = self.__model__(**request.json)
        print("AFTER CREATING IN DB WE HAVE SELF AS ", entity.id)

        return app.response_class(
            status=201,
            mimetype='application/json'
        )

    @route('/<id>', methods=['PUT', 'PATCH'])
    def patch(self, id):
        self.__model__.patch(id, **request.json)

        return app.response_class(
            status=200,
            mimetype='application/json'
        )

    def delete(self, id):
        self.__model__.delete(id)
        return app.response_class(
            status=200,
            mimetype='application/json'
        )


class BoardView(ModelView):
    __model__ = Board


class ColumnView(ModelView):
    __model__ = Column


class ComplexityView(ModelView):
    __model__ = Complexity


class ComponentView(ModelView):
    __model__ = Component


class EmployeeView(ModelView):
    __model__ = Employee


class PriorityView(ModelView):
    __model__ = Priority


class ProjectView(ModelView):
    __model__ = Project


class ReleaseView(ModelView):
    __model__ = Release


class RoleView(ModelView):
    __model__ = Role


class StatusView(ModelView):
    __model__ = Status


class SubtaskView(ModelView):
    __model__ = Subtask


class TicketView(ModelView):
    __model__ = Ticket


class SimulationView(ModelView):
    __model__ = Simulation

    def post(self):
        simulation = self.__model__(**request.json)
        simulation = SimulationWrapper(simulation)
        simulation_thread = threading.Thread(target=simulation.run_simulation, args=[request.json['until']])
        simulation_thread.daemon = True
        simulation_thread.start()

        return app.response_class(
            status=200,
            mimetype='application/json'
        )

