
from flask.app import Flask
from mongoengine.document import Document
from mongoengine.errors import ValidationError
from mongoengine.queryset.base import CASCADE
import pymongo
from werkzeug.datastructures import MultiDict
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
import mongoengine as me

class Venue(me.Document):
    name = me.StringField(required=True)
    perma = me.StringField(required=True)
    url = me.URLField()
    email = me.EmailField(required=True)
    phone = me.EmailField(required=True)
    location = me.LazyReferenceField(
        "Location", passthrough=True, reverse_delete_rule=CASCADE)
    desc = me.StringField(required=True, max_length=1024*8)
    short = me.StringField(required=True, max_length=128)
    tags = me.ListField(me.StringField(min_length=3))
    icon = me.ImageField(size=(1024, 1024, True),
                         thumbnail_size=(128, 128, True))
    photos = me.ListField(me.ImageField(size=(2048, 2048, False),
                         thumbnail_size=(512, 512, False)))
    owners = me.ListField(me.ReferenceField(User))
    hide = me.BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ["$perma", "$email", "$phone", '$name', "$desc", "$short", "$tags"],
         'default_language': "english",
         'weights': {"perma": 10, 'name': 9, 'tags': 9, 'email': 8, 'phone': 8, 'desc': 5, 'desc': 5 }
         }
    ]}

    def renderCard(venue: Any):
        return render_template("venueCard.html.j2", venue=venue)

    def renderDelete(user: User, nonce: str, venues: Any):
        return render_template("venueDelete.html.j2", user=user, venues=venues)

    def renderEdit(user: User, nonce: str, venue: Any):
        return render_template("venueEdit.html.j2", user=user, venue=venue)

    def renderForm(user: User, nonce: str, form: Any, errors: list):
        return render_template("venueForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: User, venues: list):
        return render_template("venueList.html.j2", user=user, venues=venues)

    def renderNew(user: User, nonce: str, form: Any, errors: list):
        return render_template("venueNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: User, venue: Any):
        return render_template("venuePage.html.j2", user=user, venue=venue)

    def register(form: Dict, user: User):
        venue = Venue(form)
        venue.owners.append(user.id)
        venue.validate()
        return venue.save()

    def setupApp(app: Flask):

        @app.route("/venue/<id>")
        def venuePage(id):
            user: User or None = None
            if "user" in session:
                user = session["user"]
            venue = Venue.object({"_id": id})
            if venue is None:
                return redirect(url_for('indexGET'))
            return Venue.renderPage(user, venue)

        @app.route("/venue/<id>/edit", methods=['POST', 'GET'])
        def editVenue(id):
            user = None
            f = {}
            errors = {}
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    venue: Venue or None = Venue.object({"_id": id, "owners": user.id})
                    if venue is None:
                        return redirect(url_for('listVenue'))
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        for key, value in f.items(multi=True):
                            user[key] = value
                        if f["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            try:
                                venue.validate()
                            except ValidationError as err:
                                errors[err.field_name] = err.message
                            else:
                                venue.save()
                    return Venue.renderEdit(user, nonce, venue, f, errors)
            return redirect(url_for('login'))

        @app.route("/venue/list")
        def listVenueJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return Venue.renderList(user)
            return redirect(url_for('login'))

        @app.route("/venue/list.json")
        def listVenue():
            if "user" in session:
                user = session["user"]
                if user:
                    venues: Document = Venue.select_related()
                    limit = 0
                    skip = 0
                    text = None
                    if "limit" in request.args and int(request.args["limit"]) > 0:
                        limit = int(request.args["limit"])
                    if "offset" in request.args and int(request.args["offset"]) > 0:
                        skip = int(request.args["offset"])
                    if "search" in request.args and request.args["search"] != "":
                        text = request.args["search"]
                    venues.objects({"owners": user.id}).limit(limit).skip(0)
                    resp = {}
                    resp["total"] = len(venues)
                    resp["rows"] = venues
                    return resp, 200
            return redirect(url_for('login')), 401

        @app.route("/venue/delete")
        def deleteVenue():
            if "user" in session:
                nonce = None
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    items = request.args["items"]
                    venues: List[Venue] = Venue.objects({"_id": items, "owners": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            for venue in venues:
                                venue.delete()
                            l = len(venues)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listVenue'))
                    return Venue.renderDelete(user, nonce, venues)
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
                        try:
                            venue = Venue.register(f, user)
                        except ValidationError as err:
                            errors[err.field_name] = err.message
                        else:
                            if venue:
                                return redirect(url_for('venuePage', id=venue.id))
                    else:
                        flash(_("Bad nonce!"), "danger")
                f["nonce"] = nonce
                return Venue.renderNew(user, f, errors), 200
            return redirect(url_for('login'))
