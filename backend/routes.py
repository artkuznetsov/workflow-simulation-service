from flask import Flask, request
from flask_classful import FlaskView, route

from models import *
from views.simulation import SimulationWrapper
import threading


class ModelView(FlaskView):
    __abstract__ = True
    __model__ = BaseModel
    route_prefix = 'api/v1/'

    def index(self):
        from app import app
        with app.app_context():
            response = jsonify(self.__model__.filter(**request.args))
        return app.make_response(response)

    def get(self, id: int):
        from app import app
        with app.app_context():
            return app.make_response(jsonify(self.__model__.filter(id=id)))

    def post(self):
        from app import app
        with app.app_context():
            self.__model__(**request.json)

            return app.response_class(
                status=201,
                mimetype='application/json'
            )

    @route('/<id>', methods=['PUT', 'PATCH'])
    def patch(self, id):
        from app import app
        with app.app_context():
            self.__model__.patch(id, **request.json)

            return app.response_class(
                status=200,
                mimetype='application/json'
            )

    def delete(self, id):
        from app import app
        with app.app_context():
            self.__model__.delete(id)
            return app.response_class(
                status=200,
                mimetype='application/json'
            )


class SimulationView(ModelView):
    __model__ = Simulation

    def post(self):
        from app import app
        with app.app_context():
            simulation = self.__model__(**request.json)
            simulation = SimulationWrapper(simulation)
            simulation_thread = threading.Thread(target=simulation.run, args=[request.json['until']])
            simulation_thread.daemon = True
            simulation_thread.start()

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


class TicketTypeView(ModelView):
    __model__ = TicketType


