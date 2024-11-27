from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField,PasswordField, BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models import Restaurant

class ReservationForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    location = SelectField('Restaurant location', choices=[])
    party_size = IntegerField('Party Size', validators=[DataRequired(), NumberRange(min=1, max=20)])
    customer_name = StringField('Name', validators=[Length(max=100)])
    customer_phone = StringField('Phone', validators=[Length(max=15)])
    submit = SubmitField('Reserve Table')
    
class WaitingListForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    location = SelectField('Restaurant location', choices=[])
    party_size = IntegerField('Party Size', validators=[DataRequired(), NumberRange(min=1, max=20)])
    customer_name = StringField('Name', validators=[Length(max=100)])
    customer_phone = StringField('Phone', validators=[Length(max=15)])
    submit = SubmitField('Reserve Table')