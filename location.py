
from copy import Error
from flask.app import Flask
from flask import request, session, redirect, url_for
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from typing import *
import mongoengine as me

MissingCountry = Error(_("Missing country!"))
MissingAddress1 = Error(_("Missing address 1!"))
MissingState = Error(_("Missing state/province/region!"))
MissingCity = Error(_("Missing city!"))
MissingZIP = Error(_("Missing zip!"))

class Location(me.Document):

    coordinates = me.PointField(auto_index=True)
    timezone = me.StringField()
    zip = me.StringField()
    address1 = me.StringField()
    address2 = me.StringField()
    city = me.StringField()
    state = me.StringField()
    country = me.StringField()
    type = me.StringField()

    def update(self):
        # TODO: Update old data from service
        return self

    def QueryService(query: Any):
        items = []
        # TODO: Create service
        return items

    def setupApp(app: Flask):
        @app.route("/location/query")
        def queryLocations():
            if "user" in session:
                user = session["user"]
                query = request.args
                locations: list[Location] = Location.objects(query)
                if isinstance(locations, list):
                    for item in locations:
                        item.update()
                    if len(locations) == 0:
                        locations.extend(Location.QueryService(query))
                    return locations
                return None, 204
            return redirect(url_for('login')), 401
