from flask_babel import gettext as _

LANGS = dict({
    "en": {
        "code": "en",
        "name": "English",
        "enName": "English",
        "translation": _("English")
    },
    # TODO: Add more languages
    "de": {
        "code": "de",
        "name": "Deütsch",
        "enName": "German",
        "translation": _("German")
    },
    "fr": {
        "code": "fr",
        "name": "Français",
        "enName": "French",
        "translation": _("French")
    }
})