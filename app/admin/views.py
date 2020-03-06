from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import TeamForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Team, Role, Employee


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/teams', methods=['GET', 'POST'])
@login_required
def list_teams():
    check_admin()
    teams = Team.query.all()
    return render_template('admin/teams/teams.html',
                           teams=teams, title="Teams")


@admin.route('/teams/add', methods=['GET', 'POST'])
@login_required
def add_team():
    check_admin()
    add_team = True
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data,
                                description=form.description.data)
        try:
            # add team to the database
            db.session.add(team)
            db.session.commit()
            flash('You have successfully added a new team.')
        except:
            # in case team name already exists
            flash('Error: team name already exists.')

        # redirect to teams page
        return redirect(url_for('admin.list_teams'))

    # load team template
    return render_template('admin/teams/team.html', action="Add",
                           add_team=add_team, form=form,
                           title="Add Team")


@admin.route('/teams/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    """
    Edit a team
    """
    check_admin()

    add_team = False

    team = Team.query.get_or_404(id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the team.')

        # redirect to the teams page
        return redirect(url_for('admin.list_teams'))

    form.description.data = team.description
    form.name.data = team.name
    return render_template('admin/teams/team.html', action="Edit",
                           add_team=add_team, form=form,
                           team=team, title="Edit Team")


@admin.route('/teams/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_team(id):
    """
    Delete a team from the database
    """
    check_admin()

    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    flash('You have successfully deleted the team.')

    # redirect to the teams page
    return redirect(url_for('admin.list_teams'))

    return render_template(title="Delete Team")


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


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
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

#--------------------------------------------------#

