from models import Ticket
from views.base import BaseView
from views.model_parameters import GlobalParameters as g
import numpy as np


class TicketView(BaseView):
    __model__ = Ticket

    def __init__(self, id):
        super().__init__()
        self.ticket = self.__model__.query.filter_by(id=id).first()
