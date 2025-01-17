# from datetime import datetime
# from flask import Flask, request, g, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_admin import Admin
# from app.config import Config
# from flask_admin.contrib.sqla import ModelView
# import logging
# import sys
# import os
# from flask_migrate import upgrade
#
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
# app.config.from_object(Config)
#
# logging.basicConfig(filename=os.path.join(basedir,'logs/service.log'), level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#
# db = SQLAlchemy(app)
# # db.Model.metadata.reflect(db.engine)
# migrate = Migrate(app, db)
# admin = Admin(app, name='TableReservationSystem', template_mode='bootstrap4')
# #Admin views go here
#
# from app.models import Seating, Booking_slots, bookings, Restaurant, WaitingList
# # Add model views here
#
# # Add the models to the admin interface
# admin.add_view(ModelView(Seating, db.session))
# admin.add_view(ModelView(Booking_slots, db.session))
# admin.add_view(ModelView(bookings, db.session))
# admin.add_view(ModelView(Restaurant, db.session))
# admin.add_view(ModelView(WaitingList, db.session))
#
#
# if not os.path.exists(os.path.join(basedir, 'app.db')):
#     print("Creating database tables...")
#     with app.app_context():
#         db.create_all()  # Use only in development
#         from app.models import populate_booking_slots, add_test_restaurant_and_restaurant_data
#
#         add_test_restaurant_and_restaurant_data()
#         populate_booking_slots()
#
# # Apply migrations on every startup
# with app.app_context():
#     from app.models import populate_booking_slots, add_test_restaurant_and_restaurant_data
#
#     # add_test_restaurant_and_restaurant_data()
#     populate_booking_slots(start_date=datetime.today(),num_days=45)
#     upgrade()
#
# from app import routes, models
#
# if __name__ == "__main__":
#     with app.app_context():
#         import datetime
#         # Populate booking slots for the next 7 days

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from app.config import Config
from flask_admin.contrib.sqla import ModelView
import logging
import os
from flask_migrate import upgrade

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the global objects
db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='TableReservationSystem', template_mode='bootstrap4')

# Function to create and return the app
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    # Logging setup
    if not app.config['TESTING']:
        logging.basicConfig(filename=os.path.join(basedir, 'logs/service.log'), level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    else:
        logging.basicConfig(filename=os.path.join(basedir, 'logs/testsLogs.log'), level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    # Add the models to the admin interface
    from app.models import Seating, Booking_slots, bookings, Restaurant, WaitingList
    admin.add_view(ModelView(Seating, db.session))
    admin.add_view(ModelView(Booking_slots, db.session))
    admin.add_view(ModelView(bookings, db.session))
    admin.add_view(ModelView(Restaurant, db.session))
    admin.add_view(ModelView(WaitingList, db.session))

    # Setup database and models
    with app.app_context():
        if not os.path.exists(os.path.join(basedir, 'app.db')) or app.config['TESTING']:
            print("Creating database tables...")
            db.create_all()  # Use only in development
            from app.models import populate_booking_slots, add_test_restaurant_and_restaurant_data
            add_test_restaurant_and_restaurant_data()
            populate_booking_slots(start_date=datetime.today(),num_days=45)

        # Apply migrations
        # upgrade()

    # # Register routes
    from app.routes import routeBlueprint
    app.register_blueprint(routeBlueprint)

    return app

