from flask import Blueprint, Flask, session, request, url_for, redirect, render_template, flash
from app import db, admin_db
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')
        creds = admin_db.fetch_for_check(uname)
        try:
            if uname and pwd and check_password_hash(creds['password'], pwd):
                session['uname'] = uname
                return redirect('/admin_home')
            elif uname and pwd and not check_password_hash(creds['password'],pwd):
                flash('Wrong password entered.')
                return redirect('/login')
            else:
                flash('No field can be left empty!')
                return redirect('/login')
        except Exception as e:
            return f'''Error Occurred: {e}, this error means account probably does not exist.'''

    return render_template('/admin/login.html')


@admin.route('/admin_home',methods=['GET'])
def admin_home():
    if session.get('uname'):
        name = session.get('uname')
        return render_template('/admin/admin_home.html', name=name)
    else:
        flash('Need admin privileges to access this page')
        return redirect('/login')

@admin.route('/timetable_modify', methods=['GET','POST'])
def timetable_modify():
    if session.get('uname'):
        if request.method == 'POST':
            try:
                branch = request.form.get('branch')
                sec = request.form.get('section')
                session['branch'] = branch
                session['sec'] = sec
                return redirect(url_for('admin.timetable_modify', branch=branch, sec=sec))
            except Exception as e:
                return f'Error Occurred: {e}'
        try:
            branch = request.args.get('branch')
            sec = request.args.get('sec')
            session['branch'] = branch
            session['sec'] = sec
            timetable = db.get_timetable(branch, sec) if branch and sec else []
            return render_template('/admin/timetable_mod.html', timetable=timetable, branch=branch, section=sec)
        except Exception as e:
                return f'Error Occurred: {e}'
    else:
        flash('Need admin privileges to access this page')
        return redirect('/login')

@admin.route('/add', methods=['GET','POST'])
def add():
    if session.get('uname'):
        if request.method == 'POST':
            branch = request.form.get('branch')
            classs = request.form.get('class')
            sec = request.form.get('sec')
            day = request.form.get('day')
            order = request.form.get('order')
            if branch and classs and day and sec and order:
                try:    
                    db.class_add(classs, branch, sec, day, order)
                except Exception as e:
                    return f'Error: {e}'
            else:
                flash('Please fill all the details')
            return redirect(url_for('admin.timetable_modify', branch=branch, sec=sec))
        return redirect(url_for('admin.timetable_modify'))
    else:
        flash('Need admin privileges to access this page')
        return redirect('/login')

@admin.route('/edit/<class_detail>', methods=['GET','POST'])
def edit_class(class_detail):
    if session.get('uname'):
        details = class_detail.split('_')
        if request.method == 'POST':
            edited_c = request.form.get('edited_class')
            if edited_c and len(edited_c) < 60 :
                try:
                    db.class_edit(details[0], edited_c)
                    br = session.get('branch')
                    sec = session.get('sec')
                    return redirect(url_for('admin.timetable_modify', branch = br, sec = sec))
                except Exception as e:
                    return f'Error: {e}, Edit failed; contact admin if this persists'
            else:
                flash('Field either empty or exceeds 60 characters')
                return redirect(url_for('admin.edit_class'))

        return render_template('/admin/edit_page.html', link=class_detail, class_name=details[1])
    else:
        flash('Need admin privileges to access this page')
        return redirect('/login')

@admin.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@admin.route('/create_account', methods=['GET','POST'])
def create_account():
    if session.get('uname'):
        if request.method == 'POST':
            uname = request.form.get('username')
            pwd = request.form.get('password')

            if uname and pwd and len(uname)<25 and len(pwd)<25:
                hashed_pwd = generate_password_hash(pwd)
                try:
                    admin_db.add_user(uname, hashed_pwd)
                    flash('User added successfully!')
                    return redirect('/create_account')
                except Exception as e:
                    return f'Error: {e}; basically was unable to add user contact developer.'
            elif uname and pwd:
                flash('Too long entries entered keep it below 25 characters dumbo')
                return redirect('/create_account')
            else:
                flash('No field can be left empty nigga!')
                return redirect('/create_account')

        return render_template('/admin/create_acc.html', name = session.get('uname'))
    else:
        flash('Nope. Not without logging in first idiot!')
        return redirect('/login')

@admin.route('/delete/<c_del>')
def delete_class(c_del):
    if session.get('uname'):
        try:
            db.class_delete(c_del)
            return redirect(url_for('admin.timetable_modify', branch = session.get('branch'), sec=session.get('sec')))
        except Exception as e:
            return f'Error: {e}, Was unable to delete contact the developer.'