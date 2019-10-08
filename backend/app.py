from routes import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=False)
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'workflowsimulation',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

# app.register_blueprint(api_v1, url_prefix='/api/v1/')
BoardView.register(app)
ColumnView.register(app)
ComplexityView.register(app)
ComponentView.register(app)
EmployeeView.register(app)
PriorityView.register(app)
ProjectView.register(app)
ReleaseView.register(app)
RoleView.register(app)
SubtaskView.register(app)
TicketView.register(app)
SimulationView.register(app)
TicketTypeView.register(app)

if __name__ == '__main__':
    app.run()
