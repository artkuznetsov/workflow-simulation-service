from models import Employee, Ticket, Complexity, TicketType, Priority, Component, Column, Status
from views.base import BaseView
from views.board import BoardView
from views.column import ColumnView
from views.ticket import TicketView
from views.complexity import ComplexityView
from views.status import StatusView
from views.model_parameters import GlobalParameters as g
import numpy as np


class EmployeeView(BaseView):
    __model__ = Employee

    def __init__(self, id):
        super().__init__()
        self.employee = self.__model__.query.filter_by(id=id).first()

    @staticmethod
    def increase_growth_backlog(column: Column):
        while True:
            from app import app
            with app.app_context():
                ticket_complexity = np.random.choice(Complexity.query.all(), 1, p=[0.1, 0.3, 0.4, 0.15, 0.05])[0]
                ticket_type = np.random.choice(TicketType.query.all(), 1, p=[0.47, 0.43, 0.05, 0.05])[0]
                ticket_priority = np.random.choice(Priority.query.all(), 1, p=[0.15, 0.41, 0.38, 0.06])[0]
                status = Status.query.filter_by(name=column.name).first()
                ticket_components = np.random.choice(Component.query.all(), np.random.randint(1, 3), p=[0.5, 0.25, 0.25])

                Ticket(complexity=ticket_complexity.id,
                       type=ticket_type.id,
                       priority=ticket_priority.id,
                       status=status.id,
                       column_id=column.id,
                       components=[component for component in ticket_components])

            yield g.env.timeout(1)
        return

    # def development(self):
    #     while True:
    #         """START TO WORK"""
    #         yield g.env.timeout(0.25)
    #         """START TO WORK: SEARCH TICKET"""
    #         ticket_selected = self._search_ticket()
    #     return

    # def _search_ticket(self):
    #     for ticket in
    #     for ticket in self.board.board.tickets['SELECTED FOR DEVELOPMENT']:
    #         for ticket_component in ticket.components:
    #             if ticket_component in self.components:
    #                 if ticket.type == g.subtask_types:
    #
    #                     """TAKE COMPLETION BLOCKER"""
    #                     self.start_to_work(ticket, 'IN DEV')
    #                     return True
    #                 elif ticket.type in g.subtask_types:
    #
    #                     """TAKE SUB-TASK"""
    #                     self.start_to_work(ticket, 'IN DEV')
    #                     return True
    #                 elif ticket.type == 'Feature':
    #
    #                     """TAKE FEATURE"""
    #                     self.start_to_work(ticket, 'IN ANALYSIS')
    #                     ticket.move_on('IN ANALYSIS', self.board.board)
    #                     return True
    #                 else:
    #
    #                     """TAKE TASK, DECHNICAL DEBT AND OTHER PARENT CARD"""
    #                     self.start_to_work(ticket, 'IN DEV')
    #                     return True
    #     return False