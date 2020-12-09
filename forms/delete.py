from wtforms import *
import wtforms.validators as validators
from wtforms.fields.html5 import *
from flask_babel import gettext as _
from typing import *

class DeleteForm(Form):
    items = HiddenField(
        label="Items", description="ID's of items you wanted deleted.")
    model = HiddenField(
        label="Model", description="Collection name to lookup.")
    accepted = BooleanField(label="Accecpt Removal", validators=[
        validators.DataRequired(
            _("Check this if you want to delete"))
    ])
