
from flask.app import Flask
from db import Model, Database, devListJSON, devSetResponse
from flask import render_template, request, session, redirect, url_for, flash
import os
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from user import User
from copy import Error, error
from upload import Upload
from typing import *

MissingName = Error(_("Missing name string!"))
MissingLive = Error(_("Missing live boolean!"))
MissingEmail = Error(_("Missing email string!"))
MissingWebsite = Error(_("Missing website string!"))
MissingHistory = Error(_("Missing history list!"))
MissingStats = Error(_("Missing stats list!"))
MissingSecret = Error(_("Missing secret string!"))

InvalidUser = Error(_("Invalid user!"))
InvalidIcon = Error(_("Invalid icon!"))

class API(Model):

    def testName(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingName)

    def testLive(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, bool):
            errors.append(MissingLive)

    def testEmail(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingEmail)

    def testWebsite(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingWebsite)

    def testHistory(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingHistory)

    def testStats(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingStats)

    def testSecret(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str):
            errors.append(MissingSecret)

    def testUser(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str) or not isinstance(value, User):
            errors.append(InvalidUser)

    def testIcon(form: Any, value: Any, errors: list):
        # TODO: Check if venue exists
        if not isinstance(value, str) or not isinstance(value, Upload) or not None:
            errors.append(InvalidIcon)

    name = Model.newProp("name", None, testName, "Name of the App")
    live = Model.newProp("live", False, testLive, "Should the API apply data?")
    email = Model.newProp("email", None, testEmail, "Email of the dev")
    website = Model.newProp("website", None, testWebsite, "Website of App")
    history = Model.newProp("history", [], testHistory, "History of requests")
    stats = Model.newProp("stats", [], testStats, "Stats for rates and info")
    secret = Model.newProp("secret", None, testSecret, "Given to user")
    user = Model.newProp("user", None, testUser, "HTML details on the event")
    icon = Model.newProp("icon", None, testIcon, "Icon of the App")

    def resolve(input: Any):
        return Model.resolve(API, input)
        
    def setResponse(self: Model, user: Any, include: List[str or Type[Model]], resp: Dict = {}):
        return devSetResponse({
            "user": User,
            "icon": Upload
        })(self, user, include, resp)

    def filter(self, user: Any) -> Any:
        data = Model.filter(self, user)
        if user is not User:
            del data["email"]
            del data["user"]
            del data["history"]
            del data["stats"]
            del data["secret"]
        elif user.id != self.user and not user.admin:
            del data["email"]
            del data["history"]
            del data["stats"]
            del data["secret"]
        return data

    def __init__(self, data: Any):
        super().__init__(Model.setResolve(data, {
            "icon": Upload
        }))

    def findOne(criteria: Any):
        return Database.main.findOne(API, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(API, criteria)

    def renderCard(self):
        return render_template("apiCard.html.j2", api=self)

    def renderDelete(user: User, apis: list, nonce: str):
        return render_template("apiDelete.html.j2", user=user, apis=apis, nonce=nonce)

    def renderEdit(user: User, api: Any, form: Any, errors: list):
        return render_template("apiEdit.html.j2", user=user, api=api, form=form, errors=errors)

    def renderForm(user: User, form: Any, errors: list):
        return render_template("apiForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: User, apis: list):
        return render_template("apiList.html.j2", user=user, apis=apis)

    def renderNew(user: User, form: Any, errors: list):
        return render_template("apiNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: User, api: Any):
        return render_template("apiPage.html.j2", user=user, api=api)

    def setupApp(app: Flask):
        @app.route("/api/<id>")
        def apiPage(id):
            user = None
            if "user" in session:
                user = session["user"]
            api = API.findOne({"_id": id})
            if api is None:
                return redirect(url_for('indexGET'))
            return API.renderPage(user, api)

        @app.route("/api/<id>/edit", methods=['POST', 'GET'])
        def editAPI(id):
            user = None
            form = {}
            errors = []
            if "user" in session:
                user = session["user"]
                api = API.findOne({"_id": id, "owner": user.id})
                if api is None:
                    return redirect(url_for('listAPI'))
                if request.method == "POST":
                    form = request.form
                    if form["nonce"] != user.nonce:
                        flash(_("Bad nonce!"), "danger")
                    else:
                        del user.nonce
                        api.apply(form)
                        if len(api.errors) == 0:
                            api.save()
                        else:
                            errors.extend(api.errors)
                form["nonce"] = user.nonce
                return API.renderEdit(user, api, form, errors)
            return redirect(url_for('login'))

        @app.route("/api/list")
        def listAPI():
            if "user" in session:
                user = session["user"]
                if user:
                    apis = API.findMany({"owner": user.id})
                    return API.renderList(user, apis)
            return redirect(url_for('login'))

        @app.route("/api/list.json")
        def listAPIJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return devListJSON(user, request, API, [Upload])
            return redirect(url_for('login')), 401

        @app.route("/api/delete")
        def deleteAPI():
            if "user" in session:
                nonce = None
                user = session["user"]
                if user:
                    nonce = user.nonce
                    items = request.args["items"]
                    apis = API.findMany({"_id": items, "owner": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            del user.nonce
                            for api in apis:
                                api.remove()
                            l = len(apis)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listAPI'))
                    return API.renderDelete(user, apis, nonce)
            return redirect(url_for('login'))

        @app.route('/api/new', methods=['POST', 'GET'])
        def newAPI():
            if "user" in session:
                user = session["user"]
                nonce = user.nonce
                errors = []
                form = {}
                if request.method == "POST":
                    form = request.form
                    if form["nonce"] == nonce:
                        api = API(form)
                        if len(api.errors) == 0:
                            api = API.register(api)
                            if api:
                                return redirect(url_for('apiPage', id=api.id))
                        else:
                            errors.extend(api.errors)
                    else:
                        flash(_("Bad nonce!"), "danger")
                form["nonce"] = nonce
                return API.renderNew(user, form, errors)
            return redirect(url_for('login'))
