
from flask.app import Flask
import pymongo
from werkzeug.datastructures import MultiDict
from db import Model, Database, devSetResponse, devListJSON
from flask import render_template, request, session, redirect, url_for, flash
import os
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from user import User
from location import Location
from upload import Upload
from typing import *


class Venue(Model):
    name = Model.newProp("name")
    perma = Model.newProp("perma")
    url = Model.newProp("url")
    email = Model.newProp("email")
    phone = Model.newProp("phone")
    location = Model.newProp("location")
    desc = Model.newProp("desc", "")
    short = Model.newProp("short", "")
    tags = Model.newProp("tags", [])
    icon = Model.newProp("icon")
    photos = Model.newProp("photos", [])
    owners = Model.newProp("owners", [])
    hide = Model.newProp("hide", False)

    def renderCard(venue: Any):
        return render_template("venueCard.html.j2", venue=venue)

    def renderDelete(user: User, venue: Any):
        return render_template("venueDelete.html.j2", user=user, venue=venue)

    def renderEdit(user: User, venue: Any):
        return render_template("venueEdit.html.j2", user=user, venue=venue)

    def renderForm(user: User, form: Any, errors: list):
        return render_template("venueForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: User, venues: list):
        return render_template("venueList.html.j2", user=user, venues=venues)

    def renderNew(user: User, form: Any, errors: list):
        return render_template("venueNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: User, venue: Any):
        return render_template("venuePage.html.j2", user=user, venue=venue)

    def resolve(input: Any):
        return Model.resolve(Venue, input)

    def setResponse(self: Model, user: Any, include: List[str or Type[Model]], resp: Dict = {}):
        return devSetResponse({
            "location": Location,
            "icon": Upload,
            "photos": [Upload],
            "owners": [User]
        })(self, user, include, resp)

    def filter(self, user: Any) -> Any:
        data = Model.filter(self, user)
        if user is not User:
            del data["owners"]
        elif not user.admin and not self.isOwner(user):
            del data["owners"]
        return data

    def __init__(self, data: Any):
        super().__init__(Model.setResolve(data, {
            "location": Location,
            "icon": Upload,
            "photos": Upload
        }))

    def findOne(criteria: Any):
        return Database.main.findOne(Venue, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(Venue, criteria)

    def register(form: Dict):
        venue = Venue(form)
        return venue.save()

    def setupApp(app: Flask):
        col = Database.main.getCollection(Venue)
        col.create_index([
            ('name', pymongo.TEXT),
            ('email', pymongo.TEXT),
            ('phone', pymongo.TEXT),
            ('desc', pymongo.TEXT),
            ('short', pymongo.TEXT),
            ('tags', pymongo.TEXT)
        ], name="venueIndexModel")

        @app.route("/venue/<id>")
        def venuePage(id):
            user: User or None = None
            if "user" in session:
                user = session["user"]
            venue = Venue.findOne({"_id": id})
            if venue is None:
                return redirect(url_for('indexGET'))
            return Venue.renderPage(user, venue)

        @app.route("/venue/<id>/edit", methods=['POST', 'GET'])
        def editVenue(id):
            user = None
            f = {}
            errors = []
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    venue = Venue.findOne({"_id": id, "owners": user.id})
                    if venue is None:
                        return redirect(url_for('listVenue'))
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        venue.apply(f)
                        if f["nonce"] != user.getNonce():
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            if len(venue.errors) == 0:
                                venue.save()
                    f["nonce"] = user.getNonce()
                    return Venue.renderEdit(user, venue, f, errors)
            return redirect(url_for('login'))

        @app.route("/venue/list")
        def listVenueJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    venues = Venue.findMany({"owner": user.id})
                    return Venue.renderList(user, venues)
            return redirect(url_for('login'))

        @app.route("/venue/list.json")
        def listVenue():
            if "user" in session:
                user = session["user"]
                if user:
                    return devListJSON(user, request, Venue, [Venue, Upload, Location])
            return redirect(url_for('login')), 401

        @app.route("/venue/delete")
        def deleteVenue():
            if "user" in session:
                nonce = None
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    items = request.args["items"]
                    venues = Venue.findMany({"_id": items, "owners": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            for venue in venues:
                                venue.remove()
                            l = len(venues)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listVenue'))
                    return Venue.renderDelete(user, venues, nonce)
            return redirect(url_for('login'))

        @app.route('/venue/new', methods=['POST', 'GET'])
        def newVenue():
            if "user" in session:
                user: User = session["user"]
                nonce = user.getNonce()
                errors = []
                f = {}
                if request.method == "POST":
                    f = MultiDict(request.form.items(multi=True))
                    if f.get("nonce") == nonce:
                        user.delNonce()
                        venue = Venue(f)
                        venue.addOwner(user)
                        if len(venue.errors) == 0:
                            venue = Venue.register(venue)
                            if venue:
                                return redirect(url_for('venuePage', id=venue.id))
                        else:
                            errors.extend(venue.errors)
                    else:
                        flash(_("Bad nonce!"), "danger")
                f["nonce"] = nonce
                return Venue.renderNew(user, f, errors), 200
            return redirect(url_for('login'))
