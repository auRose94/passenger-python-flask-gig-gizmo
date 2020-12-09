
from flask.app import Flask
from flask import render_template, request, session, redirect, url_for, flash
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from werkzeug.datastructures import MultiDict
from user import User
from copy import Error
from typing import *
import mongoengine as me

MissingName = Error(_("Missing name string!"))
MissingLive = Error(_("Missing live boolean!"))
MissingEmail = Error(_("Missing email string!"))
MissingWebsite = Error(_("Missing website string!"))
MissingHistory = Error(_("Missing history list!"))
MissingStats = Error(_("Missing stats list!"))
MissingSecret = Error(_("Missing secret string!"))

InvalidUser = Error(_("Invalid user!"))
InvalidIcon = Error(_("Invalid icon!"))

class API(me.Document):
    name = me.StringField(required=True)
    live = me.BooleanField(default=False)
    email = me.EmailField(allow_utf8_user=True)
    website = me.URLField()
    history = me.ListField(me.DictField())
    stats = me.DictField()
    secret = me.StringField()
    owners = me.ListField(me.ReferenceField("User", passthrough=True, reverse_delete_rule=me.NULLIFY))
    icon = me.ImageField(size=(1024, 1024, True),
                         thumbnail_size=(128, 128, True))

    def renderCard(self):
        return render_template("apiCard.html.j2", api=self)

    def renderDelete(user: User, apis: list, nonce: str):
        return render_template("apiDelete.html.j2", user=user, apis=apis, nonce=nonce)

    def renderEdit(user: User, api: Any, nonce: str, form: Any, errors: list):
        return render_template("apiEdit.html.j2", user=user, api=api, form=form, errors=errors, nonce=nonce)

    def renderForm(user: User, nonce: str, form: Any, errors: list):
        return render_template("apiForm.html.j2", user=user, form=form, errors=errors, nonce=nonce)

    def renderList(user: User, apis: list):
        return render_template("apiList.html.j2", user=user, apis=apis)

    def renderNew(user: User, nonce: str, form: Any, errors: list):
        return render_template("apiNew.html.j2", user=user, form=form, errors=errors, nonce=nonce)

    def renderPage(user: User, api: Any):
        return render_template("apiPage.html.j2", user=user, api=api)

    def setupApp(app: Flask):
        @app.route("/api/<id>")
        def apiPage(id):
            user: User or None = None
            if "user" in session:
                user = session["user"]
            api = API.objects(_id=id).first()
            if api is None:
                return redirect(url_for('indexGET'))
            return API.renderPage(user, api)

        @app.route("/api/<id>/edit", methods=['POST', 'GET'])
        def editAPI(id):
            user = None
            f = {}
            errors = {}
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    api: API or None = API.objects(_id=id, owners=user.id).first()
                    if api is None:
                        return redirect(url_for('listAPI'))
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        for key, value in f.items(multi=True):
                            user[key] = value
                        if f["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            try:
                                api.validate()
                            except me.ValidationError as err:
                                errors[err.field_name] = err.message
                            else:
                                api.save()
                    return API.renderEdit(user, nonce, api, f, errors)
            return redirect(url_for('login'))

        @app.route("/api/list")
        def listAPIJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return API.renderList(user)
            return redirect(url_for('login'))

        @app.route("/api/list.json")
        def listAPI():
            if "user" in session:
                user = session["user"]
                if user:
                    apis: me.Document = API.select_related()
                    limit = 0
                    skip = 0
                    text = None
                    if "limit" in request.args and int(request.args["limit"]) > 0:
                        limit = int(request.args["limit"])
                    if "offset" in request.args and int(request.args["offset"]) > 0:
                        skip = int(request.args["offset"])
                    if "search" in request.args and request.args["search"] != "":
                        text = request.args["search"]
                    apis.objects(owners=user.id).limit(limit).skip(0)
                    resp = {}
                    resp["total"] = len(apis)
                    resp["rows"] = apis
                    return resp, 200
            return redirect(url_for('login')), 401

        @app.route("/api/delete")
        def deleteAPI():
            if "user" in session:
                nonce = None
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    items = request.args["items"]
                    apis: List[API] = API.objects(_id=items, owners=user.id)
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            user.delNonce()
                            for api in apis:
                                api.delete()
                            l = len(apis)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listAPI'))
                    return API.renderDelete(user, nonce, apis)
            return redirect(url_for('login'))

        @app.route('/api/new', methods=['POST', 'GET'])
        def newAPI():
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
                            api = API.register(f, user)
                        except me.ValidationError as err:
                            errors[err.field_name] = err.message
                        else:
                            if api:
                                return redirect(url_for('apiPage', id=api.id))
                    else:
                        flash(_("Bad nonce!"), "danger")
                f["nonce"] = nonce
                return API.renderNew(user, f, errors), 200
            return redirect(url_for('login'))
