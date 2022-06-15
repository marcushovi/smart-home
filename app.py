import json
import time

import requests
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session
)

# import
import init

smart_devices = init.smart_devices
users = init.users

app = Flask("Smart Home")
app.secret_key = '$#%@!S)dw'


@app.errorhandler(404)
def page_not_found(e):
    if "user" in session:
        return render_template('404.html', back="dashboard", user=session['user']['username'])

    return render_template('404.html', back="login")


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')


@app.route('/')
def default():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = valid_user(request.form['username'], request.form['password'])

        if user:
            session['user'] = user
            return redirect(url_for('dashboard', usr=user['username']))
        else:
            return render_template('login.html', error="Invalid credentials!")

    else:
        if 'user' in session:
            return redirect(url_for('dashboard', usr=session['user']['username']))
        else:
            return render_template('login.html')


def valid_user(username, password):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return 0


def calculate_consumption():
    power_usage_every = 0
    power_usage_user = 0
    number_of_users = 0

    for i in range(len(smart_devices['lights'])):

        light = smart_devices['lights'][i]

        if light['notes']["owner"] == "every":
            power_usage_every += int(light['power_usage'])
        else:
            number_of_users += 1
            power_usage_user += int(light['power_usage'])

    sum_of_power_usage = power_usage_user + power_usage_every

    for i in range(len(smart_devices['lights'])):
        light = smart_devices['lights'][i]
        if light['notes']['owner'] != "every":

            aux = light['power_usage']

            if power_usage_every > 0:
                aux += power_usage_every / number_of_users

            if sum_of_power_usage > 0:
                light['power_usage_percentage'] = "{:0.2f}".format((aux / sum_of_power_usage) * 100)
            else:
                light['power_usage_percentage'] = 0

    return power_usage_every + power_usage_user


@app.route("/dashboard/<usr>")
def dashboard(usr):
    if 'user' in session:
        user = session['user']
        if user['username'] == usr:

            # update all devices
            for key in smart_devices:
                for j in range(len(smart_devices[key])):

                    smart_devices[key][j] = requests.get(smart_devices[key][j]["actions"]['device_info']).json()
                    if smart_devices[key][j]['notes'] != "":
                        smart_devices[key][j]['notes'] = json.loads(smart_devices[key][j]['notes'])

                    if smart_devices[key][j]['type'] == "SmartLight" or smart_devices[key][j]['type'] == "SwitchSensor":
                        smart_devices[key][j]['power_usage_last_recalculated_date'] = time.ctime(
                            float(smart_devices[key][j]['power_usage_last_recalculated']))
                        # just checking because of  expandable of project in future
                    elif smart_devices[key][j]['type'] == "MotionSensor":
                        smart_devices[key][j]['last_triggered_date'] = time.ctime(
                            float(smart_devices[key][j]['last_triggered_timestamp']))

            total_power_usage = calculate_consumption()

            return render_template('dashboard.html', devices=smart_devices, user=user['username'],
                                   total_power_usage=total_power_usage)
        else:
            return redirect(url_for('dashboard', usr=user['username']))
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# endpoints for devices
def check_user(usr):
    if 'user' in session:
        user = session['user']
        if (user['username'] == usr or usr == "every"):
            return True
    return False


def find_device(id, action):
    for key in smart_devices:
        for j in range(len(smart_devices[key])):
            if smart_devices[key][j]['id'] == id and smart_devices[key][j]['actions'][action]:
                return smart_devices[key][j]

    return False


def make_action(usr, id, action):
    if check_user(usr):
        device = find_device(id, action)
        if device:
            return requests.get(device['actions'][action]).json()


@app.route("/<usr>/device/<id>/turn_on")
def turn_on(usr, id):
    return make_action(usr, id, "turn_on")


@app.route("/<usr>/device/<id>/turn_off")
def turn_off(usr, id):
    return make_action(usr, id, "turn_off")


@app.route("/<usr>/device/<id>/toggle_state")
def toggle(usr, id):
    return make_action(usr, id, "toggle_state")


@app.route("/<usr>/device/<id>/change_color_blue_sky")
def blue_sky(usr, id):
    make_action(usr, id, "turn_on")
    return make_action(usr, id, "change_color_blue_sky")


@app.route("/<usr>/device/<id>/change_color_high_noon")
def high_noon(usr, id):
    make_action(usr, id, "turn_on")
    return make_action(usr, id, "change_color_high_noon")


@app.route("/<usr>/device/<id>/change_color_sunset")
def sunset(usr, id):
    make_action(usr, id, "turn_on")
    return make_action(usr, id, "change_color_sunset")


@app.route("/<usr>/device/<id>/trigger_report")
def trigger_report(usr, id):
    return make_action(usr, id, "trigger_report")
