from mongoengine.fields import ImageField, ListField
from forms.location import LocationForm
import re
from wtforms import *
import wtforms.validators as validators
from wtforms.fields.html5 import *
from flask_babel import gettext as _
from typing import *
from forms.tagList import TagListField


class BandForm(Form):
    id = HiddenField("_id", default=None)
    name = StringField(
        label=_("Name"),
        validators=[
            validators.data_required(_("Email required!"))
        ]
    )
    perma = StringField(
        label=_("Permalink")
    )
    url = URLField(
        label=_("Website")
    )
    email = EmailField(
        label=_("Email"),
        validators=[
            validators.data_required(_("Email required!"))
        ]
    )
    phone = TelField(label=_("Tel"),
                     validators=[
        validators.data_required(_("International contact required!"))
    ])
    location = FormField(LocationForm)
    short = TextAreaField(
        label=_("Excerpt")
    )
    desc = TextAreaField(
        label=_("Description")
    )
    tags = TagListField(label=_("Tags"))
    icon = FileField(label=_("Icon"), default=None)
    photos = MultipleFileField(label=_("Photos"), default=None)
    hide = BooleanField(label=_("Hide from public"))

    def validate_perma(value):
        m = re.match("/", value)
        if m is not None:
            raise ValidationError(_("Forward slashes are forbidden!"))
        m = re.match("^(?!/)[\w|\d| ]+(?!/)$", value)
        if m is None:
            raise ValidationError(_("Needs to be valid!"))
