from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length



class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)





   # def __init__(self, original_nickname, *args, **kwargs):
   #     Form.__init__(self, *args, **kwargs)
   #     self.original_nickname = original_nickname



