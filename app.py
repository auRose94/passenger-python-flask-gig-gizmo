from flask import Flask, render_template, g, request
from navItem import NavItem
from background import BackgroundImage
from country_list import countries_for_language
from flask.globals import session
from user import User
from band import Band
from venue import Venue
from location import Location
from gig import Gig
from api import API
from flask_session import Session
from flask_babel import format_timedelta, format_date, format_datetime, format_time, Babel, gettext as _
from config import dev, env
from langs import LANGS
from userForm import UserForm
from flask_mongoengine import MongoEngine

SESSION_TYPE = "mongodb"
SESSION_MONGODB_DB = "GigGizmo"
SESSION_COOKIE_SECURE = not dev

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "GigGizmo",
}
app.config.from_object(__name__)
app.secret_key = b'`\xae\xa8\xfdt\x8e["\xa3U\xd4\xcb\xff=o\x8d'
app.templates_auto_reload = True
Session(app)
babel = Babel(app)
db = MongoEngine(app)

app.env = env

app.navItems = [
    NavItem([
        NavItem("/login", _("Login")),
        NavItem("/sign-up",  _("Sign Up")),
        NavItem("/options", _("Options"), True),
        NavItem("/upload/list", _("Uploads"), True),
        NavItem("/api/list", _("Developer/Plugin API"), True),
        NavItem("/home",  _("Home"), True),
        NavItem("/delete", _("Delete Account"), True),
    ], _("User")),
    NavItem([
        NavItem("/band/list", _("All bands"), True),
        NavItem("/band/new", _("New band"), True),
    ], _("Band")),
    NavItem([
        NavItem("/venue/list", _("All venues"), True),
        NavItem("/venue/new", _("New venue"), True),
    ], _("Venue")),
    NavItem([
        NavItem("/gig/list", _("All gigs"), True),
        NavItem("/gig/new", _("New gigs"), True),
    ], _("Gig")),
    NavItem([
        NavItem("/wpPlugin", _("WordPress Plugin")),
        NavItem("/docs", _("Developer Docs")),
        NavItem("/privacy", _("Privacy Policy")),
        NavItem("/terms", _("Terms of Service")),
    ], _("Info"))
]

app.backgrounds = [
    BackgroundImage("/images/bg1.jpg"),
    BackgroundImage("/images/bg2.jpg"),
    BackgroundImage("/images/bg3.jpg"),
    BackgroundImage("/images/bg4.jpg"),
    BackgroundImage("/images/bg5.jpg"),
    BackgroundImage("/images/bg6.jpg"),
    BackgroundImage("/images/bg7.jpg"),
    BackgroundImage("/images/bg8.jpg"),
    BackgroundImage("/images/bg9.jpg")
]

@babel.localeselector
def get_locale():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(list(LANGS.keys()))


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

@app.template_global()
def getNavItems():
    return app.navItems

@app.template_global()
def getBackgroundImages():
    return app.backgrounds

@app.template_global()
def perfExtension():
    if not dev:
        return ".min"
    return ""

@app.template_filter()
def formatDateTime(value):
    format_datetime(value)

@app.template_filter()
def formatDate(value):
    format_date(value)

@app.template_filter()
def formatTime(value):
    format_time(value)

@app.template_filter()
def deltaFromNow(value):
    format_timedelta(value)

@app.template_global()
def getLanguages():
    return LANGS.items()

@app.template_global()
def getCountries():
    lang = session.get('lang', 'en')
    return countries_for_language(lang)

@app.template_global()
def getUserForm(nonce, filled, errors):
    return UserForm(nonce, filled, errors).render()
    
db.register(User)
db.register(Band)
db.register(Venue)
db.register(Gig)
db.register(Location)
db.register(API)

@app.route("/")
def indexGET():
    return render_template("index.html.j2")

@app.route("/terms")
def termsGET():
    return render_template("termsOfService.html.j2")

@app.route("/docs")
def docsGET():
    return render_template("docs.html.j2")

@app.route("/wp-plugin")
def wpPluginGET():
    return render_template("wpPlugin.html.j2")

@app.route("/privacy")
def privacyGET():
    return render_template("privacyPolicy.html.j2")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html.j2'), 404

User.setupApp(app)
Band.setupApp(app)
Venue.setupApp(app)
Location.setupApp(app)
Gig.setupApp(app)
API.setupApp(app)

if __name__ == "__main__":
    app.run()
