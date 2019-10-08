from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import Employee, Ticket
from views.base import BaseView
from views.model_parameters import GlobalParameters as g
import numpy as np

app = Flask(__name__)
db = SQLAlchemy(app)


class EmployeeView(BaseView):
    __model__ = Employee

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employees = self.__model__.query.filter_by(**kwargs).all()

    # def start_to_work(self, ticket, direct):
    #     if ticket.type in g.subtask_types:
    #         ticket.move_on(direct)
    #     else:
    #         ticket.move_on(direct, self.board.board)
    #
    #     ticket.assigned_to = self.uuid
    #     print(self.board.board)
    #
    # def search_ticket(self):
    #     pass
    #
    # def review(self):
    #     def _review_ticket(ticket):
    #         pass
    #
    #     pass
    #
    # def development(self):
    #     def _development(ticket):
    #         pass
    #
    #     pass
    #
    #     def _get_development_time(ticket):
    #         pass
    #
    # def testing(self, employee):
    #     while True:
    #         if employee.release_master and g.dow in (1, 4) and g.last_release_day != g.dow:
    #             g.env.process(self.release())
    #             yield g.env.timeout(24)
    #
    # for ticket in self.board.board.tickets['IN QA']:
    #     if ticket.assigned_to == self.uuid:
    #         yield g.env.timeout(self.get_testing_time(ticket))
    #
    #         bug = self._bug(ticket)
    #
    #         if bug['is_found']:
    #             yield g.env.timeout(0.5)
    #             self._register_bug(ticket, bug['component'])
    #         else:
    #             self._testing_pass(ticket)
    #
    # if self.board.board.tickets['READY FOR QA']:
    #     for ticket in self.board.board.tickets['READY FOR QA']:
    #         if ticket.type in g.ticket_types:
    #             for subtask in ticket.subtasks:
    #                 if subtask.type == 'Completion blocker' and subtask.status == 'READY FOR QA':
    #                     ticket = subtask
    #                     break
    #
    #         self._start_to_work(ticket)
    #
    #         yield g.env.timeout(self.get_testing_time(ticket))
    #
    #         bug = self._bug(ticket)
    #
    #         if bug['is_found']:
    #             yield g.env.timeout(0.5)
    #             self._register_bug(ticket, bug['component'])
    #         else:
    #             self._testing_pass(ticket)
    # else:
    #     """QA CAN"T FIND CARDS FOR WORK: HE/SHE SPEND 30 MINUTES TO ANY OTHER WORK (TEST CASES, REGRESSION AND SO ON)"""
    #     print("QA don't have any tickets for testing... He/she will work under process issues...")
    # yield g.env.timeout(0.5)
    # g.free_time_qa += 0.5
    # return
    # def _get_testing_time(ticket):
    #     pass
    #
    # def is_bug_found(ticket):
    #     pass
    #
    # def _bug_report(ticket, bug):
    #     pass
    #
    # def _testing_pass(ticket):
    #     pass
    #
    # def uat(self):
    #     pass
    #
    #     def _uat_pass(self, ticket):
    #         pass
    #
    # def move_all_tickets(self, source, destination):
    #     pass
    #
    #

    def increase_growth_backlog(self):
        while True:
            ticket_complexity = np.random.choice(g.complexity_types, 1,
                                                 p=[0.1, 0.3, 0.4, 0.15, 0.05])[0].copy()

            ticket_type = np.random.choice(g.ticket_types, 1,
                                           p=[0.47, 0.43, 0.05, 0.05])[0].copy()

            ticket_priority = np.random.choice(g.ticket_priority, 1,
                                               p=[0.15, 0.41, 0.38, 0.06])[0].copy().__int__()
            ticket_components = []
            while not ticket_components:
                ticket_components = np.random.choice(g.components, 1, p=[0.13, 0.16, 0.34, 0.2, 0.03, 0.08, 0.06])[
                    0].copy()

            ticket = Ticket(complexity=1,
                            type=1,
                            priority=1,
                            components=1,
                            status=1)

            # self.board.tickets.append(ticket)
            # g.stat_backlog['created']['total'] += 1

            # print(f'\n\nPO have create a new ticket in {ticket.status} with are following parameters:\n'
            #       f'Type: {ticket.type}\n'
            #       f'Priority: {ticket.priority}\n'
            #       f'Complexity: {ticket.complexity}\n'
            #       f'Components: {ticket.components}\n\n'
            #       f'Current time is {g.env.now}\n\n')

            yield g.env.timeout(1)
        return
    #
    # def release(self):
    #     pass
