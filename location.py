
from copy import Error
from forms.location import LocationForm
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

def edit(self: Location, form: LocationForm):
    self.coordinates = form.coordinates.data
    self.timezone = form.timezone.data
    self.zip = form.zip.data
    self.address1 = form.address1.data
    self.address2 = form.address2.data
    self.city = form.city.data
    self.state = form.state.data
    self.country = form.country.data
    self.type = form.type.data

    self.validate()

    return self

def register(form: LocationForm):
    loc = Location(
        id=form.id.data,
        coordinates=form.coordinates.data,
        timezone=form.timezone.data,
        zip=form.zip.data,
        address1=form.address1.data,
        address2=form.address2.data,
        city=form.city.data,
        state=form.state.data,
        country=form.country.data,
        type=form.type.data
    )
    loc.validate(clean=True)
    loc.save()
    return loc


def updateData(self):
    # TODO: Update old data from service
    return self

def queryService(query: Any):
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

Location.register = register
Location.edit = edit
Location.setupApp = setupApp
Location.updateData = updateData
Location.queryService = queryService