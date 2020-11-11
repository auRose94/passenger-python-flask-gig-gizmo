
from typing import *
from flask import Flask
from werkzeug.datastructures import MultiDict
from flask import render_template, request, session, redirect, url_for, flash
from datetime import *
from dateutil.parser import *
from flask_babel import gettext as _
from user import User
import mongoengine as me

class Band(me.Document):
    name = me.StringField(required=True)
    perma = me.StringField(required=True)
    url = me.URLField()
    email = me.EmailField(required=True)
    phone = me.EmailField(required=True)
    location = me.LazyReferenceField(
        "Location", passthrough=True, reverse_delete_rule=me.CASCADE)
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

    def renderCard(band: Any):
        return render_template("bandCard.html.j2", band=band)

    def renderDelete(user: User, nonce: str, bands: Any):
        return render_template("bandDelete.html.j2", user=user, bands=bands)

    def renderEdit(user: User, nonce: str, band: Any):
        return render_template("bandEdit.html.j2", user=user, band=band)

    def renderForm(user: User, nonce: str, form: Any, errors: list):
        return render_template("bandForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: User, bands: list):
        return render_template("bandList.html.j2", user=user, bands=bands)

    def renderNew(user: User, nonce: str, form: Any, errors: list):
        return render_template("bandNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: User, band: Any):
        return render_template("bandPage.html.j2", user=user, band=band)

    def register(form: Any, user: User):
        band = Band(form)
        band.owners.append(user.id)
        band.validate()
        return band.save()

    def setupApp(app: Flask):

        @app.route("/band/<id>")
        def bandPage(id):
            user: User or None = None
            if "user" in session:
                user = session["user"]
            band = Band.object({"_id": id})
            if band is None:
                return redirect(url_for('indexGET'))
            return Band.renderPage(user, band)

        @app.route("/band/<id>/edit", methods=['POST', 'GET'])
        def editBand(id):
            user = None
            f = {}
            errors = {}
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    band: Band or None = Band.object({"_id": id, "owners": user.id})
                    if band is None:
                        return redirect(url_for('listBand'))
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        for key, value in f.items(multi=True):
                            user[key] = value
                        if f["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            try:
                                band.validate()
                            except me.ValidationError as err:
                                errors[err.field_name] = err.message
                            else:
                                band.save()
                    return Band.renderEdit(user, nonce, band, f, errors)
            return redirect(url_for('login'))

        @app.route("/band/list")
        def listBandJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return Band.renderList(user)
            return redirect(url_for('login'))

        @app.route("/band/list.json")
        def listBand():
            if "user" in session:
                user = session["user"]
                if user:
                    bands: me.Document = Band.select_related()
                    limit = 0
                    skip = 0
                    text = None
                    if "limit" in request.args and int(request.args["limit"]) > 0:
                        limit = int(request.args["limit"])
                    if "offset" in request.args and int(request.args["offset"]) > 0:
                        skip = int(request.args["offset"])
                    if "search" in request.args and request.args["search"] != "":
                        text = request.args["search"]
                    bands.objects({"owners": user.id}).limit(limit).skip(0)
                    resp = {}
                    resp["total"] = len(bands)
                    resp["rows"] = bands
                    return resp, 200
            return redirect(url_for('login')), 401

        @app.route("/band/delete")
        def deleteBand():
            if "user" in session:
                nonce = None
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    items = request.args["items"]
                    bands: List[Band] = Band.objects({"_id": items, "owners": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            for band in bands:
                                band.delete()
                            l = len(bands)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listBand'))
                    return Band.renderDelete(user, nonce, bands)
            return redirect(url_for('login'))

        @app.route('/band/new', methods=['POST', 'GET'])
        def newBand():
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
                            band = Band.register(f, user)
                        except me.ValidationError as err:
                            errors[err.field_name] = err.message
                        else:
                            if band:
                                return redirect(url_for('bandPage', id=band.id))
                    else:
                        flash(_("Bad nonce!"), "danger")
                f["nonce"] = nonce
                return Band.renderNew(user, f, errors), 200
            return redirect(url_for('login'))
