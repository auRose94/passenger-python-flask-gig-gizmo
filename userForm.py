
from typing import Any, Dict, Tuple
from country_list.country_list import countries_for_language
from flask.globals import session
from flask_babel import gettext as _
from form import Form
from langs import LANGS


class UserForm(Form):
    def langMap(item: Tuple[str, Dict[str, Any]]) -> Any:
        code = item[0]
        lang = item[1]
        return {
            "default": code == "en",
            "value": code,
            "title": ('%s (%s)' % (lang.get("name", ""), lang.get("enName", "")))
        }

    def countryMap(item: Tuple[str, str]) -> Any:
        code = item[0]
        country = item[1]
        return {
            "default": code == "US",
            "value": code,
            "title": country
        }

    def __init__(self, nonce: str, filled: dict = {}, errors: dict = {}) -> None:
        lang = session.get('lang', 'en')
        super().__init__({
            "items": [
                [
                    {
                        "name": "lang",
                        "label": _("Language"),
                        "auto": "language",
                        "select": True,
                        "items": list(map(UserForm.langMap, LANGS.items()))
                    },
                    {
                        "name": "location['country']",
                        "id": "country",
                        "label": _("Country"),
                        "auto": "country",
                        "select": True,
                        "items": list(map(UserForm.countryMap, countries_for_language(lang)))
                    }
                ],
                [
                    {
                        "name": "email",
                        "label": _("Email"),
                        "auto": "email",
                        "type": "email",
                    },
                    {
                        "name": "phone",
                        "label": _("Phone"),
                        "auto": "tel",
                        "type": "tel",
                    },
                    {
                        "name": "birthday",
                        "label": _("Birthday"),
                        "auto": "bday",
                        "type": "date",
                    }
                ],
                [
                    {
                        "name": "password",
                        "label": _("Password"),
                        "auto": "new-password",
                        "type": "password",
                    },
                    {
                        "name": "confPassword",
                        "label": _("Confirm"),
                        "auto": "new-password",
                        "type": "password",
                    },
                ],
                [
                    {
                        "name": "firstName",
                        "label": _("First Name"),
                        "auto": "given-name",
                    },
                    {
                        "name": "middleName",
                        "label": _("Middle Name"),
                        "auto": "additional-name",
                    },
                    {
                        "name": "lastName",
                        "label": _("Last Name"),
                        "auto": "family-name",
                    }
                ],
                [
                    {
                        "name": "location['address1']",
                        "id": "address1",
                        "label": _("Address 1"),
                        "auto": "address-line1",
                    },
                    {
                        "name": "location['address2']",
                        "id": "address2",
                        "label": _("Address 2"),
                        "auto": "address-line2",
                        "optional": True
                    }
                ], 
                [
                    {
                        "name": "location['state']",
                        "label": _("State/Province/Region"),
                        "auto": "address-level1",
                    },
                    {
                        "name": "location['city']",
                        "label": _("City"),
                        "auto": "address-level2",
                    },
                    {
                        "name": "location['zip']",
                        "label": _("Postal/ZIP"),
                        "auto": "postal-code",
                    }
                ],
                [
                    {
                        "name": "userType",
                        "label": _("Using GigGizmo As?"),
                        "select": True,
                        "items": [
                            {
                                "value": "patron",
                                "title": _("Patron")
                            },
                            {
                                "value": "musician",
                                "title": _("Musician")
                            },
                            {
                                "value": "bandMember",
                                "title": _("Band Member")
                            },
                            {
                                "value": "bandManager",
                                "title": _("Band Manager")
                            },
                            {
                                "value": "venueOwner",
                                "title": _("Venue Owner")
                            },
                            {
                                "value": "venueManager",
                                "title": _("Venue Manager")
                            },
                            {
                                "value": "marketing",
                                "title": _("Marketing Consultant")
                            },
                            {
                                "value": "all",
                                "title": _("All")
                            }
                        ]
                    }, 
                    {
                        "name": "pronouns",
                        "label": _("Pronouns"),
                        "select": True,
                        "items": [
                            {
                                "value": "they/them",
                                "title": _("They/Them/Their"),
                            },
                            {
                                "value": "she/her",
                                "title": _("She/Her")
                            },
                            {
                                "value": "he/him",
                                "title": _("He/Him/His")
                            },
                            {
                                "value": "ve/ver",
                                "title": _("Ve/Ver/Vis")
                            },
                            {
                                "value": "xe/xer",
                                "title": _("Xe/Xem/Xyr")
                            },
                            {
                                "value": "ze/hir",
                                "title": _("Ze/hir")
                            }
                        ]
                    },
                    {
                        "name": "gender",
                        "label": _("Gender"),
                        "select": True,
                        "optional": True,
                        "items": [
                            {
                                "value": "",
                                "title": "",
                            },
                            {
                                "value": "non-binary",
                                "title": _("Non-Binary")
                            },
                            {
                                "value": "female",
                                "title": _("Female")
                            },
                            {
                                "value": "male",
                                "title": _("Male")
                            }
                        ]
                    }
                ]
            ],
            "submitValue": _("Register"),
        }, nonce, filled, errors)
