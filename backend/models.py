import json

from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, Integer
from sqlalchemy.inspection import inspect

db = SQLAlchemy()


def get_all(model):
    return jsonify([model.as_dict() for model in model.query.all()])


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return json.dumps([m.serialize() for m in l])


class BaseModel(db.Model, Serializer):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, **args):
        [self.__setattr__(key, value) for key, value in args.items()]
        super().__init__(**args)
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        print(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def filter_by_id(cls, id):
        return db.session.query(cls).get(id)

    @classmethod
    def filter(cls, **kwargs):
        array = []
        for item in cls.query.filter_by(**kwargs).all():
            array.append(item.as_dict())

        return array

    @classmethod
    def delete(cls, id):
        try:
            cls.query.filter_by(id=id).delete()
            db.session.commit()
        except Exception as e:
            raise Exception(f"""Can't delete an entity. Make sure that id is correct. Stacktrace is {e}""")

    @classmethod
    def patch(cls, id, **args):
        obj = cls.query.filter_by(id=id).first()
        [obj.__setattr__(key, value) for key, value in args.items()]
        db.session.add(obj)
        db.session.commit()


class Board(BaseModel):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


ticket_component = db.Table('ticket_component',
                            db.Column('ticket_id', db.Integer, db.ForeignKey('tickets.id'), primary_key=True),
                            db.Column('component_id', db.Integer, db.ForeignKey('components.id'), primary_key=True))


class Component(BaseModel):
    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Subtask(BaseModel):
    __tablename__ = 'subtasks'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)


class Ticket(BaseModel):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.ForeignKey('priorities.id'))
    complexity = db.Column(db.ForeignKey('complexities.id'))
    components = db.relationship(Component, secondary=ticket_component, lazy='subquery',
                                 backref=db.backref('tickets', lazy=True))
    status = db.Column(db.ForeignKey('statuses.id'))
    fix_version = db.Column(db.ForeignKey('releases.id'))
    assigned_to = db.Column(db.ForeignKey('employees.id'))
    subtasks = db.relationship(Subtask, backref='parent', lazy=True)
    is_present = db.Column(db.Boolean)
    column_id = db.Column(db.Integer, db.ForeignKey('columns.id'), nullable=False)
    content = db.Column(db.String)
    priority = db.Column(db.ForeignKey('priorities.id'))


class Column(BaseModel):
    __tablename__ = 'columns'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    max_size = db.Column(db.Integer)
    min_size = db.Column(db.Integer)
    count = db.Column(db.Integer)
    board = db.Column(db.ForeignKey('boards.id'))
    tickets = db.relationship(Ticket, backref='column', lazy=True)
    order = db.Column(db.Integer)

    UniqueConstraint('board', 'order')


class Priority(BaseModel):
    __tablename__ = 'priorities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Complexity(BaseModel):
    __tablename__ = 'complexities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Status(BaseModel):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Release(BaseModel):
    __tablename__ = 'releases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Project(BaseModel):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


employee_component = db.Table('employee_component',
                              db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True),
                              db.Column('component_id', db.Integer, db.ForeignKey('components.id'), primary_key=True))


class Employee(BaseModel):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.ForeignKey('roles.id'))
    project = db.Column(db.ForeignKey('projects.id'))
    experience = db.Column(db.Integer)
    available_working_hours = db.Column(db.Float)
    board = db.Column(db.ForeignKey('boards.id'))
    release_master = db.Column(db.Boolean)
    components = db.relationship(Component, secondary=employee_component, lazy='subquery',
                                 backref=db.backref('employees', lazy=True))
    wip = db.Column(db.Boolean)
    backlog_inc_frequency = db.Column(db.Integer)


class Role(BaseModel):
    __tablename__ = 'roles' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Simulation(BaseModel):
    __tablename__ = 'simulations'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    end_date = db.Column(db.DateTime)
    metrics = db.Column(db.JSON)
    board_id = db.Column(db.ForeignKey('boards.id'))
    employee_ids = db.Column(db.ARRAY(item_type=Integer))
    project = db.Column(db.ForeignKey('projects.id'))
    until = db.Column(db.Integer)
