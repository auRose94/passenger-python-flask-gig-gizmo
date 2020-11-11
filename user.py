from copy import Error
from mongoengine.errors import ValidationError
from mongoengine.queryset.base import CASCADE
from re import U
from time import time
from flask.app import Flask
from jinja2.runtime import Undefined
from password_strength.tests import Length, NonLetters, Numbers, Special, Uppercase
from werkzeug.datastructures import MultiDict
from flask import render_template, request, session, redirect, url_for, flash
from crypt import crypt
from password_strength import PasswordPolicy
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
from flask_babel import gettext as _
from location import Location
from typing import *
from config import dev
import mongoengine as me
from langs import LANGS

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
InvalidPhone = Error(_("Invalid international phone number"))

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

class User(me.Document):
    def testPassword(value: Any):
        if not isinstance(value, str):
            raise(MissingPassword)
        else:
            errs = passPolicy.test(value)
            for err in errs:
                if isinstance(err, Length):
                    raise(InvalidPasswordLength)
                elif isinstance(err, Uppercase):
                    raise(InvalidPasswordUpper)
                elif isinstance(err, Numbers):
                    raise(InvalidPasswordNumbers)
                elif isinstance(err, Special):
                    raise(InvalidPasswordSpecial)
                elif isinstance(err, NonLetters):
                    raise(InvalidPasswordSpecial)

    def testBirthday(value: Any):
        bdTime = None
        if not isinstance(value, (str, int, float, datetime)):
            raise(MissingBirthday)
        elif isinstance(value, str):
            bdTime = isoparse(value)
        elif isinstance(value, datetime):
            bdTime = value
        elif isinstance(value, float or int):
            bdTime = datetime.fromtimestamp(value)
        bdMin = datetime.now()+relativedelta(years=-18)
        if bdMin < bdTime:
            raise(InvalidBirthday)

    def testPhone(value: Any):
        # TODO: Parse phone number
        if not isinstance(value, str):
            raise(MissingPhone)
        if value.count("+") != 1:
            raise(InvalidPhone)

    admin = me.BooleanField(default=False)
    userType = me.StringField(required=True, choices=[
        "patron",
        "musician",
        "bandMember",
        "bandManager",
        "venueOwner",
        "venueManager",
        "marketing",
        "all"
    ])
    email = me.EmailField(required=True, unique=True, allow_utf8_user=True)
    password = me.StringField(required=True, validation=testPassword)
    salt = me.StringField(default=None)
    phone = me.StringField(required=True, unique=True, validation=testPhone)
    birthday = me.DateField(required=True, validation=testBirthday)
    lang = me.StringField(default="en", choices=list(LANGS.keys()))
    firstName = me.StringField(required=True)
    middleName = me.StringField()
    lastName = me.StringField(required=True)
    location = me.LazyReferenceField(
        "Location", passthrough=True, reverse_delete_rule=CASCADE)
    pronouns = me.StringField(
        default="they/them", choices=["they/them", "she/her", "he/him", "ve/ver", "xe/xer", "ze/hir"])
    gender = me.StringField(default="", choices=[
                            "", "non-binary", "female", "male"])
    icon = me.ImageField(size=(1024, 1024, True),
                         thumbnail_size=(128, 128, True))
    info = me.StringField()

    meta = {'indexes': [
        {'fields': ["$email", "$phone", '$firstName', "$middleName", "$lastName", "$info"],
         'default_language': "english",
         'weights': {'email': 10, 'phone': 10, 'info': 5, 'firstName': 2, 'middleName': 2, 'lastName': 2}
         }
    ]}

    def login(app: Flask, form: Dict = {}):
        email = form.get("email", "")
        password = form.get("password", "")
        rememberMe = form.get("rememberMe", False)
        user: User or None = User.object({"email": email})
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

    def register(form: Dict):
        user = User(form)
        user.validate()
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
                            done = user.delete()
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
                    loggedIn, user = User.login(app, f)
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
                    try:
                        user = User.register(f)
                    except ValidationError as err:
                        errors[err.field_name] = err.message
                    else:
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
                    location: Location = Location.object({"_id": user.location})
                    nonce = user.getNonce()
                    if request.method == "POST":
                        f = MultiDict(request.form.items(multi=True))
                        if f.get("nonce") == nonce:
                            user.delNonce()
                            for key, value in f.items(multi=True):
                                user[key] = value
                            try:
                                user.validate()
                            except ValidationError as err:
                                errors[err.field_name] = err.message
                            else:
                                user.save()
                                flash(_("Applied %s!" %
                                        user.firstName), "success")
                        else:
                            return redirect(url_for('userEdit'))
                    else:
                        f = user.to_json()
                        f["location"] = location.to_json()
                    return user.renderEdit(nonce, f, errors)
            return redirect(url_for('login'))


User.passwordPolicy = passPolicy
User.nonce = property(User.getNonce, User.setNonce, User.delNonce)
