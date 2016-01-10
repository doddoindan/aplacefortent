from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length



class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditMarkerForm(Form):
    # caption = StringField('nickname', validators=[DataRequired()])
    description = TextAreaField('description', validators=[Length(min=0, max=140)])
    shop = BooleanField('shop', default=False, )
    water = BooleanField('water', default=False)
    potable = BooleanField('potable', default=False) #drinkable water
    campfire = BooleanField('campfire', default=False)
    maxtentcount = SelectField(u'Tent count',
                               choices=[('1', '1'), ('2', '3 or less'), ('3', '5 or less'), ('4', 'unlimited')],
                               default=2
                               )
    latt = HiddenField('latt', default=0)
    long = HiddenField('long', default=0)
    id = HiddenField('id', default=-1)



   # def __init__(self, original_nickname, *args, **kwargs):
   #     Form.__init__(self, *args, **kwargs)
   #     self.original_nickname = original_nickname



