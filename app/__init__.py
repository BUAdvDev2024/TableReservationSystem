from flask import Flask, request, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from app.config import Config
from flask_admin.contrib.sqla import ModelView
import logging
import sys

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(filename='app/logs/service.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = SQLAlchemy(app)
# db.Model.metadata.reflect(db.engine)
migrate = Migrate(app, db)
admin = Admin(app, name='TableReservationSystem', template_mode='bootstrap4')
#Admin views go here 

from app.models import Seating, Booking_slots #, bookings
# Add model views here

# Add the models to the admin interface
admin.add_view(ModelView(Seating, db.session))
admin.add_view(ModelView(Booking_slots, db.session))
#admin.add_view(ModelView(bookings, db.session))


from app import routes, models