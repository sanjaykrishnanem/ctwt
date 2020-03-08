from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Team, Role, Employee


class TeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    team = QuerySelectField(query_factory=lambda: Team.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


class TeamAssignForm(FlaskForm):
    employee = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                  get_label="username")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


class ChangeTeamForm(FlaskForm):
    team = QuerySelectField(query_factory=lambda: Team.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    start = DateField(id='datepick', validators=[DataRequired()])
    submit = SubmitField('Submit')
    