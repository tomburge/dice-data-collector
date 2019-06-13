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
from celery import Celery

# my imports
from vrops import pull_data_from_vrops, get_list_of_json_files
from push_to_dice import dice_transmit

application = Flask(__name__)
application.config['SECRET_KEY'] = 'supersecretkey'

# celery config
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery initialization
celery = Celery(application.name, broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)


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

@application.route("/", methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@application.route("/vrops-connect", methods=["GET","POST"])
def vrops_connect():
    if request.method == "POST":
        vropshost = request.form.get('vropshost')
        vropsuser = request.form.get('vropsuser')
        vropspass = request.form.get('vropspass')
        customer_id = request.form.get('customer_id')
        response = pull_data_from_vrops(vropshost, vropsuser, vropspass, customer_id)
        dice_file = 'dice_vrops_output_' + str(datetime.date.today()) + '.json'
        with open('static/json/' + dice_file, 'w') as j:
            json.dump(response, j, indent=4)
        return redirect('get-json')

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
    application.run(host="0.0.0.0", port=5000)