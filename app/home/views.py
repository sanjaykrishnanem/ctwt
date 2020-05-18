from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import login_required, current_user

from . import home
from .. import db
from ..models import Employee, Team, Projects, EmpProjects, Task

@home.route('/')
def homepage():
    return render_template('home/index.html', title='Welcome to CTWT')

@home.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@home.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin == 1:
        return redirect(url_for('admin.admin_dashboard'))
    if current_user.is_lead == 1:
        return redirect(url_for('lead.dash'))
    else:
        lead = False
    team = current_user.getteam()
    role = current_user.getrole()
    pro = EmpProjects.query.filter((EmpProjects.eid == current_user.id)).all()
    apro = 0
    compro = 0
    for x in pro:
        g = Projects.query.filter((Projects.pid == x.pid)).first()
        if g.closed == 1:
            compro = compro + 1
        else:
            apro = apro + 1
    return render_template('home/dashboard.html', title='Dashboard', lead=lead, team = team, role = role, compro = compro, apro = apro)


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Admin Dashboard')


@home.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('home/profilepage.html', title='Employee Profile')


@home.route('/api/teammates', methods=['GET', 'POST'])
@login_required
def list_members():
    """
    List all employees
    """
    e = current_user.team_id
    f = current_user.id
    # print(f)
    employees = Employee.query.filter((((Employee.id != f) & (Employee.team_id == e))))
    if current_user.is_admin == 1:
        employees = Employee.query.all()
    # return render_template('lead/members/members.html',employees=employees, title='Employees')
    emp = []
    for x in employees:
        try:
            role = x.getrole()
        except e:
            role = "None"
        emp.append({
            'id' : x.id,
            'Ename' : x.getname(x.id),
            'Prole' : role,
        })
    return jsonify(emp)


@home.route('/homeapi/projects', methods=['GET', 'POST'])
@login_required
def team_projects():
    """
    List all projects
    """
    e = current_user.id
    projects = EmpProjects.query.filter((((EmpProjects.eid == e)))).all()
    PCount = []
    for x in projects:
        p = Projects.query.filter((Projects.pid == x.pid)).all()
        # emp = EmpProjects.query.filter((EmpProjects.pid == x.pid)).all()
        # a = []
        for y in p:
            PCount.append({
                'Pro' : y.pid,
                'Pname' : y.projectname,
                'Pdesc' : y.description,
                'Pstart': y.start_time,
            })
    return jsonify(PCount)


@home.route('/homeapi/tasks/list', methods=['GET', 'POST'])
@login_required
def fetch_tasks():
    """
    List all projects
    """
    e = current_user.id
    projects = Task.query.filter((((Task.employeeid == e)))).all()
    PCount = []
    for y in projects:
        if y.status != 2:
            PCount.append({
                'Task' : y.task,
                'id'   : y.taskid,
                'pid' : y.pid,  
                'priority' : y.priority,
                'deadline' : y.end_time,
                'starttime': y.start_time,
                'status' : y.status
            })       
    return jsonify(PCount)

@home.route('/homeapi/task/start', methods=['GET', 'POST'])
@login_required
def start_task():
    """
    List all projects
    """
    id = request.form.get('task')
    # e = current_user.id
    t = Task.query.filter((Task.taskid == id)).first()
    t.status = 1
    db.session.commit()
    return jsonify({"success":"true"})

@home.route('/homeapi/task/complete', methods=['GET', 'POST'])
@login_required
def complete_task():
    """
    List all projects
    """
    id = request.form.get('task')
    # e = current_user.id
    t = Task.query.filter((Task.taskid == id)).first()
    t.status = 2
    db.session.commit()
    return jsonify({"success":"true"})