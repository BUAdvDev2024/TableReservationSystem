from flask import Flask, request, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
import logging
import sys

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(filename='app/logs/service.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = SQLAlchemy(app)
# db.Model.metadata.reflect(db.engine)
migrate = Migrate(app, db)

from app import routes, models