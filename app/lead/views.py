from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import login_required, current_user

from . import lead
from .. import db
from ..models import Employee, Team, Projects, EmpProjects, Role, Task, Tgroup
from ..admin.forms import ProjectForm
import datetime

def check_access():
    if ((current_user.is_lead == 0) and (current_user.is_admin == 0)):
        abort(403)

@lead.route('/team/members', methods=['GET', 'POST'])
@login_required
def list_members():
    """
    List all employees
    """
    check_access()
    e = current_user.team_id
    f = current_user.id
    # print(f)
    employees = Employee.query.filter((((Employee.id != f) & (Employee.team_id == e))))
    if current_user.is_admin == 1:
        employees = Employee.query.all()
    # return render_template('lead/members/members.html',employees=employees, title='Employees')
    emp = []
    for x in employees:
        p = EmpProjects.query.filter((EmpProjects.eid == x.id)).count()
        role = Role.query.filter((Role.id == x.role_id)).first()
        emp.append({
            'id' : x.id,
            'Ename' : x.first_name + ' ' + x.last_name,
            'Prole' : role.name,
            'EPcount' : p
        })
    return jsonify(emp)

@lead.route('/team/projects', methods=['GET', 'POST'])
@login_required
def team_projects():
    """
    List all projects
    """
    e = current_user.team_id
    projects = Projects.query.filter((((Projects.tid == e) & (Projects.closed == False))))
    PCount = []
    for x in projects:
        p = EmpProjects.query.filter((EmpProjects.pid == x.pid)).count()
        PCount.append({
            'Pro' : x.pid,
            'Pname' : x.projectname,
            'Pdesc' : x.description,
            'Pstart': x.start_time,
            'Pcount' : p
        })
    return jsonify(PCount)
    # check_access()
    # e = current_user.team_id
    # projects = Projects.query.filter((((Projects.tid == e))))
    # team = Team.query.get_or_404(e)
    # return render_template('lead/team/projects.html', team=team, projects=projects, title="Team Dashboard", subtitle="Projects")

@lead.route('/team/project/<int:id>/members', methods=['GET'])
@login_required
def list_projects_emp(id):
    """
    List all projects
    """
    check_access()
    project = Projects.query.get_or_404(id)
    pid = project.pid
    f = current_user.id
    emp = EmpProjects.query.filter((((EmpProjects.pid == pid))))
    # print emp
    for e in emp:
        print e.eid
    return jsonify({'success':True})


@lead.route('/team/dashboard', methods=['GET', 'POST'])
@login_required
def dash():
    """
    Team Dashboard
    """
    check_access()
    if current_user.is_admin == 1:
        return redirect(request.referrer)
    e = current_user.team_id
    f = current_user.id
    # print(f)
    employees = Employee.query.filter((((Employee.id != f) & (Employee.team_id == e))))
    projects = Projects.query.filter((((Projects.tid == e) & (Projects.closed == False))))
    ComProjects = Projects.query.filter((((Projects.tid == e) & (Projects.closed == True))))
    PCount = []
    for x in projects:
        p = EmpProjects.query.filter((EmpProjects.pid == x.pid)).count()
        PCount.append({
            'Pro' : x.pid,
            'Pcount' : p
        })
    team = Team.query.get_or_404(e)
    tcount = 0.7
    return render_template('lead/leadbase.html', projects=projects, pcount=PCount, comprojects = ComProjects, team=team, tcount=tcount, employees=employees, title='Team Dashboard')

@lead.route('/team/tasks', methods=['GET', 'POST'])
@login_required
def teamtasks():
    """
    Team Tasks
    """
    check_access()
    if current_user.is_admin == 1:
        return redirect(request.referrer)
    e = current_user.team_id
    f = current_user.id
    # print(f)
    team = Team.query.filter((Team.id == e))
    return render_template('lead/tasks.html', team=team, title='Team Dashboard')

@lead.route('/api/team/tasks', methods=['GET', 'POST'])
@login_required
def apiteamtasks():
    if request.method == 'GET':
        check_access()
        e = current_user.team_id
        f = current_user.id
        groups = Tgroup.query.filter(((Tgroup.tid == e))).all()
        Tasks = []
        for x in groups:
            p = Task.query.filter((Task.groupid == x.gid)).all()
            pc =  Task.query.filter((Task.groupid == x.gid)).count()
            a = []
            b = Task.query.filter((Task.groupid == x.gid)).first()
            for y in p:
                if y.status == 0 or y.status == None:
                    status = "Yet to start"
                elif y.status == 1:
                    status = "On-going"
                elif y.status == 2:
                    status = "Completed"
                a.append({
                    'Eid' : y.employeeid,
                    'Ename' : Employee.getname(y.employeeid),
                    'status' : status,
                    'isCompleted' : y.iscompleted
                })
            Tasks.append({
                'Tid' : b.tid,
                'Task' : b.task,
                'Tcount' : pc,
                'Temp' : a,
                'Priority' : b.priority,
                'start' : b.start_time,
                'end' : b.end_time,
                'gid' : b.groupid,
                'group' : x.gname

            })
        return jsonify(Tasks)
    else:
        check_access()
        task  = request.form.get('task')
        deadline = request.form.get('deadline')
        end_time = datetime.datetime.strptime(deadline, '%Y-%m-%d')
        print(end_time)
        priority = request.form.get('priority')
        group = request.form.get('group')
        e = current_user.team_id
        f = current_user.id
        if priority == "High":
            priority = 1
        else:
            priority = 0
        print(group)
        # print(newemp[0])
        if group == "ind":
            newg = Tgroup(gname=group,tid=e)
            try:
                db.session.add(newg)
                db.session.commit()
            except e:
                print(e)
            test = request.form.get('emp')
            test = test[1:-1]
            emp = test.split(",")
            print(emp)
            groupid = Tgroup.query.order_by(Tgroup.gid.desc()).first().gid
            for i in emp:
                t = Task(task=task,employeeid=i,priority=priority,start_time=datetime.datetime.now(),end_time=end_time, iscompleted=False, groupid=groupid)
                try:
                    db.session.add(t)
                    db.session.commit()
                except e:
                    print(e)
        return jsonify({"success":"true"})
        

@lead.route('/api/team/members', methods=['GET', 'POST'])
@login_required
def fetchteamemp():
    f = current_user.team_id
    e = current_user.id
    emp = Employee.query.filter(((Employee.team_id == f)&(Employee.id != e))).all()
    Employees = []
    for x in emp:
        Employees.append({
            'id':x.id,
            'name':x.getname(x.id),
            'role' : x.getrole()
        })
    return jsonify(Employees)

@lead.route('/api/team/project/<int:id>', methods=['GET', 'POST'])
@login_required
def fetchteamproemp(id):
    f = current_user.team_id
    e = current_user.id
    emp = EmpProjects.query.filter((EmpProjects.pid == id)).all()
    Employees = []
    for x in emp:
        Employees.append({
            'id':x.eid,
            'name': Employee.query.filter((Employee.id == x.eid)).first().getname(x.eid),
            'role' : Employee.query.filter((Employee.id == x.eid)).first().getrole()
        })
    return jsonify(Employees)

@lead.route('/api/team/projects', methods=['GET', 'POST'])
@login_required
def fetchteampro():
    f = current_user.team_id
    e = current_user.id
    pro = Projects.query.filter(((Projects.tid == f))).all()
    projects = []
    for x in pro:
        projects.append({
            'id':x.pid,
            'name':x.projectname,
        })
    return jsonify(projects)



@lead.route('/team/projects/add/', methods=['GET', 'POST'])
@login_required
def add_team_project():
    """
    Add Project
    """
    check_access()
    date = request.form['projectdate']
    name = request.form['projectname']
    desc = request.form['projectdesc']
    proj = Projects(projectname=name,description=desc, tid=current_user.team_id, start_time=date)
    try:
        db.session.add(proj)
        db.session.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False})



# @lead.route('/team/projects/add/', methods=['GET', 'POST'])
# @login_required
# def add_team_projects():
#     """
#     Add Project
#     """
#     check_access()
#     team = Team.query.get_or_404(current_user.team_id)
#     form = ProjectForm()
#     if form.validate_on_submit():
#         print(form.name.data)
#         proj = Projects(projectname=form.name.data,description=form.description.data, tid=current_user.team_id, start_time=form.start.data)
#         try:
#             # add role to the database
#             db.session.add(proj)
#             db.session.commit()
#             flash('You have successfully added a Project.')
#         except:
#             # in case proj name already exists
#             flash('Error: Project name already exists.')
#         return redirect(url_for('lead.list_projects'))
        
#     return render_template('lead/projects/edit.html', team=team, form=form, title="Add Team Members")
    

# @lead.route('/team/projects/delete/<int:tid>/<int:pid>', methods=['GET', 'POST'])
# @login_required
# def delete_team_project(tid, pid):
#     """
#     Delete Project
#     """
#     check_access()
#     if current_user.is_admin == 0:
#         tid = current_user.team_id
#     team = Team.query.get_or_404(tid)
#     emp = EmpProjects.query.filter(EmpProjects.pid == pid)
#     for x in emp:
#         e = EmpProjects.query.get_or_404(x.eid).all()
#         db.session.delete(e.eid)
#         db.session.commit()   
#     prj = Projects.query.get_or_404(pid)
#     db.session.delete(prj)
#     db.session.commit() 
#     return redirect(url_for('lead.list_projects'))  
#     return render_template('lead/projects/projects.html', team=team, form=form, title="Add Team Members")



