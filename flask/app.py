#!/usr/bin/env python
# python standard library imports
import json
import datetime

#python flask imports
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_assets import Bundle, Environment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired
from celery import Celery, task

<<<<<<< Updated upstream
# my imports
from vrops import pull_data_from_vrops, get_list_of_json_files
from push_to_dice import dice_transmit
=======
# app imports
from test_connect import test_vrops_connect, test_vcenter_connect
from vrops import pull_data_from_vrops
from vcenter import pull_data_from_vcenter
from general_tasks import dice_transmit, get_list_of_json_files
>>>>>>> Stashed changes
import config

# ---------------------------------------------------------------------------------

# initialize flask app
application = Flask(__name__)
application.config['SECRET_KEY'] = 'supersecretkey'

# celery config
application.config.from_object('config')

# celery initialization
celery = Celery(
    application.import_name,
    backend=application.config['CELERY_RESULT_BACKEND'],
    broker=application.config['CELERY_BROKER_URL']
)
celery.conf.update(application.config)


# environment config
env = Environment(application)
js = Bundle('js/clr-icons.min.js', 'js/clr-icons-api.js','js/clr-icons-element.js', 'js/custom-elements.min.js')
env.register('js_all', js)
css = Bundle('css/clr-ui.min.css', 'css/clr-icons.min.css')
env.register('css_all', css)

class LoginForm(FlaskForm):
    vropshost = StringField('vROPs Address:', validators=[InputRequired(), DataRequired()])
    vropsuser = StringField('vROPs Username: ', validators=[InputRequired(), DataRequired()])
    vropspass = PasswordField('vROPs Password: ', validators=[InputRequired(), DataRequired()])
    customer_id = StringField('Customer ID', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Submit')

class TransmitForm(FlaskForm):
    api_key = StringField('DICE API Key', validators=[InputRequired(), DataRequired()])
    api_secret = StringField('DICE Secret Key', validators=[InputRequired(), DataRequired()])
    json_file = StringField('DICE JSON File ', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Send To DICE')

@celery.task(name='call.vrops.connect')
def call_vrops_connect(vropshost, vropsuser, vropspass, customer_id):
    pull_data_from_vrops(vropshost, vropsuser, vropspass, customer_id)


@celery.task(name='call.vrops.test')
def call_vrops_test(vropshost, vropsuser, vropspass):
    code = test_vrops_connect(vropshost, vropsuser, vropspass)
    if code == 200:
        print('success')
    else:
        print('failure')

<<<<<<< Updated upstream
=======

@celery.task(name='call.vcenter.connect')
def call_vcenter_connect(vchost, vcuser, vcpass, customer_id):
    pull_data_from_vcenter(vchost, vcuser, vcpass, customer_id)


@celery.task(name='call.vcenter.test')
def call_vcenter_test(vchost, vcuser, vcpass):
    code = test_vcenter_connect(vchost, vcuser, vcpass)
    if code == 200:
        print('success')
    else:
        print('failure')


@celery.task(name='push.to.dice')
def transmit_to_dice(api_key, api_secret, json_file):
    api_key = api_key
    api_secret = api_secret
    json_file = json_file
    dice_transmit(api_key, api_secret, json_file)


>>>>>>> Stashed changes
@celery.task(name='call.test.call')
def test_call():
    test_call = 'test_call was called\n'
    with open('test_call.log', 'a') as j:
        j.write(test_call)

@application.route("/", methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@application.route("/vrops-connect", methods=["GET","POST"])
def vrops_connect():
    if request.method == "POST":
<<<<<<< Updated upstream
        vropshost = request.form.get('vropshost')
        vropsuser = request.form.get('vropsuser')
        vropspass = request.form.get('vropspass')
        customer_id = request.form.get('customer_id')
        celery.send_task('call.vrops.connect', args=(vropshost, vropsuser, vropspass, customer_id))
        return redirect('get-json')
=======
        if 'submit' in request.form:
            vropshost = request.form.get('host')
            vropsuser = request.form.get('user')
            vropspass = request.form.get('pwd')
            customer_id = request.form.get('customer_id')
            celery.send_task('call.vrops.connect', args=(vropshost, vropsuser, vropspass, customer_id))
            return redirect('get-json')
        elif 'test' in request.form:
            vropshost = request.form.get('host')
            vropsuser = request.form.get('user')
            vropspass = request.form.get('pwd')
            celery.send_task('call.vrops.test', args=(vropshost, vropsuser, vropspass))
            return redirect('get-json')
            

@application.route("/vcenter-connect", methods=["GET","POST"])
def vcenter_connect():
    if request.method == "POST":
        if 'submit' in request.form:
            vchost = request.form.get('host')
            vcuser = request.form.get('user')
            vcpass = request.form.get('pwd')
            customer_id = request.form.get('customer_id')
            celery.send_task('call.vcenter.connect', args=(vchost, vcuser, vcpass, customer_id))
            return redirect('get-json')
        elif 'test' in request.form:
            vchost = request.form.get('host')
            vcuser = request.form.get('user')
            vcpass = request.form.get('pwd')
            celery.send_task('call.vcenter.test', args=(vchost, vcuser, vcpass))
            return redirect('get-json')

>>>>>>> Stashed changes

@application.route("/example")
def example():
    with open('static/example/example.json', 'r') as j:
        json_example = json.load(j)
    return render_template('example.html', json_example=json_example)

@application.route("/get-json")
def get_json():
    form = TransmitForm()
    files = get_list_of_json_files()
    return render_template('json.html', form=form, files=files)

@application.route("/transmit-data", methods=["GET","POST"])
def transmit_data():
    if request.method == "POST":
        api_key = request.form.get('api_key')
        api_secret = request.form.get('api_secret')
        json_file = request.form.get('json_file')
        response = dice_transmit(api_secret, api_secret, json_file)
    return redirect('get-json')

@application.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0")
