from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	email    = StringField  (u'Email'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	password            = PasswordField(u'Password'  , validators=[DataRequired()])
	confirm_password    = PasswordField(u'confirm-password'  , validators=[DataRequired()])
	email               = StringField  (u'Email'     , validators=[DataRequired(), Email()])

class ProfileUpdateForm(FlaskForm):
    phone       = StringField  (u'phone'      ,  validators=[DataRequired()])
    email       = StringField  (u'email'      ,  validators=[DataRequired(), Email()])
    address     = StringField  (u'address'    ,  validators=[DataRequired()])
    country     = StringField  (u'country'    ,  validators=[DataRequired()])
    description = StringField  (u'description',  validators=[DataRequired()])
    firstname   = StringField  (u'firstname'  ,  validators=[DataRequired()]) 
    lastname    = StringField  (u'lastname'   ,  validators=[DataRequired()]) 
    city        = StringField  (u'city'       ,  validators=[DataRequired()]) 