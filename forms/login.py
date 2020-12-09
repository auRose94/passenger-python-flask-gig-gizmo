from forms.user import UserForm
from wtforms import *
import wtforms.validators as validators
from wtforms.fields.html5 import *
from flask_babel import gettext as _
from typing import *

class LoginForm(Form):
    email = EmailField(
        label=_("Email"),
        validators=[
            validators.data_required(_("Email required!"))
        ]
    )
    password = PasswordField(
        label=_("Password"),
        validators=[
            validators.data_required(_("Password required!"))
        ]
    )
    rememberMe = BooleanField(
        label=_("Remember Me")
    )