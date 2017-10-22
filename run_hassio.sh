CONFIG_PATH=/data/options.json

DATABASE_FILE="$(jq --raw-output '.db_file' $CONFIG_PATH)" 
MQTT_BROKER_URL="$(jq --raw-output '.mqtt_broker' $CONFIG_PATH)"  
MQTT_BROKER_PORT="$(jq --raw-output '.mqtt_port' $CONFIG_PATH)"   
MQTT_USERNAME="$(jq --raw-output '.mqtt_username' $CONFIG_PATH)"   
MQTT_PASSWORD="$(jq --raw-output '.mqtt_password' $CONFIG_PATH)"
export SQLALCHEMY_DATABASE_URI MQTT_BROKER_URL MQTT_BROKER_PORT MQTT_USERNAME MQTT_PASSWORD
python run.py   