from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='team',
                                lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

class Task(db.Model):
    __tablename__ = 'tasks'

    tid = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    tasks = db.relationship('AssignTask', backref='task',
                                lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

class AssignTask(db.Model):
    __tablename__ = 'assigntasks'

    tid = db.Column(db.Integer, db.ForeignKey('tasks.tid'), primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    tasks = db.relationship('Employees', backref='task',lazy='dynamic', uselist=False)

    def __repr__(self):
        return '{}'.format(self.name)


class Projects(db.Model):
    __tablename__ = 'projects'


    def __repr__(self):
        return '{}'.format(self.name)

class AssignProjects(db.Model):
    __tablename__ = 'assignprojects'


    def __repr__(self):
        return '{}'.format(self.name)


