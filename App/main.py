import os
from flask import Flask
#from wtforms import StringField,SubmitField, PasswordField, BooleanField, ValidationError,EmailField, DecimalField, SelectField,IntegerField,FloatField
#from wtforms.validators import DataRequired, EqualTo, Length
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
#from flask_wtf import FlaskForm
#from wtforms.validators import InputRequired, Email ,Length
from flask import jsonify

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///temp-database.db'
app.config['SECRET_KEY']='secret key'

db=SQLAlchemy(app)

from App.database import create_db



#Login Setup
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)






from App.controllers import (
    setup_jwt
)

from App.views import (
    user_views,
    index_views,
    student_views,
    staff_views,
    notification_views,
    recommendation_views,
)


# New views must be imported and added to this list

views = [
    user_views,
    index_views,
    student_views,
    staff_views,
    notification_views,
    recommendation_views
]



def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        delta = app.config['JWT_EXPIRATION_DELTA']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        delta = os.environ.get('JWT_EXPIRATION_DELTA', 7)
        
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=int(delta))
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    setup_jwt(app)
    app.app_context().push()
    return app



#@app.route('/signup',methods=['GET','POST'])
#def signup():
 #   form=SignUpForm()
  #  if form.validate_on_submit():
   #     user=User.query.filter_by(email=form.email.data).first()
    #    if user is None:
     #      newUser=User(firstName=form.firstName.data,lastName=form.lastName,email=form.email.data,password=form.password.data,)
      #     newUser.set_password(newUser.password)
       # db.session.add(newUser)
        #db.session.commit()
        #form.username.data=''
        #form.email.data=''
        #return redirect(url_for('index'))
    #return render_template('signup.html',form=form)

#@app.route('/login',methods=['POST','GET'])
#def login():
 #   form=LoginForm()
  #  if form.validate_on_submit():
   #     user=User.query.filter_by(email=form.email.data).first()
    #    if user:
     #       if check_password_hash(user.password, form.password.data):
      #          login_user(user)
       #         flash("Logged In Successful")
        #        return redirect(url_for('index'))
         #   else:
          #      flash("Incorrect Password")
    #return render_template('login.html',form=form)