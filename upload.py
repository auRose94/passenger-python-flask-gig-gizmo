
from flask.app import Flask
from db import Model, Database, devListJSON, devSetResponse
from flask import render_template, request, session, redirect, url_for, flash
import os
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from copy import Error, error
from typing import *

MissingOwners = Error(_("Missing owners array!"))
MissingName = Error(_("Missing name string!"))
MissingFile = Error(_("Missing file string!"))
MissingWidth = Error(_("Missing width number!"))
MissingHeight = Error(_("Missing height number!"))
MissingMIME = Error(_("Missing mime string!"))
MissingInfo = Error(_("Missing info string!"))
MissingHash = Error(_("Missing hash string!"))


class Upload(Model):
    def testOwners(form: Any, value: Any, errors: list):
        # TODO: Check if owners exist
        if not isinstance(value, list):
            errors.append(MissingOwners)

    def testName(form: Any, value: Any, errors: list):
        # TODO: Check if file exists or valid
        if not isinstance(value, str):
            errors.append(MissingName)

    def testFile(form: Any, value: Any, errors: list):
        # TODO: Check if file exists or valid
        if not isinstance(value, str):
            errors.append(MissingFile)

    def testWidth(form: Any, value: Any, errors: list):
        if not isinstance(value, int):
            errors.append(MissingWidth)

    def testHeight(form: Any, value: Any, errors: list):
        if not isinstance(value, int):
            errors.append(MissingHeight)

    def testMIME(form: Any, value: Any, errors: list):
        # TODO: Check if valid MIME type
        if not isinstance(value, str):
            errors.append(MissingMIME)

    def testInfo(form: Any, value: Any, errors: list):
        # TODO: Apply limit to info
        if not isinstance(value, str):
            errors.append(MissingInfo)

    def testHash(form: Any, value: Any, errors: list):
        # TODO: Check if file hash works
        if not isinstance(value, str):
            errors.append(MissingHash)

    owners = Model.newProp("owners", [], testOwners,
                           "Owners who have rights to this.")
    name = Model.newProp("name", "", testName,
                         "Name given when uploaded to server")
    file = Model.newProp("file", None, testFile, "File location in server")
    width = Model.newProp("width", None, testWidth, "Photo pixel width")
    height = Model.newProp("height", None, testHeight, "Photo pixel height")
    mime = Model.newProp("mime", None, testMIME, "Photo MIME type")
    info = Model.newProp("info", "", testInfo, "Text description of upload")
    hash = Model.newProp("hash", None, testHash,
                         "Hash of upload, generated if blank and new")

    def renderCard(self):
        return render_template("uploadCard.html.j2", upload=self)

    def renderDelete(user: Model, nonce: str):
        return render_template("uploadDelete.html.j2", user=user, nonce=nonce)

    def renderEdit(user: Model, upload: Any, form: Any, errors: list):
        return render_template("uploadEdit.html.j2", user=user, upload=upload, form=form, errors=errors)

    def renderForm(user: Model, form: Any, errors: list):
        return render_template("uploadForm.html.j2", user=user, form=form, errors=errors)

    def renderList(user: Model, uploads: list):
        return render_template("uploadList.html.j2", user=user, uploads=uploads)

    def renderNew(user: Model, form: Any, errors: list):
        return render_template("uploadNew.html.j2", user=user, form=form, errors=errors)

    def renderPage(user: Model, upload: Any):
        return render_template("uploadPage.html.j2", user=user, upload=upload)

    def resolve(input: Any):
        return Model.resolve(Upload, input)

    def filter(self, user: Any) -> Any:
        data = Model.filter(self, user)
        if user is not Model:
            del data["owners"]
        elif not user.admin and not self.isOwner(user):
            del data["owners"]
        del data["hash"]
        return data

    def setResponse(self: Model, user: Any, include: List[str or Type[Model]], resp: Dict = {}):
        return devSetResponse({
            "owners": ["User"]
        })(self, user, include, resp)

    def __init__(self, data: Any):
        super().__init__(data)

    def findOne(criteria: Any):
        return Database.main.findOne(Upload, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(Upload, criteria)

    def setupApp(app: Flask):
        @app.route("/upload/<id>")
        def uploadPage(id):
            user = None
            if "user" in session:
                user = session["user"]
            upload = Upload.findOne({"_id": id})
            if upload is None:
                return redirect(url_for('indexGET'))
            return Upload.renderPage(user, upload)

        @app.route("/upload/<id>/edit", methods=['POST', 'GET'])
        def editUpload(id):
            user = None
            form = {}
            errors = []
            if "user" in session:
                user = session["user"]
                upload = Upload.findOne({"_id": id, "owners": user.id})
                if upload is None:
                    return redirect(url_for('listUpload'))
                if request.method == "POST":
                    form = request.form
                    upload.apply(form)
                    if form["nonce"] != user.nonce:
                        flash(_("Bad nonce!"), "danger")
                    else:
                        del user.nonce
                        if len(upload.errors) == 0:
                            upload.save()
                form["nonce"] = user.nonce
                return Upload.renderEdit(user, upload, form, errors)
            return redirect(url_for('login'))

        @app.route("/upload/list")
        def listUpload():
            if "user" in session:
                user = session["user"]
                if user:
                    uploads = Upload.findMany({"owner": user.id})
                    return Upload.renderList(user, uploads)
            return redirect(url_for('login'))

        @app.route("/upload/list.json")
        def listUploadJSON():
            if "user" in session:
                user = session["user"]
                if user:
                    return devListJSON(user, request, Upload, [])
            return redirect(url_for('login')), 401

        @app.route("/upload/delete")
        def deleteUpload():
            if "user" in session:
                nonce = None
                user = session["user"]
                if user:
                    nonce = user.nonce
                    items = request.args["items"]
                    uploads = Upload.findMany(
                        {"_id": items, "owners": user.id})
                    if request.method == "POST":
                        if request.form["nonce"] != nonce:
                            flash(_("Bad nonce!"), "danger")
                        else:
                            del user.nonce
                            for upload in uploads:
                                upload.remove()
                            l = len(uploads)
                            if l > 1:
                                flash(_("Removed %i items!" % l), "success")
                            else:
                                flash(_("Removed item!"), "success")
                            return redirect(url_for('listUpload'))
                    return Upload.renderDelete(user, uploads, nonce)
            return redirect(url_for('login'))

        @app.route('/upload/new', methods=['POST', 'GET'])
        def newUpload():
            if "user" in session:
                user = session["user"]
                nonce = user.nonce
                errors = []
                form = {}
                if request.method == "POST":
                    form = request.form
                    if form["nonce"] == nonce:
                        upload = Upload(form)
                        upload.addOwner(user)
                        if len(upload.errors) == 0:
                            upload = Upload.register(upload)
                            if upload:
                                return redirect(url_for('uploadPage', id=upload.id))
                        else:
                            errors.extend(upload.errors)
                    else:
                        flash(_("Bad nonce!"), "danger")
                form["nonce"] = nonce
                return Upload.renderNew(user, form, errors)
            return redirect(url_for('login'))
