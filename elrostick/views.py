from elrostick import app, db, mqtt
from elrostick.models import Outlets
from elrostick.forms import OutletForm
from flask import render_template, redirect, session, flash, url_for, jsonify, request, make_response
from functools import wraps
from sqlalchemy import Integer, cast
import subprocess
from logging import log

#vars
prefix = '/home/elroswitches/'
#helpers

def turn_on(channel,unit):
    cmd = [ './rc_switch.sh', 'on' , channel, unit]
    res = subprocess.Popen(cmd,shell=False,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    stdout, stderr = res.communicate()
    app.logger.info("output from rc_switch.sh: %s" % stdout)

def turn_off(channel,unit):
    cmd = [ './rc_switch.sh', 'off' , channel, unit]
    res = subprocess.Popen(cmd,shell=False,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    stdout , stderr = res.communicate()
    app.logger.info("output from rc_switch.sh: %s" % stdout)

def subscribe_topics():
    mqtt.unsubscribe_all()
    outlets = Outlets.query.all()
    for outlet in outlets:
        topic = prefix + outlet.name
        mqtt.subscribe(topic)
        app.logger.info('subscribing to topic %s' % topic )

@mqtt.on_message()
def on_message(client,userdata,message):
    topic = message.topic
    payload = message.payload.decode()
    switch_name = topic.replace(prefix,'')
    outlet = Outlets.query.filter_by(name=switch_name).first()
    if payload == "ON":
        app.logger.info('turning on outlet :%s via mqtt' % outlet.name)
        turn_on(outlet.channel,outlet.unit)
    else:
        app.logger.info('turning off outlet :%s via mqtt' % outlet.name)
        turn_off(outlet.channel,outlet.unit)
    

# views #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/outlets')
def show_outlets():
    outlets = Outlets.query.all()
    return render_template('outlets.html',outlets=outlets)


@app.route('/outlets/add', methods=['get', 'post'])
def add_outlet():
    form = OutletForm()
    if form.validate_on_submit():
        outlet = Outlets()
        outlet.name = form.name.data
        outlet.channel = form.channel.data
        outlet.unit = form.unit.data
        db.session.add(outlet)
        db.session.commit()    
        flash('Outlet added')
        #refresh subscribed topics
        subscribe_topics()
        return redirect(url_for('show_outlets'))
        
    return render_template('outlet_add.html', form=form)

@app.route('/outlets/remove/<int:id>')
def remove_outlet(id):
    outlet = Outlets.query.filter_by(id=id).first()
    db.session.delete(outlet)
    db.session.commit()
    flash('Outlet %s deleted' % outlet.name)
    subscribe_topics()
    return redirect(url_for('show_outlets'))

@app.route('/outlets/turn_on/<int:id>')
def turn_on_view(id):
    outlet = Outlets.query.filter_by(id=id).first()
    turn_on(outlet.channel,outlet.unit)
    flash("Outlet %s turned on" % outlet.name)
    return redirect((url_for('show_outlets')))

@app.route('/outlets/turn_off/<int:id>')
def turn_off_view(id):
    outlet = Outlets.query.filter_by(id=id).first()
    turn_off(outlet.channel,outlet.unit)
    flash("Outlet  %s  turned off" % outlet.name)
    return redirect((url_for('show_outlets')))

