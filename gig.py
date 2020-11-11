
from flask.app import Flask
from werkzeug.datastructures import MultiDict
from flask import render_template, request, session, redirect, url_for, flash
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from user import User
from venue import Venue
from band import Band
from typing import *
import mongoengine as me

class Gig(me.Document):
    venue = me.LazyReferenceField(
        "Venue", passthrough=True, reverse_delete_rule=me.NULLIFY)
    location = me.LazyReferenceField(
        "Location", passthrough=True, reverse_delete_rule=me.NULLIFY)
    bands = me.ListField(me.LazyReferenceField("Band", passthrough=True, reverse_delete_rule=me.NULLIFY))
    owners = me.ListField(me.ReferenceField("User", passthrough=True, reverse_delete_rule=me.NULLIFY))
    start = me.DateTimeField()
    stop = me.DateTimeField()
    info = me.StringField(required=True, max_length=1024*8)

    def renderCard(self, bands: Dict[str, Band], venue: Venue):
        return render_template("gigCard.html.j2", gig=self, bands=bands, venue=venue)

    def renderDelete(user: User, nonce: str, gigs: list, bands: Dict[str, Band], venues: Dict[str, Venue]):
        return render_template("gigDelete.html.j2", user=user, gigs=gigs, bands=bands, venues=venues, nonce=nonce)

    def renderEdit(user: User, nonce: str, gig: Any, form: Any, errors: list):
        return render_template("gigEdit.html.j2", user=user, gig=gig, form=form, errors=errors, nonce=nonce)

    def renderForm(user: User, nonce: str, form: Any, errors: list):
        return render_template("gigForm.html.j2", user=user, form=form, errors=errors, nonce=nonce)

    def renderList(user: User, gigs: list, bands: Dict[str, Band], venues: Dict[str, Venue]):
        return render_template("gigList.html.j2", user=user, gigs=gigs, bands=bands, venues=venues)

    def renderNew(user: User, nonce: str, form: Any, errors: list):
        return render_template("gigNew.html.j2", user=user, form=form, errors=errors, nonce=nonce)

    def renderPage(user: User, gig: Any, bands: Dict[str, Band], venue: Venue):
        return render_template("gigPage.html.j2", user=user, gig=gig, bands=bands, venue=venue)

    def setupApp(app: Flask):

        @app.route("/gig/<id>")
        def gigPage(id):
            user: User or None = None
            if "user" in session:
                user = session["user"]
            gig = Gig.object({"_id": id})
            if gig is None:
                return redirect(url_for('indexGET'))
            return Gig.renderPage(user, gig)

        @app.route("/gig/<id>/edit", methods=['POST', 'GET'])
        def editGig(id):
            user = None
            f = {}
            errors = {}
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    gig: Gig or None = Gig.object({"_id": id, "owners": user.id})
                    if gig is None:
                        return redirect(url_for('listGig'))
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        for key, value in f.items(multi=True):
                            user[key] = value
                        if f["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            try:
                                gig.validate()
                            except me.ValidationError as err:
                                errors[err.field_name] = err.message
                            else:
                                gig.save()
                    return Gig.renderEdit(user, nonce, gig, f, errors)
            return redirect(url_for('login'))

        @app.route("/gig/list")
        def listGigJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return Gig.renderList(user)
            return redirect(url_for('login'))

        @app.route("/gig/list.json")
        def listGig():
            if "user" in session:
                user = session["user"]
                if user:
                    gigs: me.Document = Gig.select_related()
                    limit = 0
                    skip = 0
                    text = None
                    if "limit" in request.args and int(request.args["limit"]) > 0:
                        limit = int(request.args["limit"])
                    if "offset" in request.args and int(request.args["offset"]) > 0:
                        skip = int(request.args["offset"])
                    if "search" in request.args and request.args["search"] != "":
                        text = request.args["search"]
                    gigs.objects({"owners": user.id}).limit(limit).skip(0)
                    resp = {}
                    resp["total"] = len(gigs)
                    resp["rows"] = gigs
                    return resp, 200
            return redirect(url_for('login')), 401

        @app.route("/gig/delete")
        def deleteGig():
            if "user" in session:
                nonce = None
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    items = request.args["items"]
                    gigs: List[Gig] = Gig.objects({"_id": items, "owners": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            for gig in gigs:
                                gig.delete()
                            l = len(gigs)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listGig'))
                    return Gig.renderDelete(user, nonce, gigs)
            return redirect(url_for('login'))

        @app.route('/gig/new', methods=['POST', 'GET'])
        def newGig():
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
                            gig = Gig.register(f, user)
                        except me.ValidationError as err:
                            errors[err.field_name] = err.message
                        else:
                            if gig:
                                return redirect(url_for('gigPage', id=gig.id))
                    else:
                        flash(_("Bad nonce!"), "danger")
                f["nonce"] = nonce
                return Gig.renderNew(user, f, errors), 200
            return redirect(url_for('login'))
