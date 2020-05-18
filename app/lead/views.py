from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import login_required, current_user

from . import lead
from .. import db
from ..models import Employee, Team, Projects, EmpProjects, Role, Task
from ..admin.forms import ProjectForm
import datetime
import random
import string
import dateutil

def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))

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



@lead.route('/team/projects/list', methods=['GET', 'POST'])
@login_required
def team_projects_list():
    """
    List all projects
    """
    check_access()
    e = current_user.team_id
    projects = Projects.query.filter((((Projects.tid == e)))).all()
    team = Team.query.get_or_404(e)
    return render_template('lead/projects.html', team=team, projects=projects, title="Team Dashboard", subtitle="Projects")

@lead.route('/team/projects', methods=['GET', 'POST'])
@login_required
def team_projects():
    """
    List all projects
    """
    check_access()
    e = current_user.team_id
    projects = Projects.query.filter((((Projects.tid == e))))
    PCount = []
    for x in projects:
        p = EmpProjects.query.filter((EmpProjects.pid == x.pid)).count()
        emp = EmpProjects.query.filter((EmpProjects.pid == x.pid)).all()
        a = []
        for y in emp:
            a.append({
                'Eid' : y.eid,
                'Ename' : Employee.getname(y.eid),
                'Erole' : Employee.query.filter((Employee.id == y.eid)).first().getrole()
            })
        if(x.closed == True):
            status = "Completed"
        else:
            status = "Not Completed"
        PCount.append({
            'Pro' : x.pid,
            'Pname' : x.projectname,
            'Pdesc' : x.description,
            'Pstart': x.start_time,
            'Pcount' : p,
            'status' : status,
            'employees' : a

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
        print(e.eid)
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
    tcount = Task.query.filter((Task.tid == e)).count()
    comtasks = Task.query.filter((Task.tid == e) & (Task.iscompleted == True)).count()
    return render_template('lead/overview.html', projects=projects, comtasks = comtasks, pcount=PCount, comprojects = ComProjects, team=team, tcount=tcount, employees=employees, title='Team Dashboard')

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
    return render_template('lead/tasks.html', team=True, title='Tasks')

@lead.route('/api/team/tasks', methods=['GET', 'POST'])
@login_required
def apiteamtasks():
    if request.method == 'GET':
        check_access()
        # e = current_user.team_id
        # f = current_user.id
        # groups = Tgroup.query.filter(((Tgroup.tid == e))).all()
        # Tasks = []
        # p = Task.query.filter((Task.groupid == x.gid)).all()
        # pc =  Task.query.filter((Task.groupid == x.gid)).count()
        # a = []
        # b = Task.query.filter((Task.groupid == x.gid)).first()
        # for y in p:
        #     if y.status == 0 or y.status == None:
        #         status = "Yet to start"
        #     elif y.status == 1:
        #         status = "On-going"
        #     elif y.status == 2:
        #         status = "Completed"
        #     a.append({
        #         'Eid' : y.employeeid,
        #         'Ename' : Employee.getname(y.employeeid),
        #         'status' : status,
        #         'isCompleted' : y.iscompleted
        #     })
        # Tasks.append({
        #     'Tid' : b.tid,
        #     'Task' : b.task,
        #     'Tcount' : pc,
        #     'Temp' : a,
        #     'Priority' : b.priority,
        #     'start' : b.start_time,
        #     'end' : b.end_time,
        #     'gid' : b.groupid,
        #     'group' : x.gname

        # })
            
        return redirect(request.url)
    else:
        check_access()
        task  = request.form.get('task')
        deadline = request.form.get('deadline')
        end_time = datetime.datetime.strptime(deadline, '%Y-%m-%d')
        print(end_time)
        priority = request.form.get('priority')   
        q = random_string(64)
        while Task.query.filter((Task.gid == q)).count()!=0:
            q = random_string(64)
        print(q)
        pid = request.form.get('project')
        e = current_user.team_id
        f = current_user.id
        if priority == "High":
            priority = 1
        else:
            priority = 0
        # print(group)
        test = request.form.get('emp')
        test = test[1:-1]
        emp = test.split(",")
        print(emp)
        for i in emp:
            t = Task(task=task,employeeid=i,priority=priority,start_time=datetime.datetime.now(),end_time=end_time, iscompleted=False, pid=pid, tid=e, gid = q)
            try:
                db.session.add(t)
                db.session.commit()
            except:
                db.session.rollback()
            
        return jsonify({"success":"true"})
        

@lead.route('/api/team/members', methods=['GET', 'POST'])
@login_required
def fetchteamemp():
    check_access()
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

@lead.route('/api/project/members/add/<int:id>', methods=['GET', 'POST'])
@login_required
def fetchprojnemp(id):
    check_access()
    Employees = []
    empro = EmpProjects.query.filter((EmpProjects.tid == current_user.team_id) & (EmpProjects.pid == id)).all()
    emp = Employee.query.filter((Employee.team_id == current_user.team_id)).all()
    # print(emp)
    for x in emp:
        c = 0
        for y in empro:
            if x.id == y.eid:
                c = 1     
        if c == 0:
            print(x.getname(x.id),"GHHHHH")
            Employees.append({
                'id': x.id,
                'name': x.getname(x.id),
                'role' :x.getrole()
            })
    return jsonify(Employees)
        

@lead.route('/project/members/add/<int:id>', methods=['GET', 'POST'])
@login_required
def addprojemp(id):
    check_access()
    # print("HUUUUUUUUU")
    pid = request.form.get('project')
    e = current_user.team_id
    f = current_user.id
    test = request.form.get('emp')
    test = test[1:-1]
    emp = test.split(",")
    for i in emp:
        print("IIIII" , i)
        A = EmpProjects(pid = pid, tid = e, eid = i)
        try:
            db.session.add(A)
            db.session.commit()
        except e:
            return jsonify({"success" : False})
    return jsonify({"success" : True}) 


@lead.route('/project/members/remove', methods=['GET', 'POST'])
@login_required
def remprojemp():
    check_access()
    # print("HUUUUUUUUU")
    pid = request.form.get('project')
    Emp = request.form.get('emp')
    p = pid
    # print(pid,emp)
    # e = current_user.team_id
    # f = current_user.id
    # test = request.form.get('emp')
    # test = test[1:-1]
    # emp = test.split(",")
    emp = EmpProjects.query.filter((EmpProjects.eid == Emp) & (EmpProjects.pid == p)).first()
    t = Task.query.filter((Task.pid == p) & (Task.employeeid == Emp)).all()
    for x in t:
        r = Task.query.filter((Task.taskid == x.taskid)).first()
        db.session.delete(r)
        db.session.commit()
    try:
        db.session.delete(emp)
        db.session.commit()
    except e:
        return jsonify({"success" : False})
    return jsonify({"success" : True})       

@lead.route('/api/team/project/<int:id>', methods=['GET', 'POST'])
@login_required
def fetchteamproemp(id):
    check_access()
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


@lead.route('/project/remove', methods=['GET', 'POST'])
@login_required
def remproject():
    check_access()
    f = current_user.team_id
    pid = request.form.get('pid')
    emp = EmpProjects.query.filter((EmpProjects.pid == pid)).all()
    # Employees = []
    for x in emp:
      e = EmpProjects.query.filter((EmpProjects.pid == pid) & (EmpProjects.tid == x.tid) & (EmpProjects.eid == x.eid)).first()
      if EmpProjects.query.filter((EmpProjects.pid == pid) & (EmpProjects.tid == x.tid) & (EmpProjects.eid == x.eid)).count() != 0:
        db.session.delete(e)
        db.session.commit()
    t = Task.query.filter((Task.pid == pid)).all()
    for x in t:
        e = Task.query.filter((Task.taskid == x.taskid)).first()
        if Task.query.filter((Task.taskid == x.taskid)).count() != 0:
            db.session.delete(e)
            db.session.commit()
    pid = request.form.get('pid')
    print(pid)
    pro = Projects.query.filter((Projects.pid == pid) & (Projects.tid == f)).first()
    if Projects.query.filter((Projects.pid == pid)).count() != 0:
        db.session.delete(pro)
        db.session.commit()
    return jsonify({"success":"true"})



@lead.route('/project/add', methods=['GET', 'POST'])
@login_required
def addproject():
    check_access()
    f = current_user.team_id
    pid = request.form.get('projectname')
    desc = request.form.get('desc')
    pro = Projects(projectname = pid, description = desc, tid = current_user.team_id)
    try:
        db.session.add(pro)
        db.session.commit()
    except e:
        db.session.rollback()
        print(e)
    return jsonify({"success":"true"})


@lead.route('/api/team/projects', methods=['GET', 'POST'])
@login_required
def fetchteampro():
    check_access()
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



@lead.route('/api/project/<int:id>/tasks', methods=['GET','POST'])
@login_required
def project_api(id):
    emp = EmpProjects.query.filter((EmpProjects.pid == id)).all()
    a = []
    for y in emp:           
        c = Task.query.filter((Task.employeeid == y.eid) & (Task.pid == id)).all()
        if Task.query.filter((Task.employeeid == y.eid) & (Task.pid == id)).count() == 0:
            continue
        l = []
        for z in c:
            deadline = z.end_time
            deadline = deadline.date()
            # deadline = datetime.datetime(deadline).date
            print(deadline)
            if z.status == 0 or z.status == None:
                status = "Yet to start"
            elif z.status == 1:
                status = "On-going"
            elif z.status == 2:
                status = "Completed"
            l.append({
                'tid' : z.taskid,
                'task' : z.task,
                'start' : z.start_time,
                'end' : z.end_time,
                'iscompleted' : z.iscompleted,
                'status' : status,
                'priority' : z.priority,
                'deadline' : deadline
            })
        a.append({
            'Eid' : y.eid,
            'Ename' : Employee.getname(y.eid),
            'Erole' : Employee.query.filter((Employee.id == y.eid)).first().getrole(),
            'tasks' : l
        })
    return jsonify(a)


@lead.route('/api/project/<int:id>/status', methods=['POST'])
@login_required
def project_status(id):
    check_access()
    status = request.form.get('status')
    print(status)
    p = Projects.query.filter((Projects.pid == id)).first()
    if(status == "1"):
        p.closed = True
    else:
        p.closed = False
    # print(p.closed)
    db.session.commit()
    # print(Projects.query.filter((Projects.pid == id)).first().closed)
    return jsonify({"success":True})


@lead.route('/api/task/<int:id>/delete', methods=['POST'])
@login_required
def task_delete(id):
    check_access()
    # taskid = request.form.get('taskid')
    # print(status)
    p = Task.query.filter((Task.taskid == id)).first()
    # if(status == "1"):
    #     p.closed = True
    # else:
    #     p.closed = False
    # print(p.closed)
    db.session.delete(p)
    db.session.commit()
    # print(Projects.query.filter((Projects.pid == id)).first().closed)
    return jsonify({"success":True})



@lead.route('/team/project/<int:id>', methods=['GET', 'POST'])
@login_required
def project_page(id):
    check_access()
    pro = Projects.query.filter(Projects.pid==id).first()
    prostatus = pro.closed
    # if prostatus:
    #     prostatus = "Completed"
    # else:
    #     prostatus = "Not Completed"
    return render_template('lead/projectpage.html',projectname=pro.projectname, id=pro.pid, prostatus=prostatus, title=pro.projectname+" Project")


@lead.route('/api/project/<int:id>/members', methods=['GET', 'POST'])
@login_required
def list_project_members(id):
    """
    List all employees
    """
    check_access()
    e = id
    # f = current_user.id
    # print(f)
    emppro = EmpProjects.query.filter((EmpProjects.pid == e))
    emp = []
    for x in emppro:
        p = Employee.query.filter((Employee.id == x.eid)).first()
        Hcount = Task.query.filter((Task.employeeid == x.eid) & (Task.priority == 1) & (Task.pid == e)).count()
        Lcount = Task.query.filter((Task.employeeid == x.eid) & (Task.priority == 0) & (Task.pid == e)).count()
        role = p.getrole()
        emp.append({
            'id' : p.id,
            'Ename' : p.getname(p.id),
            'Prole' : role,
            'Hcount': Hcount,
            'Lcount': Lcount
            # 'EPcount' : p
        })
    return jsonify(emp)