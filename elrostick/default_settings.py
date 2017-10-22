import os

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.environ.get('DATABASE_FILE', '/data/elrostick.db')
SECRET_KEY = os.environ.get('SECRET_KEY','asdfghjkl')
MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL', None)
MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT', 1883)
MQTT_USERNAME = os.environ.get('MQTT_USERNAME', None)
MQTT_PASSWORD= os.environ.get('MQTT_PASSWORD', None)

