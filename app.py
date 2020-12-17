from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import csv
import os
import time
from threading import Thread
from test import get_data

application = app = Flask(__name__)
app.secret_key = "NDU23JSC933JF3"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

directory = r'./Data'

total_orgs = []

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    activision_id = db.Column(db.String(30), nullable = False)
    username = db.Column(db.String(20), nullable=False)
    org = db.Column(db.String(20), nullable = False)
    cw_kd = db.Column(db.Float(20), default = 0.0)
    mw_kd = db.Column(db.Float(20), default = 0.0)
    wz_kd = db.Column(db.Float(20), default = 0.0)
    wz_wins = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"User {self.username}"


# Upload data to the database:
def csv_to_db():

    all_users = User.query.all()

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):

            with open(os.path.join(directory, filename), mode='r') as current_season:
                csv_reader = csv.reader(current_season)
                for line in csv_reader:

                    # Generate the total list of orgs
                    if line[1] not in total_orgs:
                        total_orgs.append(line[1])

                    user = User(username = line[0], org = line[1], activision_id = line[2],
                                cw_kd = round(float(line[3]),2), mw_kd = round(float(line[4]),2),
                                wz_kd = round(float(line[5]),2), wz_wins = line[6])

                    db.session.add(user)
                    db.session.commit()


@app.route('/filter/<org>', methods=['GET', 'POST'])
def filter(org):
    data =  User.query.filter_by(org=org)

    return render_template('index.html', org = org, data = data, total_orgs = total_orgs)


@app.route('/', methods=['GET', 'POST'])
def index():
    data = User.query.all()

    return render_template('index.html', data = data, total_orgs = total_orgs)

@app.route('/millersmellsbad', methods=['GET', 'POST'])
def miller():

    class Friend():

        org = "POO"
        cw_kd = 0
        mw_kd = 0
        wz_kd = 0
        wz_wins = 0

        def __init__(self, name, username):
            self.username = username
            self.name = name

    my_friends = {"Jack": "snowmanonfire99", "Mike": "Nincompoop#5584877", "Zach": "lil nut#1150495", "Alec": "Miller#5648187", "Cole": "Golden Eagle820"}
    my_friends_list = []

    for key, value in my_friends.items():
        friend = Friend(key, value)
        cw_kd, mw_kd, wz_kd, wz_wins = get_data(friend.username)
        friend.cw_kd, friend.mw_kd, friend.wz_kd, friend.wz_wins = round(cw_kd, 2), round(mw_kd, 2), round(wz_kd, 2), wz_wins
        my_friends_list.append(friend)


    return render_template('millersmellsbad.html', my_friends_list = my_friends_list)


@app.route('/about', methods=['GET'])
def about():

    return render_template('about.html')


@app.route('/addmydatabase', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        code = request.form.get('input_code')
        if code == "Boeing1998":
            org = request.form.get('org_input')
            username = request.form.get('username_input')
            activision_id = request.form.get('activision_id_input')

            if org not in total_orgs:
                total_orgs.append(org)

            user = User(username=username, org=org, activision_id=activision_id)

            db.session.add(user)
            db.session.commit()

            flash('Successfully added {}'.format(username))
            return redirect(url_for('add'))
        else:
            flash('Unsuccessful Update')
            return redirect(url_for('add'))

    else:
        return render_template('addmydatabase.html')


@app.route('/updatemydatabase', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        code = request.form.get('input_code')
        if code == "Boeing1998":

            username = request.form.get('username_input')

            user = User.query.filter_by(username = username).first()

            if user == None:
                flash('No user found')
                return redirect(url_for('update'))

            update_org = request.form.get('org_input')
            update_username = request.form.get('username_update_input')
            update_activision_id = request.form.get('activision_id_input')

            updating_org = request.form.get('update-org')
            updating_username = request.form.get('update-username')
            updating_activision_id = request.form.get('update-activison-id')

            updates = []

            if update_org != "" and updating_org == "update":
                user.org = update_org
                updates.append("Org")
                if update_org not in total_orgs:
                    total_orgs.append(update_org)
                db.session.commit()

            if update_username != "" and updating_username == "update":
                user.username = update_username
                updates.append("Username")
                db.session.commit()

            if update_activision_id != "" and updating_activision_id == "update":
                user.activision_id = update_activision_id
                updates.append("Activision ID")
                db.session.commit()

            if len(updates) == 0:
                flash('Unsuccessful Update')
                return redirect(url_for('update'))
            else:
                flash('Successfully updated {} for {}'.format(*updates, username))
                return redirect(url_for('update'))
        else:
            flash('Unsuccessful Update')
            return redirect(url_for('update'))

    else:
        return render_template('updatemydatabase.html')


@app.route('/deletemydatabase', methods=['GET', 'POST'])
def delete():

    if request.method == 'POST':
        code = request.form.get('input_code')
        if code == "Boeing1998":


            username = request.form.get('username_input')

            user = User.query.filter_by(username=username).first()

            db.session.delete(user)
            db.session.commit()

            flash('Successfully deleted {}'.format(username))
            return redirect(url_for('delete'))
        else:
            flash('Unsuccessful Update')
            return redirect(url_for('delete'))

    else:
        return render_template('deletemydatabase.html')


def update_loop(username):
    while True:

        updated_csv = {}
        all_users = User.query.all()

        for user in all_users:
            activision_id = user.activision_id
            cw_kd, mw_kd, wz_kd, wz_wins = get_data(activision_id)

            if cw_kd == 0 and mw_kd == 0 and wz_kd == 0 and wz_wins == 0:
                continue

            user.cw_kd, user.mw_kd, user.wz_kd, user.wz_wins = round(cw_kd,2), round(mw_kd,2), round(wz_kd,2), wz_wins
            db.session.commit()
            updated_csv[user.id] = [user.username, user.org, user.activision_id, cw_kd, mw_kd, wz_kd, wz_wins]

            if user.org not in total_orgs:
                total_orgs.append(user.org)

            time.sleep(60)

        with open('Data/data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for row, value in updated_csv.items():
                writer.writerow([value[0], value[1], value[2], value[3], value[4], value[5], value[6]])


thread = Thread(target=update_loop, args=("snowmanonfire99",))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    csv_to_db()
    thread.start()
    app.run()
