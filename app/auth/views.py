from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee

import re 

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        if not (re.search(regex,form.email.data)):  
            flash('Invalid Email ID','error')
            return redirect(url_for('auth.register'))
        if form.password.data != form.confirm_password.data:
            flash('Password does not match Confirm Password','error')
            return redirect(url_for('auth.register'))
        try:
            db.session.add(employee)
            db.session.commit()
        except:
            print( "Error")
            flash('Username/Email already exists','error')
            return redirect(url_for('auth.register'))
        flash('You have been successfully registered! You may now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verifypassword(
                form.password.data):
            login_user(employee)
            return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.','success')
    return redirect(url_for('auth.login'))
