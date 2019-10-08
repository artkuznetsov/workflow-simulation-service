from models import Complexity
from views.base import BaseView


class ComplexityView(BaseView):
    __model__ = Complexity

    def __init__(self, id):
        super().__init__()
        self.complexity = self.__model__.query.filter_by(id=id).first()
