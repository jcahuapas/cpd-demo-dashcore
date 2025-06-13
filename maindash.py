import dash
import dash_bootstrap_components as dbc
import pandas as pd
######LOGIN #######
import os
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config
#########

my_app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.MATERIA, 
                          dbc.icons.FONT_AWESOME,
                          dbc.icons.BOOTSTRAP,
                          'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'],
    meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]                                
)
my_app.title = "DEMO-MBD"
server = my_app.server


color_in_graf_global = '#F3F3F3'
color_out_graf_global = '#F3F3F3'

# import the dataset
url = "https://raw.githubusercontent.com/mnguyen0226/two_sigma_property_listing/main/data/train.json"
df = pd.read_json(url)

###LOGIN#
# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False    
)

db.init_app(server)

# Create User class with UserMixin
class User(UserMixin, base):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

###