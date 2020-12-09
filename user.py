from copy import Error
from forms.unregister import UnregisterForm
from forms.login import LoginForm
from location import Location
from flask import Flask
from mongoengine import *
from time import time
from flask import render_template, request, session, redirect, url_for, flash
from crypt import crypt
from datetime import *
from dateutil.parser import *
from flask_babel import gettext as _
from typing import *
import mongoengine as me
from langs import LANGS
from pymongo.collection import ObjectId

from forms.user import UserForm, UserEditForm, UserRegisterForm
from forms.unregister import UnregisterForm
from forms.login import LoginForm


class User(me.Document):
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
    password = me.StringField(
        required=True, validation=UserForm.validate_password)
    salt = me.StringField(default=None)
    phone = me.StringField(required=True, unique=True,
                           validation=UserForm.validate_phone)
    birthday = me.DateField(
        required=True, validation=UserForm.validate_birthday)
    lang = me.StringField(default="en", choices=list(LANGS.keys()))
    firstName = me.StringField(required=True)
    middleName = me.StringField()
    lastName = me.StringField(required=True)
    location = me.LazyReferenceField(
        "Location", dbref=ObjectId, passthrough=True, reverse_delete_rule=me.CASCADE)
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


def login(app: Flask, form: LoginForm or UserForm):
    if form.validate():
        user: User = User.objects(email=form.email.data).first()
        if user is not None:
            hash = crypt(form.password.data, user.salt)
            if hash == user.password:
                session.permanent = form["rememberMe"].data or False
                session["agent"] = request.user_agent.string
                session["remote"] = request.remote_user
                session["user"] = user
                session["expires"] = (date.today(
                ) + app.permanent_session_lifetime).isoformat()
                session["created"] = (date.today()).isoformat()
                return True, user
    return False, None


def renderLogin(form: LoginForm):
    return render_template("userLogin.html.j2", form=form)


def renderHome(self: User):
    return render_template("userHome.html.j2", user=self)


def renderEdit(self: User, form: UserEditForm):
    return render_template("userEdit.html.j2", user=self, form=form, edit=True)


def renderDelete(self: User, form: UnregisterForm):
    return render_template("userDelete.html.j2", user=self, form=form)


def renderCard(self: User):
    return render_template("userCard.html.j2", user=self)


def renderPage(self: User):
    return render_template("userPage.html.j2", user=self)


def renderSignUp(form: UserRegisterForm):
    return render_template("userSignup.html.j2", form=form)

def edit(self: User, location: Location, form: UserEditForm):
    if form.password.data != "":
        salt = crypt(str(time()))
        hash = crypt(form.password.data, salt)
        self.password = hash
        self.salt = salt
    else:
        form.password.data = self.password
    self.userType = form.userType.data
    self.firstName = form.firstName.data
    self.middleName = form.middleName.data
    self.lastName = form.lastName.data
    self.email = form.email.data
    self.phone = form.phone.data
    self.birthday = form.birthday.data
    self.lang = form.lang.data
    self.pronouns = form.pronouns.data
    self.gender = form.gender.data
    self.icon = form.icon.data
    self.info = form.info.data

    location.edit(form.location.form)

    self.validate()
    return self


def register(form: UserForm):
    errors = form.validate()
    if not errors:
        location = Location.register(form.location.form)

        salt = crypt(str(time()))
        hash = crypt(form.password.data, salt)
        user = User(
            id=form.id.data,
            email=form.email.data,
            phone=form.phone.data,
            birthday=form.birthday.data,
            lang=form.lang.data,
            firstName=form.firstName.data,
            middleName=form.middleName.data,
            lastName=form.lastName.data,
            location=location.id,
            pronouns=form.pronouns.data,
            gender=form.gender.data,
            userType=form.userType.data,
            salt=salt,
            password=hash,
            # icon=form.icon.data,
            # info=form.info.data
        )
        user.validate()

        return user.save()
    return None


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
        f = UnregisterForm(request.form)
        if "user" in session:
            user: User or None = session["user"]
            if isinstance(user, User):
                if request.method == "POST":
                    if f.validate():
                        done = user.delete()
                        if done:
                            flash(_("Account deleted, Goodbye, %s!" %
                                    user.firstName), "primary")
                            return redirect(url_for('userSignup'))
                return user.renderDelete(f)
        return redirect(url_for("userLogin"))

    @app.route('/login', methods=['POST', 'GET'])
    def userLogin():
        f = LoginForm(request.form)
        if request.method == "POST":
            try:
                loggedIn, user = login(app, f)
            except me.ValidationError:
                flash(_("Please fill everything required."), "danger")
            else:
                if loggedIn:
                    flash(_("Welcome %s!" % user.firstName), "success")
                    return redirect(url_for('userHome'), 301)
                else:
                    flash(_("Bad login credentials"), "danger")
        return renderLogin(f)

    @app.route('/sign-up', methods=['POST', 'GET'])
    def userSignup():
        f = UserRegisterForm(request.form)
        if request.method == "POST":
            try:
                user = register(f)
            except me.ValidationError as err:
                flash(_("Please fill everything required."), "danger")
            else:
                if isinstance(user, User):
                    flash(_("Created account!"), "success")
                    loggedIn, user = login(app, f)
                    if loggedIn:
                        flash(_("Welcome %s!" %
                                user.firstName), "success")
                        return redirect(url_for('userHome'), 301)
                    else:
                        return redirect(url_for('userLogin'))
        return User.renderSignUp(f)

    @app.route('/options', methods=['POST', 'GET'])
    def userEdit():
        if "user" in session:
            user: User or None = session["user"]
            if isinstance(user, User):
                location: Location = Location.objects(
                    id=user.location.id).first()
                f = UserEditForm(request.form, user)
                if request.method == "POST":
                    try:
                        user.edit(location, f)
                    except me.ValidationError:
                        flash(
                            _("Please correctly fill everything required."), "danger")
                    else:
                        location.save()
                        user.save()
                        flash(_("Applied %s!" %
                                user.firstName), "success")
                return user.renderEdit(f)
        return redirect(url_for("userLogin"))


User.login = login
User.renderLogin = renderLogin
User.renderHome = renderHome
User.renderEdit = renderEdit
User.renderDelete = renderDelete
User.renderCard = renderCard
User.renderPage = renderPage
User.renderSignUp = renderSignUp
User.register = register
User.edit = edit
User.setupApp = setupApp
