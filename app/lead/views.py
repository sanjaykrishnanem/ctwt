from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import login_required, current_user

from . import lead
from .. import db
from ..models import Employee, Team, Projects, EmpProjects
from ..admin.forms import ProjectForm


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
    return render_template('lead/members/members.html',
                           employees=employees, title='Employees')

@lead.route('/team/projects', methods=['GET', 'POST'])
@login_required
def list_projects():
    """
    List all projects
    """
    check_access()
    e = current_user.team_id
    projects = Projects.query.filter((((Projects.tid == e))))
    team = Team.query.get_or_404(e)
    if current_user.is_admin == 1:
        employees = Projects.query.all()
        ad = True
    else:
        ad = False
    return render_template('lead/projects/projects.html',
                           projects=projects, title='Projects', ad = ad, team=team)

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
    projects = Projects.query.filter((((Projects.tid == e))))
    team = Team.query.get_or_404(e)
    return render_template('lead/team/dashboard.html', projects=projects, team=team, employees=employees, title='Team Dashboard')

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



