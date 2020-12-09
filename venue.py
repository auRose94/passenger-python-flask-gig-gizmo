
import json
from location import Location
from forms.delete import DeleteForm
from forms.venue import VenueForm
from flask import Flask
from flask import render_template, request, session, redirect, url_for, flash
from datetime import *
from dateutil.parser import *
from flask_babel import gettext as _
from user import User
from typing import *
import mongoengine as me

class Venue(me.Document):
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
    owners = me.ListField(me.ReferenceField(
        "User", passthrough=True, reverse_delete_rule=me.NULLIFY))
    hide = me.BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ["$perma", "$email", "$phone", '$name', "$desc", "$short", "$tags"],
         'default_language': "english",
         'weights': {"perma": 10, 'name': 9, 'tags': 9, 'email': 8, 'phone': 8, 'desc': 5, 'desc': 5}
         }
    ]}


def renderCard(venue: Venue):
    return render_template("venueCard.html.j2", venue=venue)


def renderDelete(user: User, venues: List[Venue]):
    return render_template("venueDelete.html.j2", user=user, venues=venues)


def renderEdit(user: User, venue: Venue):
    return render_template("venueEdit.html.j2", user=user, venue=venue)


def renderForm(user: User, form: VenueForm):
    return render_template("venueForm.html.j2", user=user, form=form)


def renderList(user: User):
    return render_template("venueList.html.j2", user=user)


def renderNew(user: User, form: VenueForm):
    return render_template("venueNew.html.j2", user=user, form=form)


def renderPage(user: User, venue: Venue):
    return render_template("venuePage.html.j2", user=user, venue=venue)


def register(form: VenueForm, user: User):
    icon = form.icon
    if icon.data == "":
        icon = None
    photos = form.photos
    if len(photos.data) == 1 and photos.data[0] == "":
        photos=None
    location = Location.register(form.location.form)

    item = Venue(
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

    @app.route("/venue/<id>")
    def venuePage(id: str):
        user: User or None = None
        if "user" in session:
            user = session["user"]
        venue = Venue.objects(id=id).first()
        if venue is None:
            return redirect(url_for('indexGET'))
        return Venue.renderPage(user, venue)

    @app.route("/venue/<id>/edit", methods=['POST', 'GET'])
    def editVenue(id: str):
        user = None
        if "user" in session:
            user: User or None = session["user"]
            if isinstance(user, User):
                venue: Venue or None = Venue.objects(
                    id=id, owners=user.id).first()
                if venue is None:
                    return redirect(url_for('listVenue'))
                f = VenueForm(request.form, venue)
                if request.method == "POST":
                    try:
                        venue.validate()
                    except me.ValidationError:
                        flash(
                            _("Please correctly fill everything required."), "danger")
                    else:
                        venue.save()
                return Venue.renderEdit(user, venue, f)
        return redirect(url_for("userLogin"))

    @app.route("/venue/list")
    def listVenueJSON():
        if "user" in session:
            user = session["user"]
            if user:
                return Venue.renderList(user)
        return redirect(url_for("userLogin"))

    @app.route("/venue/list.json")
    def listVenue():
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
                venues = Venue.objects(owners=user.id).limit(limit).skip(skip)
                resp = {}
                resp["total"] = len(venues)
                resp["rows"] = venues
                return resp, 200
        return redirect(url_for("userLogin")), 401

    @app.route("/venue/delete")
    def deleteVenue():
        if "user" in session:
            user: User or None = session["user"]
            f = DeleteForm(request.form)
            f.items = request.args["items"]
            f.model = "Venue"
            if isinstance(user, User):
                items = request.args["items"]
                venues: List[Venue] = Venue.objects(id=items, owners=user.id)
                if request.method == "POST":
                    for venue in venues:
                        venue.delete()
                    count = len(venues)
                    if count > 1:
                        flash(_("Removed %(count) items!", count=count), "success")
                    else:
                        flash(_("Removed item!"), "success")
                    return redirect(url_for('listVenue'))
                return Venue.renderDelete(user, venues)
        return redirect(url_for("userLogin"))

    @app.route('/venue/new', methods=['POST', 'GET'])
    def newVenue():
        if "user" in session:
            user: User = session["user"]
            f = VenueForm(request.form)
            if request.method == "POST":
                try:
                    venue = Venue.register(f, user)
                except me.ValidationError as err:
                    flash(_("Please correctly fill everything required."), "danger")
                else:
                    if venue:
                        return redirect(url_for('venuePage', id=venue.id))
            return Venue.renderNew(user, f), 200
        return redirect(url_for("userLogin"))


Venue.renderCard = renderCard
Venue.renderDelete = renderDelete
Venue.renderEdit = renderEdit
Venue.renderForm = renderForm
Venue.renderList = renderList
Venue.renderNew = renderNew
Venue.renderPage = renderPage
Venue.register = register
Venue.setupApp = setupApp
