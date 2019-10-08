from datetime import datetime

import simpy as simpy

from models import *
from views.base import BaseView

from views.employee import EmployeeView
from views.board import BoardView


class SimulationWrapper(BaseView):
    def __init__(self, simulation):
        super().__init__()
        self.env = simpy.Environment()
        self.start_time = None
        self.dow = 1
        self.simulation = simulation

    def run(self, until):
        self.start_time = datetime.now()

        self.env.process(self.increase_growth_backlog())
        # self.env.process(self.development())

        self.env.process(self.time())

        self.env.run(until=until)
        print(f'End of simulation {self.simulation.id}')

    @staticmethod
    def _get_employee_by(**kwargs):
        from app import app
        with app.app_context():
            return [EmployeeView(id=employee.id) for employee in Employee.query.filter_by(**kwargs).all()]

    def increase_growth_backlog(self):
        from app import app
        with app.app_context():
            board = BoardView(id=self.simulation.board_id)
            column = Column.query.filter_by(board=board.id, name='BACKLOG').first()
        while True:
            for product_owner in self._get_employee_by(role=2):
                self.env.process(product_owner.increase_growth_backlog(column))
            yield self.env.timeout(1)

    # def development(self):
    #     while True:
    #         board = BoardView(id=self.simulation.board_id)
    #         search_tickets_at = Column.query.filter_by(board=board.id, name='SELECTED FOR DEVELOPMENT')
    #         for developer in self._get_employee_by(role=3):
    #             self.env.process(developer.development(board))
    #         yield self.env.timeout(1)

    def time(self):
        while True:
            yield self.env.timeout(8)
            print(f"Day of the week is {self.dow}\n\n")
            self.dow = self.dow + 1
            if self.dow == 7:
                self.dow = 1

