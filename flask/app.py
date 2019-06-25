# python standard library imports
import json

# flask imports
from flask import Flask, render_template, redirect, url_for, request, Response, flash
from flask_assets import Bundle, Environment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, InputRequired
from celery import Celery, task

# app imports
from test_connect import test_vrops_connect, test_vcenter_connect
from vrops import pull_data_from_vrops
from vcenter import pull_data_from_vcenter
from general_tasks import dice_transmit, get_list_of_json_files
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
js = Bundle(
    'js/clr-icons.min.js',
    'js/clr-icons-api.js',
    'js/clr-icons-element.js',
    'js/custom-elements.min.js',
    'js/jquery-3.4.1.min.js'
)
env.register('js_all', js)
css = Bundle('css/clr-ui.min.css', 'css/clr-icons.min.css')
env.register('css_all', css)


class LoginForm(FlaskForm):
    host = StringField('Host Address:', validators=[InputRequired(), DataRequired()])
    user = StringField('Username: ', validators=[InputRequired(), DataRequired()])
    pwd = PasswordField('Password: ', validators=[InputRequired(), DataRequired()])
    port = StringField('Port: ', validators=[InputRequired(), DataRequired()])
    customer_id = StringField('Customer ID', validators=[InputRequired(), DataRequired()])
    vrops_connect = HiddenField()
    vcenter_connect = HiddenField()
    submit = SubmitField('Collect')
    test =SubmitField('Test Connection')


class TransmitForm(FlaskForm):
    api_key = StringField('DICE API Key', validators=[InputRequired(), DataRequired()])
    api_secret = StringField('DICE Secret Key', validators=[InputRequired(), DataRequired()])
    json_file = StringField('DICE JSON File ', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Send To DICE')


@celery.task(name='call.vrops.connect')
def call_vrops_connect(vropshost, vropsuser, vropspass, vropsport, customer_id):
    pull_data_from_vrops(vropshost, vropsuser, vropspass, vropsport, customer_id)


@celery.task(name='call.vcenter.connect')
def call_vcenter_connect(vchost, vcuser, vcpass, vcport, customer_id):
    pull_data_from_vcenter(vchost, vcuser, vcpass, vcport, customer_id)


@celery.task(name='push.to.dice')
def transmit_to_dice(api_key, api_secret, json_file):
    api_key = api_key
    api_secret = api_secret
    json_file = json_file
    dice_transmit(api_key, api_secret, json_file)


@celery.task(name='call.test.call')
def test_call():
    test_call = 'test_call was called\n'
    with open('test_call.log', 'a') as j:
        j.write(test_call)


@application.route("/", methods=['GET', "POST"])
def index():
    vrops_form = LoginForm()
    vcenter_form = LoginForm()
    vr_message = ''
    vc_message = ''
    if request.method == "POST":
        if "vrops_connect" in request.form:
            if 'submit' in request.form:
                vropshost = request.form.get('host')
                vropsuser = request.form.get('user')
                vropspass = request.form.get('pwd')
                vropsport = request.form.get('port')
                customer_id = request.form.get('customer_id')
                code = test_vrops_connect(vropshost, vropsuser, vropspass, vropsport)
                if code == 200:
                    celery.send_task('call.vrops.connect', args=(vropshost, vropsuser, vropspass, vropsport, customer_id))
                    return redirect('get-json')
                else:
                    vr_message = 'Connection Failed'
                    return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)
            elif 'test' in request.form:
                vropshost = request.form.get('host')
                vropsuser = request.form.get('user')
                vropspass = request.form.get('pwd')
                vropsport = request.form.get('port')
                code = test_vrops_connect(vropshost, vropsuser, vropspass, vropsport)
                if code == 200:
                    vr_message = 'Connection Successful'
                    return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)
                else:
                    vr_message = 'Connection Failed'
                    return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)
        elif "vcenter_connect" in request.form:
            if 'submit' in request.form:
                vchost = request.form.get('host')
                vcuser = request.form.get('user')
                vcpass = request.form.get('pwd')
                vcport = request.form.get('port')
                customer_id = request.form.get('customer_id')
                code = test_vcenter_connect(vchost, vcuser, vcpass, vcport)
                if code == 200:
                    celery.send_task('call.vcenter.connect', args=(vchost, vcuser, vcpass, vcport, customer_id))
                    return redirect('get-json')
                else:
                    vc_message = 'Connection Failed'
                    return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)
            elif 'test' in request.form:
                vchost = request.form.get('host')
                vcuser = request.form.get('user')
                vcpass = request.form.get('pwd')
                vcport = request.form.get('port')
                code = test_vcenter_connect(vchost, vcuser, vcpass, vcport)
                if code == 200:
                    vc_message = 'Connection Successful'
                    return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)
                else:
                    vc_message = 'Connection Failed'
                    return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)
    else:
        message = ''
        return render_template('index.html', vrops_form=vrops_form, vcenter_form=vcenter_form, vc_message=vc_message, vr_message=vr_message)


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
        celery.send_task('push.to.dice', args=(api_key, api_secret, json_file))
    return redirect('get-json')


@application.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    application.run(host="0.0.0.0")
