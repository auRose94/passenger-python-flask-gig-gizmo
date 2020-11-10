from copy import Error
from re import U
from time import time
from flask.app import Flask
from jinja2.runtime import Undefined
from password_strength.tests import Length, NonLetters, Numbers, Special, Uppercase
import pymongo
from pymongo.operations import IndexModel
from werkzeug.datastructures import MultiDict
from db import Model, Database, devSetResponse
from flask import render_template, request, session, redirect, url_for, flash
from crypt import crypt
from validate_email import validate_email
from password_strength import PasswordPolicy
import os
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from location import Location
from upload import Upload
from typing import *
from config import dev

passwordMinLength = 8
passwordMinUpperCaser = 1
passwordMinNumbers = 1
passwordMinSpecial = 1
passwordMinNon = 1

MissingPassword = Error(_("Missing password!"))
MissingEmail = Error(_("Missing email!"))
MissingBirthday = Error(_("Missing birthday!"))
MissingUserType = Error(_("Missing userType!"))
MissingPhone = Error(_("Missing phone!"))
MissingLang = Error(_("Missing language!"))
MissingFirstName = Error(_("Missing first name!"))
MissingLastName = Error(_("Missing last name!"))
MissingUserType = Error(_("Missing User Type ('userType')!"))
MissingPronouns = Error(_("Missing pronouns!"))

InvalidPasswordLength = Error(
    _("Password is too short (expected %i)!" % passwordMinLength))
InvalidPasswordUpper = Error(
    _("Password is missing uppercase letters (expected %i)!" % passwordMinUpperCaser))
InvalidPasswordNumbers = Error(
    _("Password is missing numbers (expected %i)!" % passwordMinNumbers))
InvalidPasswordSpecial = Error(
    _("Password is missing special characters (expected %i)!" % passwordMinSpecial))
InvalidPasswordNon = Error(
    _("Password is missing non-letter characters (expected %i)!" % passwordMinNon))

InvalidEmail = Error(_("Invalid email!"))
InvalidBirthday = Error(_("Invalid birthday!"))
InvalidUserType = Error(_("Invalid userType!"))

BadCredentials = Error(_("Bad login credentials"))
BadNonce = Error(_("Bad nonce!"))

passPolicy = PasswordPolicy.from_names(
    length=passwordMinLength,  # min length: 8
    uppercase=passwordMinUpperCaser,  # need min. 2 uppercase letters
    numbers=passwordMinNumbers,  # need min. 2 digits
    special=passwordMinSpecial,  # need min. 2 special characters
    # need min. 2 non-letter characters (digits, specials, anything)
    nonletters=passwordMinNon,
)


class User(Model):
    def testPassword(form: Any, value: Any, errors: list):
        if not isinstance(value, str):
            errors.append(MissingPassword)
        else:
            errs = passPolicy.test(value)
            for err in errs:
                if isinstance(err, Length):
                    errors.append(InvalidPasswordLength)
                elif isinstance(err, Uppercase):
                    errors.append(InvalidPasswordUpper)
                elif isinstance(err, Numbers):
                    errors.append(InvalidPasswordNumbers)
                elif isinstance(err, Special):
                    errors.append(InvalidPasswordSpecial)
                elif isinstance(err, NonLetters):
                    errors.append(InvalidPasswordSpecial)

    def testEmail(form: Any, value: Any, errors: list):
        if not isinstance(value, str):
            errors.append(MissingEmail)
        elif not validate_email(value, verify=not dev):
            errors.append(InvalidEmail)

    def testBirthday(form: Any, value: Any, errors: list):
        if not isinstance(value, str):
            errors.append(MissingBirthday)
        else:
            bdTime = isoparse(value)
            bdMin = datetime.now()+relativedelta(years=-18)
            if bdMin < bdTime:
                errors.append(InvalidBirthday)

    def testUserType(form: Any, value: Any, errors: list):
        if not isinstance(value, str):
            errors.append(MissingUserType)
        elif [
            "patron",
            "musician",
            "bandMember",
            "bandManager",
            "venueOwner",
            "venueManager",
            "marketing",
            "all"
        ].index(value) == -1:
            errors.append(InvalidUserType)

    def testPhone(form: Any, value: Any, errors: list):
        # TODO: Parse phone number
        if not isinstance(value, str):
            errors.append(MissingPhone)

    def testLang(form: Any, value: Any, errors: list):
        # TODO: Find language from list
        if not isinstance(value, str):
            errors.append(MissingLang)

    def testFirstName(form: Any, value: Any, errors: list):
        if not isinstance(value, str):
            errors.append(MissingFirstName)

    def testLastName(form: Any, value: Any, errors: list):
        if not isinstance(value, str):
            errors.append(MissingLastName)

    def testPronouns(form: Any, value: Any, errors: list):
        # TODO: Check pronouns from list
        if not isinstance(value, str):
            errors.append(MissingPronouns)

    def testLocation(form: Any, value: Any, errors: list):
        loc = Location(value)
        if len(loc.errors) > 0:
            errors.extend(loc.errors)

    admin = Model.newProp(
        "admin", False, doc="Is an admin", hide=True)
    userType = Model.newProp(
        "userType", "all", testUserType, "What type of user")
    email = Model.newProp(
        "email", test=testEmail, doc="Email of user", hide=True)
    password = Model.newProp(
        "password", test=testPassword, doc="Hashed and salted password", hide=True)
    salt = Model.newProp(
        "salt", doc="The unique hash part for password test", hide=True)
    phone = Model.newProp(
        "phone", test=testPhone, doc="Telephone phone number of user")
    birthday = Model.newProp(
        "birthday", test=testBirthday, doc="Birthday of user")
    lang = Model.newProp(
        "lang", "en", testLang, "Language code the user prefers")
    firstName = Model.newProp(
        "firstName", test=testFirstName, doc="Formal name of user")
    middleName = Model.newProp(
        "middleName", "", doc="The middle name of the user")
    lastName = Model.newProp(
        "lastName", test=testLastName, doc="Family name of user")
    location = Model.newProp(
        "location", test=testLocation, doc="Location id in the database")
    pronouns = Model.newProp(
        "pronouns", "they/them", testPronouns, "Reference, for user convenience and stats")
    gender = Model.newProp(
        "gender", "", doc="Reference, for user convenience and stats")
    icon = Model.newProp(
        "icon", doc="User avatar")
    info = Model.newProp(
        "info", "", doc="HTML page description of user")

    def resolve(input: Any):
        return Model.resolve(User, input)

    def setResponse(self: Model, user: Any, include: List[str or Type[Model]], resp: Dict = {}):
        return devSetResponse({
            "location": Location,
            "icon": Upload
        })(self, user, include, resp)

    def filter(self, user: Any) -> Any:
        data = Model.filter(self, user)
        del data["password"]
        del data["salt"]
        if not isinstance(user, User) or (user.id != self.id and not user.admin):
            del data["email"]
            del data["phone"]
            del data["admin"]
        return data

    def __init__(self, data: Any):
        super().__init__(Model.setResolve(data, {
            "location": Location,
            "icon": Upload
        }))

    def findOne(criteria: Any):
        return Database.main.findOne(User, criteria)

    def findMany(criteria: Any):
        return Database.main.findMany(User, criteria)

    def login(app: Flask, email: str, password: str, rememberMe: bool = False):
        user = User.findOne({"email": email})
        if isinstance(user, User):
            hash = crypt(password, user.salt)
            if hash == user.password:
                if rememberMe:
                    session.permanent = True
                session["agent"] = request.user_agent
                session["remote"] = request.remote_user
                session["user"] = user
                session["expires"] = date.today(
                ) + app.permanent_session_lifetime
                session["created"] = time()
                return True, user
        return False, Undefined

    def renderLogin(nonce: str, error: Any):
        return render_template("userLogin.html.j2", error=error, nonce=nonce)

    def renderHome(self):
        return render_template("userHome.html.j2", user=self)

    def renderEdit(self, nonce: str, form: Any, errors: list):
        return render_template("userEdit.html.j2", user=self, nonce=nonce, filled=form, errors=errors)

    def renderDelete(self, nonce: str):
        return render_template("userDelete.html.j2", user=self, nonce=nonce)

    def renderCard(self):
        return render_template("userCard.html.j2", user=self)

    def renderPage(self):
        return render_template("userPage.html.j2", user=self)

    def renderSignUp(nonce: str, form: dict, errors: dict):
        return render_template("userSignup.html.j2", nonce=nonce, filled=form, errors=errors)

    def register(form: Any):
        user = None
        if isinstance(form, User):
            user = form
        elif isinstance(form, dict):
            user = User(form)
        salt = crypt(str(time()))
        hash = crypt(form["password"], salt)
        user.password = hash
        user.salt = salt
        return user.save()

    def delNonce(_self=None):
        del session["nonce"]

    def setNonce(_self=None, salt=None):
        nonce = crypt(str(time()), salt)
        session["nonce"] = nonce

    def getNonce(_self=None) -> str:
        nonce = None
        if session:
            if "nonce" in session:
                nonce = session["nonce"]
            if nonce == None:
                nonce = crypt(str(time()))
                session["nonce"] = nonce
        return nonce

    def setupApp(app: Flask):
        col = Database.main.getCollection(User)
        col.create_index([
            ('firstName', pymongo.TEXT),
            ('middleName', pymongo.TEXT),
            ('lastName', pymongo.TEXT),
            ('email', pymongo.TEXT),
            ('phone', pymongo.TEXT),
            ('info', pymongo.TEXT),
        ], name="userIndexModel")

        @app.route("/home")
        def userHome():
            if "user" in session:
                user = session["user"]
                if user:
                    return user.renderHome()
            return redirect(url_for('userLogin'))

        @app.route("/delete", methods=["POST", "GET"])
        def userDelete():
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    nonce = user.getNonce()
                    if request.method == "POST":
                        if nonce == request.form.get("nonce"):
                            user.delNonce()
                            done = user.remove()
                            if done:
                                flash(_("Account deleted, Goodbye, %s!" %
                                        user.firstName), "primary")
                                return redirect(url_for('userSignup'))
                        else:
                            flash(_("Bad nonce!"), "danger")
                    return user.renderDelete(nonce)
            return redirect(url_for('login'))

        @app.route('/login', methods=['POST', 'GET'])
        def userLogin():
            error = None
            nonce = User.getNonce()
            if request.method == "POST":
                f = MultiDict(request.form.items(multi=True))
                if f.get("nonce") == nonce:
                    User.delNonce()
                    loggedIn, user = User.login(
                        app, f["email"], f["password"], f["rememberMe"])
                    if loggedIn:
                        flash(_("Welcome %s!" % user.firstName), "success")
                        return redirect(url_for('userHome'), 301)
                    else:
                        error = BadCredentials
                else:
                    error = BadNonce
            flash(error, "danger")
            return User.renderLogin(nonce, error)

        @app.route('/sign-up', methods=['POST', 'GET'])
        def userSignup():
            f = {}
            nonce = User.getNonce()
            errors = {}
            if request.method == "POST":
                f = MultiDict(request.form.items(multi=True))
                if f.get("nonce") == nonce:
                    User.delNonce()
                    user = User(f)
                    if user.valid():
                        user = User.register(user)
                        if isinstance(user, User):
                            flash(_("Created account!"), "success")
                            loggedIn, user = User.login(app,
                                                        f["email"], f["password"], False)
                            if loggedIn:
                                flash(_("Welcome %s!" %
                                        user.firstName), "success")
                                return redirect(url_for('userHome'), 301)
                            else:
                                return redirect(url_for('login'))
                    else:
                        errors = user.errors
                else:  # Bad nonce, reload
                    return redirect(url_for('userSignup'))
            return User.renderSignUp(nonce, f, errors)

        @app.route('/options', methods=['POST', 'GET'])
        def userEdit():
            f = {}
            errors = {}
            if "user" in session:
                user: User or None = session["user"]
                if isinstance(user, User):
                    location = Location.findOne({"_id": user.location})
                    nonce = user.getNonce()
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        if f.get("nonce") == nonce:
                            user.delNonce()
                            user.apply(f)
                            if user.valid():
                                user.save()
                                flash(_("Applied %s!" %
                                        user.firstName), "success")
                            else:
                                errors = user.errors
                        else:
                            return redirect(url_for('userEdit'))
                    else:
                        f = user.filter(user)
                        f["location"] = location.filter(user)
                    return user.renderEdit(nonce, f, errors)
            return redirect(url_for('login'))


User.passwordPolicy = passPolicy
User.nonce = property(User.getNonce, User.setNonce, User.delNonce)
