from datetime import datetime, date
from dateutil.parser import isoparse
from flask.helpers import url_for
from mongoengine.fields import ListField
from wtforms import *
import wtforms.validators as validators
from wtforms.fields.html5 import *
from flask_babel import gettext as _
from typing import *
from password_strength import PasswordPolicy
from dateutil.relativedelta import relativedelta
from password_strength.tests import Length, NonLetters, Numbers, Special, Uppercase
from langs import LANGS
from forms.location import LocationForm
from mongoengine.fields import ObjectId


passwordMinLength = 8
passwordMinUpperCaser = 1
passwordMinNumbers = 1
passwordMinSpecial = 1
passwordMinNon = 1

MissingPassword = ValidationError(_("Missing password!"))
MissingBirthday = ValidationError(_("Missing birthday!"))
MissingPhone = ValidationError(_("Missing phone!"))
MissingFirstName = ValidationError(_("Missing first name!"))

InvalidPasswordLength = ValidationError(
    _("Password is too short (expected %i)!" % passwordMinLength))
InvalidPasswordUpper = ValidationError(
    _("Password is missing uppercase letters (expected %i)!" % passwordMinUpperCaser))
InvalidPasswordNumbers = ValidationError(
    _("Password is missing numbers (expected %i)!" % passwordMinNumbers))
InvalidPasswordSpecial = ValidationError(
    _("Password is missing special characters (expected %i)!" % passwordMinSpecial))
InvalidPasswordNon = ValidationError(
    _("Password is missing non-letter characters (expected %i)!" % passwordMinNon))

InvalidBirthday = ValidationError(_("Invalid birthday!"))
InvalidPhone = ValidationError(_("Invalid international phone number, +numbers"))

passPolicy = PasswordPolicy.from_names(
    length=passwordMinLength,  # min length: 8
    uppercase=passwordMinUpperCaser,  # need min. 2 uppercase letters
    numbers=passwordMinNumbers,  # need min. 2 digits
    special=passwordMinSpecial,  # need min. 2 special characters
    # need min. 2 non-letter characters (digits, specials, anything)
    nonletters=passwordMinNon,
)

class UserForm(Form):
    def tosLabel():
        return '<a href="%s">%s</a>' % (url_for("termsGET"),
                                     _('Accept the Terms of Service'))
    def langMap(item: Tuple[str, Dict[str, Any]]) -> Any:
        code = item[0]
        lang = item[1]
        return (code, ('%s (%s)' % (lang.get("name", ""), lang.get("enName", ""))))

    id = HiddenField("_id", default=ObjectId)
    email = EmailField(
        label=_("Email"),
        validators=[
            validators.DataRequired(_("Email is required")),
            validators.Email(
                _("Needs to be a valid email")
            )
        ]
    )
    phone = TelField(
        label=_("Phone"),
        validators=[validators.DataRequired(_("Phone is required"))]
    )
    birthday = DateField(
        label=_("Birthday"),
        validators=[validators.DataRequired(_("Birthday is required"))]
    )
    lang = SelectField(
        label=_("Language"),
        default="en",
        choices=list(map(langMap, LANGS.items()))
    )
    accept_tos = BooleanField(
        label=(tosLabel),
        validators=[validators.DataRequired(_("You have to accept the Terms of Service"))]
    )
    firstName = StringField(
        label=_("First"),
        validators=[validators.DataRequired(_("First/Formal name required"))]
    )
    middleName = StringField(
        label=_("Middle")
    )
    lastName = StringField(
        label=_("Last"),
        validators=[validators.DataRequired(_("Last/Family name required"))]
    )
    location = FormField(LocationForm)
    userType = SelectField(
        label=_("Using GigGizmo As?"),
        choices=[
            ("patron", _("Patron")),
            ("musician", _("Musician")),
            ("bandMember", _("Band Member")),
            ("bandManager", _("Band Manager")),
            ("venueOwner", _("Venue Owner")),
            ("venueManager", _("Venue Manager")),
            ("marketing", _("Marketing")),
            ("all", _("All"))
        ]
    )
    pronouns = SelectField(
        label=_("Pronouns"),
        choices=[
            ("they/them", _("They/Them/Their")),
            ("she/her", _("She/Her")),
            ("he/him", _("He/Him/His")),
            ("ve/ver", _("Ve/Ver/Vis")),
            ("xe/xer", _("Xe/Xem/Xyr")),
            ("ze/hir", _("Ze/hir"))
        ]
    )
    gender = SelectField(
        label=_("Gender"),
        choices=[
            ("", ""),
            ("non-binary", _("Non-Binary")),
            ("female", _("Female")),
            ("male", _("Male"))
        ]
    )
    info = TextAreaField(
        label=_("Biography")
    )
    icon = FileField(label=_("Icon"), default=None)

    def validate_password(*argv):
        value = None
        if len(argv) >= 2:
            value = argv[1]
        else:
            value = argv[0]
        if isinstance(value, PasswordField):
            value = value.data
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

    def validate_birthday(*argv):
        value = None
        if len(argv) >= 2:
            value = argv[1]
        else:
            value = argv[0]
        if isinstance(value, DateField):
            value = value.data
        bdTime = None
        if value is None:
            raise(MissingBirthday)
        elif isinstance(value, str):
            bdTime = isoparse(value)
        elif isinstance(value, date):
            bdTime = datetime(value.year, value.month, value.day)
        elif isinstance(value, int):
            bdTime = datetime.fromtimestamp(value)
        bdMin = datetime.now() - relativedelta(years=18)
        if bdMin < bdTime:
            raise(InvalidBirthday)

    def validate_phone(*argv):
        value = None
        if len(argv) >= 2:
            value = argv[1]
        else:
            value = argv[0]
        if isinstance(value, StringField):  
            value = value.data  
        if type(value) is not str:
            raise(MissingPhone)
        if value.count("+") != 1:
            raise(InvalidPhone)

class UserEditForm(UserForm):
    password = PasswordField(
        label=_("Password"),
        validators=[
            validators.EqualTo('confPassword', message='Passwords must match')
        ])
    confPassword = PasswordField(
        label=_("Confirm")
    )

class UserRegisterForm(UserForm):
    password = PasswordField(
        label=_("Password"),
        validators=[
            validators.DataRequired(_("Password is required")),
            validators.EqualTo('confPassword', message='Passwords must match')
        ])
    confPassword = PasswordField(
        label=_("Confirm"),
        validators=[
            validators.DataRequired(_("Rewrite the password here"))
        ]
    )