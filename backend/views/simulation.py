from datetime import datetime

import simpy as simpy
from flask import request
from flask_sqlalchemy import SQLAlchemy

from models import Simulation
from views.base import BaseView
from views.board import BoardView
from views.project import ProjectView
from views.employee import EmployeeView
from views.Role import RoleView

# db = SQLAlchemy()


class SimulationWrapper(BaseView):
    def __init__(self, simulation):
        super().__init__()
        self.board = BoardView(id=simulation.board_id)
        self.a = RoleView()
        self.select = self.a.filter(name='Product Owner')
        self.project = ProjectView(id=simulation.project)
        self.employee_view = EmployeeView()
        self.simulation_members = self.employee_view.filter(project=simulation.project, board=simulation.board_id)
        self.env = simpy.Environment()
        self.start_time = None
        self.dow = 1
        self.simulation = simulation
        self.product_owners = []
        self.qas = []

    def get_members_by_role_name(self, role_name):
        role_view = RoleView()
        role = role_view.get(name=role_name)
        employee_view = EmployeeView()
        return employee_view.filter(role=role.id)


        # for member in self.simulation_members:
            # role_id = db.session.query(Role).filter(Role.name == role_name)
            # role_id = Role.query.filter_by(name=role_name).id
            # if member.role == role_id:
            #     member_view = EmployeeView(id=member.id)
            #     array.append(member_view)

        return array

    def run_simulation(self, until):
        self.start_time = datetime.now()

        self.env.process(self.increase_growth_backlog())
        # self.env.process(self.development())
        # self.env.process(self.testing())
        # self.env.process(self.uat())
        self.env.process(self.time())

        # self.simulation.patch(cls=Simulation, id=self.simulation.id, status='STARTED')
        self.env.run(until=until)

    # def save(self):
    #     return self.__model__(start_date=self.start_time,
    #                           status='STARTED',
    #                           board_id=self.board.id,
    #                           employee_ids=[employee.id for employee in self.employees],
    #                           project=self.project
    #                           )

    # def testing(self):
    #     while True:
    #         for employee in self.employees:
    #             if employee.role is 1:
    #                 self.env.process(self.employee_view.testing(employee))
    #         yield self.env.timeout(1000000)
    #
    # def uat(self):
    #     while True:
    #         [self.env.process(employee.uat()) for employee in self.employees]
    #         yield self.env.timeout(1000000)
    #
    # def release(self):
    #     while True:
    #         [self.env.process(employee.release()) for employee in self.employees]
    #         yield self.env.timeout(1000000)
    #
    def increase_growth_backlog(self):
        while True:
            for po in self.get_members_by_role_name(role_name='Product Owner'):
                self.env.process(po.increase_growth_backlog())
            # for member in self.simulation_members:
            #     if member.role == Role.query.filter_by(name='Product Owner').id:
            #         product_owners = EmployeeView(id=member.id)
            #         employee_view.increase_growth_backlog()
            # [self.env.process(EmployeeView(employee.id).increase_growth_backlog(employee.id)) for employee in self.simulation_members]
            yield self.env.timeout(1000000)
    #
    # def development(self):
    #     while True:
    #         [self.env.process(employee.development()) for employee in self.employees]
    #         yield self.env.timeout(1000000)
    #
    def time(self):
        while True:
            yield self.env.timeout(24)
            print(f"Day of the week is {self.dow}\n\n")
            self.dow = self.dow + 1
            if self.dow == 7:
                self.dow = 1

