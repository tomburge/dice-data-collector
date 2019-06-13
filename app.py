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

# my imports
from vrops import pull_data_from_vrops

application = Flask(__name__)
application.config['SECRET_KEY'] = 'supersecretkey'

env = Environment(application)
js = Bundle('js/clr-icons.min.js', 'js/clr-icons-api.js','js/clr-icons-element.js', 'js/custom-elements.min.js')
env.register('js_all', js)
css = Bundle('css/clr-ui.min.css', 'css/clr-icons.min.css')
env.register('css_all', css)

class LoginForm(FlaskForm):
    vropshost = StringField('vROPs Address:', validators=[InputRequired(), DataRequired()])
    vropsuser = StringField('vROPs Username: ', validators=[InputRequired(), DataRequired()])
    vropspass = PasswordField('vROPs Password: ', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Submit')

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
        response = pull_data_from_vrops(vropshost, vropsuser, vropspass)
        dice_file = 'dice_vrops_output_' + str(datetime.date.today()) + '.json'
        with open('static/json/' + dice_file, 'w') as j:
            json.dump(response, j, indent=4)
        return redirect('get-json')
        
@application.route("/get-json")
def get_json():
    return render_template('json.html')

@application.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)