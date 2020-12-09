from forms.user import UserForm
from wtforms import *
import wtforms.validators as validators
from wtforms.fields.html5 import *
from flask_babel import gettext as _
from typing import *

class UnregisterForm(Form):
    confirm = BooleanField(
        label=_("Confirm delete"),
        validators=[
            validators.data_required(_("Check the box to confirm!"))
        ]
    )