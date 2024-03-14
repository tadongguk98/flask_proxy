import json

from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'juhcnjKSACKL'

class SimpleFrom(FlaskForm):
    submit = SubmitField('Submit')
    key = StringField('Enter your Tinsoft key: ', validators= [DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SimpleFrom()
    if form.validate_on_submit():

        session['proxy'] = form.key.data
        proxy = get_proxy(session['proxy'])
        flash(f'Your proxy : {proxy}')
        return redirect(url_for('index'))


    return render_template('proxy.html', form=form)
def get_proxy(api):


    res_cur = requests.get(f"http://proxy.tinsoftsv.com/api/getProxy.php?key={api}")
    time_change = json.loads(res_cur.text).get('next_change')
    if time_change == 0 or time_change == None:

        res_new = requests.get(f"http://proxy.tinsoftsv.com/api/changeProxy.php?key={api}&location=0")
        new_ip = json.loads(res_new.text).get('proxy')
    else:

        res_new = requests.get(f"http://proxy.tinsoftsv.com/api/getProxy.php?key={api}")
        new_ip = json.loads(res_new.text).get('proxy')
    return new_ip

if __name__ == '__main__':
    app.run(debug=True, port = 8080)