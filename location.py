
from flask.app import Flask
from db import Model, Database
from flask import render_template, request, session, redirect, url_for, flash
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from copy import Error, error
from typing import *

MissingCountry = Error(_("Missing country!"))
MissingAddress1 = Error(_("Missing address 1!"))
MissingState = Error(_("Missing state/province/region!"))
MissingCity = Error(_("Missing city!"))
MissingZIP = Error(_("Missing zip!"))


class Location(Model):
    def testCountry(form: Any, value: Any, errors: list):
        # TODO: Check service for country
        if not isinstance(value, str):
            errors.append(MissingCountry)

    def testAddress1(form: Any, value: Any, errors: list):
        # TODO: Check service if address exists?
        if not isinstance(value, str):
            errors.append(MissingAddress1)

    def testState(form: Any, value: Any, errors: list):
        # TODO: Check service if state exists?
        if not isinstance(value, str):
            errors.append(MissingState)

    def testCity(form: Any, value: Any, errors: list):
        # TODO: Check service if city exists?
        if not isinstance(value, str):
            errors.append(MissingCity)

    def testZIP(form: Any, value: Any, errors: list):
        # TODO: Check service if zip exists
        if not isinstance(value, str) or int(value) == 0:
            errors.append(MissingZIP)

    type = Model.newProp("type", "Point")
    country = Model.newProp("country", None, testCountry)
    state = Model.newProp("state", None, testState)
    city = Model.newProp("city", None, testCity)
    address1 = Model.newProp("address1", None, testAddress1)
    address2 = Model.newProp("address2")
    zip = Model.newProp("zip", None, testZIP)
    coordinates = Model.newProp("coordinates", [])
    timezone = Model.newProp("timezone")

    def resolve(input: Any):
        return Model.resolve(Location, input)

    def __init__(self, data: Any):
        super().__init__(data)

    def findOne(criteria: Any):
        return Database.main.findOne(Location, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(Location, criteria)

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
                locations = Location.findMany(query)
                if isinstance(locations, list):
                    for item in locations:
                        item.update()
                    if len(locations) == 0:
                        locations.extend(Location.QueryService(query))
                    return locations
                return None, 204
            return redirect(url_for('login')), 401
