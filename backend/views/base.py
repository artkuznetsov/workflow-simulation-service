from models import BaseModel


class BaseView:
    __model__ = BaseModel

    def __init__(self, **kwargs):
        [self.__setattr__(key, value) for key, value in kwargs.items()]

    def filter(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs).all()

    def save(self, **args):
        return self.__model__(**args)

    def get(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs).first()
