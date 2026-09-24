from flask import Blueprint, Flask, session, request, url_for, redirect, render_template, flash
from app import db, admin_db
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint("routes", __name__)

@routes.route('/')
def home():

    return render_template('home.html')


@routes.route('/timetable', methods=['GET','POST'])
def timetable():
    if request.method == 'POST':
        branch = request.form.get('branch')
        sec = request.form.get('section')
        return redirect(url_for('routes.timetable', branch=branch, sec=sec))

    branch = request.args.get('branch')
    sec = request.args.get('sec')
    timetable = db.get_timetable(branch, sec) if branch and sec else []
    return render_template('timetable.html', timetable=timetable, branch=branch, section=sec)

