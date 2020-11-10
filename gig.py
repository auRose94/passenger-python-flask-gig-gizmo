
from flask.app import Flask
from db import Model, Database, devListJSON, devSetResponse
from flask import render_template, request, session, redirect, url_for, flash
import os
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from user import User
from venue import Venue
from band import Band
from copy import Error
from location import Location
from typing import *

MissingVenue = Error(_("Missing venue!"))
MissingLocation = Error(_("Missing location from venue!"))
MissingStart = Error(_("Missing start time and date!"))
MissingStop = Error(_("Missing stop time and date!"))

InvalidInfo = Error(_("Invalid info!"))
InvalidBands = Error(_("Invalid bands!"))
InvalidOwners = Error(_("Invalid owners!"))

class Gig(Model):

    def testVenue(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingVenue)

    def testLocation(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingVenue)

    def testBands(form: Any, value: Any, errors: list):
        # TODO: Check if all bands exist
        if not isinstance(value, list):
            errors.append(InvalidBands)

    def testOwners(form: Any, value: Any, errors: list):
        # TODO: Check if all bands exist
        if not isinstance(value, list):
            errors.append(InvalidOwners)

    def testStart(form: Any, value: Any, errors: list):
        # TODO: Parse date-time format
        if not isinstance(value, str):
            errors.append(MissingStart)

    def testStop(form: Any, value: Any, errors: list):
        # TODO: Parse date-time format
        if not isinstance(value, str):
            errors.append(MissingStop)

    def testInfo(form: Any, value: Any, errors: list):
        # TODO: check if valid html
        if not isinstance(value, str):
            errors.append(InvalidInfo)

    venue = Model.newProp("venue", None, testVenue, "The id of venue")
    location = Model.newProp("location", None, testLocation, "Venue location")
    bands = Model.newProp("bands", [], testBands, "The list of band ids")
    owners = Model.newProp("owners", [], testOwners, "Owners of the bands and venues")
    start = Model.newProp("start", None, testStart, "The starting time")
    stop = Model.newProp("stop", None, testStop, "The stopping time")
    info = Model.newProp("info", "", testInfo, "HTML details on the event")

    def resolve(input: Any):
        return Model.resolve(Gig, input)
        
    def setResponse(self, include, resp):
        return devSetResponse({
            "venue": Venue,
            "bands": [Band],
            "owners": [User],
            "location": Location
        })(self, include, resp)

    def __init__(self, data: Any):
        super().__init__(Model.setResolve(data, {
            "location": Location
        }))

    def findOne(criteria: Any):
        return Database.main.findOne(Gig, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(Gig, criteria)

    def renderCard(self, bands: Dict[str, Band], venue: Venue):
        return render_template("gigCard.html.j2", gig=self, bands=bands, venue=venue)

    def renderDelete(user: User, gigs: list, bands: Dict[str, Band], venues: Dict[str, Venue], nonce: str):
        return render_template("gigDelete.html.j2", user=user, gigs=gigs, bands=bands, venues=venues, nonce=nonce)

    def renderEdit(user: User, gig: Any, form: Any, errors: list):
        return render_template("gigEdit.html.j2", user=user, gig=gig, form=form, errors=errors)

    def renderForm(user: User, form: Any, errors: list):
        return render_template("gigForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: User, gigs: list, bands: Dict[str, Band], venues: Dict[str, Venue]):
        return render_template("gigList.html.j2", user=user, gigs=gigs, bands=bands, venues=venues)

    def renderNew(user: User, form: Any, errors: list):
        return render_template("gigNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: User, gig: Any, bands: Dict[str, Band], venue: Venue):
        return render_template("gigPage.html.j2", user=user, gig=gig, bands=bands, venue=venue)

    def setupApp(app: Flask):
        @app.route("/gig/<id>")
        def gigPage(id):
            user = None
            if "user" in session:
                user = session["user"]
            gig = Gig.findOne({"_id": id})
            if gig is None:
                return redirect(url_for('indexGET'))
            return Gig.renderPage(user, gig)

        @app.route("/gig/<id>/edit", methods=['POST', 'GET'])
        def editGig(id):
            user = None
            form = {}
            errors = []
            if "user" in session:
                user = session["user"]
                gig = Gig.findOne({"_id": id, "owner": user.id})
                if gig is None:
                    return redirect(url_for('listGig'))
                if request.method == "POST":
                    form = request.form
                    if form["nonce"] != user.nonce:
                        flash(_("Bad nonce!"), "danger")
                    else:
                        del user.nonce
                        gig.apply(form)
                        if len(gig.errors) == 0:
                            gig.save()
                        else:
                            errors.extend(gig.errors)
                form["nonce"] = user.nonce
                return Gig.renderEdit(user, gig, form, errors)
            return redirect(url_for('login'))

        @app.route("/gig/list")
        def listGig():
            if "user" in session:
                user = session["user"]
                if user:
                    gigs = Gig.findMany({"owner": user.id})
                    bandIds = []
                    venueIds = []
                    for gig in gigs:
                        if gig.venue not in venueIds:
                            venueIds.append(gig.venue)
                        for bid in gig.bands:
                            if bid not in bandIds:
                                bandIds.append(bid)
                    bands = Band.findMany({"_id": bandIds})
                    venues = Venue.findMany({"_id": venueIds})
                    def ModelMap(item):
                        return [item.id, item]
                    bands = dict(map(ModelMap, bands))
                    venues = dict(map(ModelMap, venues))
                    return Gig.renderList(user, gigs, bands, venues)
            return redirect(url_for('login'))

        @app.route("/gig/list.json")
        def listGigJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return devListJSON(user, request, Gig, [Gig, Band, Venue, Location])
            return redirect(url_for('login')), 401

        @app.route("/gig/delete")
        def deleteGig():
            if "user" in session:
                nonce = None
                user = session["user"]
                if user:
                    nonce = user.nonce
                    items = request.args["items"]
                    gigs = Gig.findMany({"_id": items, "owner": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            del user.nonce
                            for gig in gigs:
                                gig.remove()
                            l = len(gigs)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listGig'))
                    return Gig.renderDelete(user, gigs, nonce)
            return redirect(url_for('login'))

        @app.route('/gig/new', methods=['POST', 'GET'])
        def newGig():
            if "user" in session:
                user = session["user"]
                nonce = user.nonce
                errors = []
                form = {}
                if request.method == "POST":
                    form = request.form
                    if form["nonce"] == nonce:
                        gig = Gig(form)
                        if len(gig.errors) == 0:
                            gig = Gig.register(gig)
                            if gig:
                                return redirect(url_for('gigPage', id=gig.id))
                        else:
                            errors.extend(gig.errors)
                    else:
                        flash(_("Bad nonce!"), "danger")
                form["nonce"] = nonce
                return Gig.renderNew(user, form, errors)
            return redirect(url_for('login'))
