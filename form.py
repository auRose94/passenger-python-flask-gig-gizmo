
from flask_babel import gettext


class Form:
    nonce = ""
    items = []
    filled = {}
    errors = {}
    submitValue = gettext("Submit")
    submitClass = "btn btn-primary"

    def __init__(self, conf: dict, nonce: str, filled: dict = {}, errors: dict = {}) -> None:
        if isinstance(nonce, str):
            self.nonce = nonce
        if "items" in conf:
            self.items = conf["items"]
        if "submitValue" in conf:
            self.submitValue = conf["submitValue"]
        if "submitClass" in conf:
            self.submitClass = conf["submitClass"]
        if isinstance(filled, dict):
            self.filled = filled
        if isinstance(errors, dict):
            self.errors = errors

    def renderItem(self, item: dict, row: list = []) -> str:
        groupClass = item.get("groupClass", False)
        inputClass = item.get("class", "")
        label = item.get("label", "")
        name = item.get("name", "")
        sub = name.find('[')
        subKey = None
        if sub != -1:
            root = name[:sub]
            end = name.find(']', sub)
            subKey = name[sub+2:end-1]
            name = root
        id = item.get("id", name)
        type = item.get("type", "text")
        if not subKey:
            value = self.filled.get(name, None)
            error = self.errors.get(name, None)
        else:
            root = self.filled.get(name, {})
            value = root.get(subKey, None)
            root = self.errors.get(name, {})
            error = root.get(subKey, None)
        if error is not None:
            inputClass += " is-invalid"
        elif value is not None:
            inputClass += " is-valid"
        auto = item.get("auto", None)
        req = not item.get("optional", False)
        select = item.get("select", False)
        if not groupClass:
            rowSize = len(row)
            groupClass == "col-md-" + str([10, 6, 4, 2][rowSize])
        buffer = '<div class="form-group %s">' % (groupClass)
        buffer += '<label for="%s">%s</label>' % (name, label)
        if select:
            items: list[dict] = item.get("items", [])
            selAtts = [
                'type="%s"' % (type),
                'class="form-control %s"' % (inputClass),
                'name="%s"' % (name),
                'id="%s"' % (id),
            ]
            if req:
                selAtts.append("required")
            if auto is not None:
                selAtts.append('autocomplete="%s"' % (auto))
            if value is not None:
                selAtts.append('value="%s"' % (value))

            buffer += '<select %s>' % (" ".join(selAtts).strip())
            for sItem in items:
                sValue = sItem.get("value", "")
                default = sItem.get("default", False)
                sLabel = sItem.get("title", "")
                opAtts = [
                    'value="%s"' % (sValue)
                ]
                if (value is not None and sValue == value) or default:
                    opAtts.append('selected="true"')
                buffer += '<option %s>%s</option>' % (
                    " ".join(opAtts).strip(), sLabel)
            buffer += '</select>'
        else:
            inAtts = [
                'type="%s"' % (type),
                'class="form-control %s"' % (inputClass),
                'name="%s"' % (name),
                'id="%s"' % (id),
            ]
            if req:
                inAtts.append("required=\"true\"")
            if auto is not None:
                inAtts.append('autocomplete="%s"' % (auto))
            if value is not None:
                inAtts.append('value="%s"' % (value))
            buffer += '<input %s>' % (" ".join(inAtts).strip())
        if error is not None:
            buffer += '<div class="invalid-feedback">%s</div>' % (error)
        buffer += '</div>'
        return buffer

    def render(self) -> str:
        atts = ""
        if len(self.errors) > 0:
            atts = 'class="needs-validation"'
        buffer = '<form %s method="post">' % (atts)
        buffer += '<input type="hidden" name="nonce" value="%s">' % (
            self.nonce)
        for item in self.items:
            if isinstance(item, list):
                buffer += '<div class="form-row">'
                for rowItem in item:
                    buffer += self.renderItem(rowItem, item)
                buffer += '</div>'
            elif isinstance(item, dict):
                buffer += self.renderItem(item)
        buffer += '<input type="submit" value="%s" class="%s">' % (
            self.submitValue, self.submitClass)
        buffer += '</form>'
        return buffer
