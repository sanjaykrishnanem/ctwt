from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


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
    is_lead = db.Column(db.Boolean, default=False)
    employees = db.relationship('EmpProjects', backref='empproj', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def getname(id):
        e = Employee.query.filter(Employee.id == id).first()
        return e.first_name + ' ' + e.last_name
    
    def getrole(self):
        return Role.query.filter(Role.id == self.role_id).first().name
    
    def getteam(self):
        if Team.query.filter(Team.id == self.team_id).first() is None:
            return ''
        else:
            c =  Team.query.filter(Team.id == self.team_id).first().name
            return c

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

    taskid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employees.id'))
    pid  = db.Column(db.Integer, db.ForeignKey('projects.pid'))
    tid  = db.Column(db.Integer, db.ForeignKey('teams.id'))
    gid = db.Column(db.String(256), nullable=False)

    task = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    iscompleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer)
    # groupid  = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '{}'.format(self.task)


class Projects(db.Model):
    __tablename__ = 'projects'
    pid  = db.Column(db.Integer, primary_key=True)
    tid  = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True)
    projectname = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    closed = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return '{}'.format(self.projectname)


class EmpProjects(db.Model):
    __tablename__ = 'empprojects'
    pid  = db.Column(db.Integer, db.ForeignKey('projects.pid'), primary_key=True)
    eid = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    employee = db.relationship('Employee', backref='employeeproj',uselist=False)
    tid  = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True, nullable=False)


    def __repr__(self):
        return '{}'.format(self.pid)




