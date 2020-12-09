from time import timezone
from country_list.country_list import countries_for_language
from flask.globals import session
from wtforms import *
import wtforms.validators as validators
from wtforms.fields.html5 import *
from flask_babel import gettext as _
from typing import *
from mongoengine.fields import ObjectId

class LocationForm(Form):
    def getLang():
        if session:
            return session.get('lang', 'en')
        return "en"

    def countryMap(item: Tuple[str, str]) -> Any:
        code = item[0]
        country = item[1]
        return (code, country)
    
    id = HiddenField("_id", default=ObjectId)
    coordinates = HiddenField("coordinates", default=[0, 0])
    timezone = HiddenField("timezone", default=None)
    type = HiddenField("type", default=None)
    country = SelectField(
        label=_("Country"),
        default="US",
        choices=list(map(countryMap, countries_for_language(getLang())))
    )
    state = StringField(
        label=_("State/Province/Region")
    )
    city = StringField(
        label=_("City")
    )
    address1 = StringField(
        label=_("Address1")
    )
    address2 = StringField(
        label=_("Address2")
    )
    zip = StringField(
        label=_("ZIP")
    )
