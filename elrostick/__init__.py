import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
from flask_bootstrap import Bootstrap


app = Flask(__name__)
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

app.config.from_object('elrostick.default_settings')
if app.config['SQLALCHEMY_DATABASE_URI'] is None:
    raise Exception('app database not configured')
if app.config['MQTT_BROKER_URL'] is None:
    raise Exception('mqtt broker not configured')
if app.config['MQTT_USERNAME'] is None:
    raise Exception('mqtt user not configured')
if app.config['MQTT_PASSWORD'] is None:
    raise Exception('mqtt password not configured')

app.logger.info('running config:')
for config in app.config.keys():
    app.logger.info('NAME: %s VALUE:%s' % (config,app.config[config]))



db = SQLAlchemy(app)
mqtt = Mqtt(app)
Bootstrap(app)

import elrostick.models
import elrostick.views
import elrostick.forms
#hack
if 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI']:
    db_file = app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///","")
    if not os.path.exists(db_file):
        db.create_all()
elrostick.views.subscribe_topics()