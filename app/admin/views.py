from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import null

from . import admin
from .forms import TeamForm, RoleForm,ChangeTeamForm, EmployeeAssignForm, TeamAssignForm
from .. import db
from ..models import Team, Role, Employee


def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    check_admin()
    employeecount = Employee.query.filter(Employee.is_admin == 0).count() 
    employees = Employee.query.filter(Employee.is_admin == 0)
    teamcount = Team.query.filter().count() 
    teams = Team.query.all()
    return render_template('admin/admin_dashboard.html',title="Admin Dashboard",employees=employees, employeecount=employeecount, teamcount=teamcount, teams=teams)

@admin.route('/teams', methods=['GET', 'POST'])
@login_required
def list_teams():
    check_admin()
    teams = Team.query.all()
    return render_template('admin/teams/Teampage.html', title="Teams", teams=teams)

# @admin.route('/teams/add', methods=['GET', 'POST'])
# @login_required
# def add_team():
#     check_admin()
#     add_team = True
#     form = TeamForm()
#     if form.validate_on_submit():
#         team = Team(name=form.name.data,
#                                 description=form.description.data)
#         try:
#             # add team to the database
#             db.session.add(team)
#             db.session.commit()
#             flash('You have successfully added a new team.')
#             Addsuccess = 1
#             Addfail = 0
#             return True
            
#         except:
#             # in case team name already exists
#             flash('Error: team name already exists.')
#             Addfail = 1
#             Addsuccess = 0
#         # redirect to teams page
#         return redirect(url_for('admin.list_teams', Addfail=Addfail,Addsuccess=Addsuccess))

#     # load team template
#     return render_template('admin/teams/team.html', action="Add",
#                            add_team=add_team, form=form,
#                            title="Add Team")

@admin.route('/teams_add', methods=['POST'])
@login_required
def team_add():
    check_admin()
    teamname = request.form['teamname']
    teamdesc = request.form['teamdesc']
    # print teamname
    # print teamdesc
    team = Team(name=teamname,description=teamdesc)
    try:
        db.session.add(team)
        db.session.commit()
    except: 
        return jsonify({'success':False})
      
    return jsonify({'success':True})
    # try:
    #     db.session.add(team)
    #     db.session.commit()
    #     flash('You have successfully added a new team.')
    #     Addsuccess = 1
    #     Addfail = 0
    #     return True

@admin.route('/teams/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    """
    Edit a team
    """
    check_admin()

    team = Team.query.get_or_404(id)
    lead = Employee.query.filter(((Employee.team_id == id) & (Employee.is_lead == 1)))
    emp = Employee.query.filter(((Employee.team_id == id) & (Employee.is_lead == 0)))
    nemp = Employee.query.filter(((Employee.team_id != id) | (Employee.team_id.is_(None)) )) 
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        db.session.commit()
        return redirect(url_for('admin.edit_team', id=id))
    return render_template('admin/teams/team.html', form=form, employees=emp, lead=lead, notemployees=nemp, team=team, title="Edit Team")


# @admin.route('/teams/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_team(id):
#     """
#     Delete a team from the database
#     """
#     check_admin()

#     team = Team.query.get_or_404(id)
#     db.session.delete(team)
#     db.session.commit()
#     flash('You have successfully deleted the team.')

#     # redirect to the teams page
#     return redirect(url_for('admin.list_teams'))

#     return render_template(title="Delete Team")


@admin.route('/teams/delete', methods=['POST'])
@login_required
def team_delete():
    """
    Delete a team from the database
    """
    check_admin()
    id = request.form['id']
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'success':True})

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


# @admin.route('/roles/add', methods=['GET', 'POST'])
# @login_required
# def add_role():
#     """
#     Add a role to the database
#     """
#     check_admin()

#     add_role = True

#     form = RoleForm()
#     if form.validate_on_submit():
#         role = Role(name=form.name.data,
#                     description=form.description.data)

#         try:
#             # add role to the database
#             db.session.add(role)
#             db.session.commit()
#             flash('You have successfully added a new role.')
#         except:
#             # in case role name already exists
#             flash('Error: role name already exists.')

#         # redirect to the roles page
#         return redirect(url_for('admin.list_roles'))

#     # load role template
#     return render_template('admin/roles/role.html', add_role=add_role,
#                            form=form, title='Add Role')
@admin.route('/role/add', methods=['POST'])
@login_required
def role_add():
    check_admin()
    name = request.form['rolename']
    desc = request.form['roledesc']
    print(id)
    print(name)
    print(desc)
    role = Role(name=name,description=desc)
    try:
        role.name = name
        role.description = desc
        db.session.add(role)
        db.session.commit()
    except: 
        return jsonify({'success':False})

    return jsonify({'success':True})

@admin.route('/role/edit', methods=['POST'])
@login_required
def role_edit():
    check_admin()
    id = request.form['id']
    name = request.form['rolename']
    desc = request.form['roledesc']
    print(id)
    print(name)
    print(desc)
    role = Role.query.get_or_404(id)
    try:
        role.name = name
        role.description = desc
        db.session.commit()
    except: 
        return jsonify({'success':False})

    return jsonify({'success':True})
    
@admin.route('/role/delete', methods=['POST'])
@login_required
def role_delete():
    check_admin()
    id = request.form['id']
    print(id)
    role = Role.query.get_or_404(id)
    try:
        db.session.delete(role)
        db.session.commit()
    except: 
        return jsonify({'success':False})

    return jsonify({'success':True})

# @admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_role(id):
#     """
#     Edit a role
#     """
#     check_admin()

#     add_role = False

#     role = Role.query.get_or_404(id)
#     form = RoleForm(obj=role)
#     if form.validate_on_submit():
#         role.name = form.name.data
#         role.description = form.description.data
#         db.session.add(role)
#         db.session.commit()
#         flash('You have successfully edited the role.')

#         # redirect to the roles page
#         return redirect(url_for('admin.list_roles'))

#     form.description.data = role.description
#     form.name.data = role.name
#     return render_template('admin/roles/role.html', add_role=add_role,
#                            form=form, title="Edit Role")


# @admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_role(id):
#     """
#     Delete a role from the database
#     """
#     check_admin()

#     role = Role.query.get_or_404(id)
#     db.session.delete(role)
#     db.session.commit()
#     flash('You have successfully deleted the role.')

#     # redirect to the roles page
#     return redirect(url_for('admin.list_roles'))

#     return render_template(title="Delete Role")


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    # return employees
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a team and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a team or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.team = form.team.data
        print(form.role.data)
        if form.role.data.name == "Team Lead":
            employee.is_lead = 1
        else:
            employee.is_lead = 0
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a team and a role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Assign a team and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a team or role
    if employee.is_admin:
        abort(403)

    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the account.')

    # redirect to the roles page
    return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Delete Employee')


@admin.route('/teams/members/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team_members(id):
    """
    Edit team members
    """
    check_admin()
    team = Team.query.get_or_404(id)
    form = TeamAssignForm()
    employees = Employee.query.all()

    if form.validate_on_submit():
        # print(form.employee.data.id)
        emp = Employee.query.get_or_404(form.employee.data.id)
        emp.tid = id
        if emp.is_admin:
            abort(403)
        db.session.commit()
        message = 'You have successfully added '+form.employee.data.first_name+' to the team'
        flash(message)
    return render_template('admin/teams/members/edit.html', addmore = True, employees=employees, team=team, form=form, title="Add Team Members")

@admin.route('/teams/members/add/<int:id>/<int:eid>', methods=['GET', 'POST'])
@login_required
def add_team_member(id, eid):
    """
    Edit team members
    """
    check_admin()
    employee = Employee.query.get_or_404(eid)
    employee.team_id = id
    if employee.is_admin:
        abort(403)
    db.session.commit()
    return redirect(url_for('admin.edit_team', id=id))

@admin.route('/employees/team/change/<int:id>/<int:eid>', methods=['GET', 'POST'])
@login_required
def change_member_team(id, eid):
    check_admin()
    employee = Employee.query.get_or_404(eid)
    print(eid)
    if employee.is_admin:
        abort(403)
    try:
        employee.team_id = None
    except TypeError:
        pass
    db.session.commit()
    return redirect(url_for('admin.edit_team', id=id))