
from copy import Error
from typing import *
from flask.app import Flask
import pymongo
from pymongo.operations import IndexModel
from werkzeug.datastructures import MultiDict
from db import Model, Database, devListJSON, devSetResponse
from flask import render_template, request, session, redirect, url_for, flash
import os
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from user import User
from location import Location
from upload import Upload

class Band(Model):
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

    def renderCard(self):
        return render_template("bandCard.html.j2", band=self)

    def renderDelete(user: User, bands: list, nonce: str):
        return render_template("bandDelete.html.j2", user=user, bands=bands)

    def renderEdit(user: User, band: Any, form: Any, errors: list):
        return render_template("bandEdit.html.j2", user=user, band=band)

    def renderForm(user: User, form: Any, errors: list):
        return render_template("bandForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: User, bands: list):
        return render_template("bandList.html.j2", user=user, bands=bands)

    def renderNew(user: User, form: Any, errors: list):
        return render_template("bandNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: User, band: Any):
        return render_template("bandPage.html.j2", user=user, band=band)

    def resolve(input: Any):
        return Model.resolve(Band, input)

    def setResponse(self: Model, user: Any, include: List[str or Type[Model]], resp: Dict = {}):
        return devSetResponse({
            "location": Location,
            "icon": Upload,
            "photos": [Upload],
            "owners": [User]
        })(self, user, include, resp)

    def filter(self, user: Any) -> Any:
        data = self.__data.copy()
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
        return Database.main.findOne(Band, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(Band, criteria)

    def register(form: Any):
        band = Band(form)
        return band.save()

    def setupApp(app: Flask):
        col = Database.main.getCollection(Band)
        col.create_index([
            ('name', pymongo.TEXT),
            ('email', pymongo.TEXT),
            ('phone', pymongo.TEXT),
            ('desc', pymongo.TEXT),
            ('short', pymongo.TEXT),
            ('tags', pymongo.TEXT)
        ], name="bandIndexModel")

        @app.route("/band/<id>")
        def bandPage(id):
            user: User or None = None
            if "user" in session:
                user = session["user"]
            band = Band.findOne({"_id": id})
            if band is None:
                return redirect(url_for('indexGET'))
            return Band.renderPage(user, band)

        @app.route("/band/<id>/edit", methods=['POST', 'GET'])
        def editBand(id):
            user = None
            f = {}
            errors = []
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    band = Band.findOne({"_id": id, "owners": user.id})
                    if band is None:
                        return redirect(url_for('listBand'))
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        if f["nonce"] != user.getNonce():
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            band.apply(f)
                            if len(band.errors) == 0:
                                band.save()
                            else:
                                errors.extend(band.errors)
                    f["nonce"] = user.getNonce()
                    return Band.renderEdit(user, band, f, errors)
            return redirect(url_for('login'))

        @app.route("/band/list")
        def listBand():
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    sel = {"owner": user.id}
                    bands = Band.findMany(sel)
                    return Band.renderList(user, bands)
            return redirect(url_for('login'))

        @app.route("/band/list.json")
        def listBandJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return devListJSON(user, request, Band, [Band, Upload, Location])
            return redirect(url_for('login')), 401

        @app.route("/band/delete")
        def deleteBand():
            if "user" in session:
                nonce = None
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    items = request.args["items"]
                    bands = Band.findMany({"_id": items, "owners": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            for band in bands:
                                band.remove()
                            l = len(bands)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listBand'))
                    return Band.renderDelete(user, bands, nonce)
            return redirect(url_for('login'))

        @app.route('/band/new', methods=['POST', 'GET'])
        def newBand():
            if "user" in session:
                user: User or None = session["user"]
                nonce = user.getNonce()
                errors = []
                f = {}
                if request.method == "POST":
                    f = MultiDict(request.form.items(multi=True))
                    if f["nonce"] == nonce:
                        user.delNonce()
                        band = Band(f)
                        band.addOwner(user)
                        if len(band.errors) == 0:
                            band = Band.register(band)
                            if band:
                                return redirect(url_for('bandPage', id=band.id))
                        else:
                            errors.extend(band.errors)
                    else:
                        flash(_("Bad nonce!"), "danger")
                f["nonce"] = nonce
                return Band.renderNew(user, f, errors)
            return redirect(url_for('login'))
