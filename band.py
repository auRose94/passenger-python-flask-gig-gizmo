
from location import Location
from typing import *
from flask import Flask
from flask import render_template, request, session, redirect, url_for, flash
from datetime import *
from dateutil.parser import *
from flask_babel import gettext as _
from user import User
from forms.band import BandForm
from forms.delete import DeleteForm
import mongoengine as me

class Band(me.Document):
    name = me.StringField(required=True)
    perma = me.StringField(required=True)
    url = me.URLField()
    email = me.EmailField(required=True)
    phone = me.StringField(required=True)
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


def renderCard(band: Band):
    return render_template("bandCard.html.j2", band=band)


def renderDelete(user: User, bands: List[Band]):
    return render_template("bandDelete.html.j2", user=user, bands=bands)


def renderEdit(user: User, band: Band):
    return render_template("bandEdit.html.j2", user=user, band=band)


def renderForm(user: User, form: BandForm):
    return render_template("bandForm.html.j2", user=user, form=form)


def renderList(user: User):
    return render_template("bandList.html.j2", user=user)


def renderNew(user: User, form: BandForm):
    return render_template("bandNew.html.j2", user=user, form=form)


def renderPage(user: User, band: Band):
    return render_template("bandPage.html.j2", user=user, band=band)


def register(form: BandForm, user: User):
    icon = form.icon
    if icon.data == "":
        icon = None
    photos = form.photos
    if len(photos.data) == 1 and photos.data[0] == "":
        photos=None
    location = Location.register(form.location.form)

    item = Band(
        name=form.name.data,
        perma=form.perma.data,
        url=form.url.data,
        email=form.email.data,
        phone=form.phone.data,
        location=location.id,
        desc=form.desc.data,
        short=form.short.data,
        tags=form.tags.data,
        icon=icon,
        photos=photos,
        owners=form.owners.data,
        hide=form.hide.data
    )
    try:
        ownerIndex = item.owners.index(user.id)
        if ownerIndex < 0:
            item.owners.append(user.id)
    except ValueError:
        item.owners.append(user.id)
    item.validate(clean=True)
    return item.save()


def setupApp(app: Flask):

    @app.route("/band/<id>")
    def bandPage(id: str):
        user: User or None = None
        if "user" in session:
            user = session["user"]
        band = Band.objects(id=id).first()
        if band is None:
            return redirect(url_for('indexGET'))
        return Band.renderPage(user, band)

    @app.route("/band/<id>/edit", methods=['POST', 'GET'])
    def editBand(id: str):
        user = None
        if "user" in session:
            user: User or None = session["user"]
            if isinstance(user, User):
                band: Band or None = Band.objects(
                    id=id, owners=user.id).first()
                if band is None:
                    return redirect(url_for('listBand'))
                f = BandForm(request.form, band)
                if request.method == "POST":
                    try:
                        band.validate()
                    except me.ValidationError:
                        flash(
                            _("Please correctly fill everything required."), "danger")
                    else:
                        band.save()
                return Band.renderEdit(user, band, f)
        return redirect(url_for("userLogin"))

    @app.route("/band/list")
    def listBandJSON():
        if "user" in session:
            user = session["user"]
            if user:
                return Band.renderList(user)
        return redirect(url_for("userLogin"))

    @app.route("/band/list.json")
    def listBand():
        if "user" in session:
            user = session["user"]
            if user:
                limit = 0
                skip = 0
                text = None
                if "limit" in request.args and int(request.args["limit"]) > 0:
                    limit = int(request.args["limit"])
                if "offset" in request.args and int(request.args["offset"]) > 0:
                    skip = int(request.args["offset"])
                if "search" in request.args and request.args["search"] != "":
                    text = request.args["search"]
                bands = Band.objects(owners=user.id).limit(limit).skip(skip)
                resp = {}
                resp["total"] = len(bands)
                resp["rows"] = bands
                return resp, 200
        return redirect(url_for("userLogin")), 401

    @app.route("/band/delete")
    def deleteBand():
        if "user" in session:
            user: User or None = session["user"]
            f = DeleteForm(request.form)
            f.items = request.args["items"]
            f.model = "Band"
            if isinstance(user, User):
                items = request.args["items"]
                bands: List[Band] = Band.objects(id=items, owners=user.id)
                if request.method == "POST":
                    for band in bands:
                        band.delete()
                    count = len(bands)
                    if count > 1:
                        flash(_("Removed %(count) items!", count=count), "success")
                    else:
                        flash(_("Removed item!"), "success")
                    return redirect(url_for('listBand'))
                return Band.renderDelete(user, bands)
        return redirect(url_for("userLogin"))

    @app.route('/band/new', methods=['POST', 'GET'])
    def newBand():
        if "user" in session:
            user: User = session["user"]
            f = BandForm(request.form)
            if request.method == "POST":
                try:
                    band = Band.register(f, user)
                except me.ValidationError:
                    flash(_("Please correctly fill everything required."), "danger")
                else:
                    if band:
                        return redirect(url_for('bandPage', id=band.id))
            return Band.renderNew(user, f), 200
        return redirect(url_for("userLogin"))

Band.renderCard = renderCard
Band.renderDelete = renderDelete
Band.renderEdit = renderEdit
Band.renderForm = renderForm
Band.renderList = renderList
Band.renderNew = renderNew
Band.renderPage = renderPage
Band.register = register
Band.setupApp = setupApp