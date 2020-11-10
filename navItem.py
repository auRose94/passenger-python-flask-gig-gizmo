from flask import request, session
from crypt import crypt
from time import time

class NavItem:
    def set_href(self, value):
        self.rule = value

    def get_href(self) -> str:
        return self.rule

    def del_href(self):
        del self.rule

    href = property(get_href, set_href, del_href)

    def __init__(self, rule, title, auth=False) -> None:
        self.rule = rule  # or array of NavItems
        self.title = title
        self.auth = auth

    def show(self):
        if isinstance(self.rule, list):
            return all(ele.show() for ele in self.rule)
        if self.auth:
            return isinstance(session, object) and "user" in session
        elif self.auth == False:
            return True
        return False

    def active(self):
        if isinstance(self.rule, list):
            return any(ele.active() for ele in self.rule)
        url_rule = str(request.url_rule)
        rule = self.rule
        return str(url_rule).find(rule) != -1 and len(url_rule) == len(rule)

    def classes(self):
        classes = ["nav-item"]
        if isinstance(self.rule, list):
            classes.append("dropdown")
        if self.active():
            classes.append("active")
        return " ".join(classes)

    def renderTitle(self):
        content = ""
        content += self.title
        if self.active():
            content += '<span class="sr-only">(current)</span>'
        return content

    def render(self):
        items = []
        items.append('<li class="'+self.classes()+'">')
        if isinstance(self.rule, list):
            uuid = crypt(str(time()))
            items.append('<a id="'+uuid+'" class="nav-link dropdown-toggle" href="#" role="button" ' + 
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+
                self.renderTitle()+'</a>')
            items.append('<div class="dropdown-menu" aria-labelledby="'+uuid+'">')
            for item in self.rule:
                if item.show():
                    items.append('<a class="dropdown-item" href="'+item.href+'">'+item.renderTitle()+'</a>')
            items.append('</div>')
        else:
            items.append('<a class="nav-link" href="'+self.href+'">'+self.renderTitle()+'</a>')
        items.append('</li>')
        return "".join(items)
