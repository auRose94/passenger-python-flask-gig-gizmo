import os

from flask.helpers import url_for

class BackgroundImage:
    def __init__(self, src) -> None:
        self.src = src

    def properties(self) -> str:
        src = url_for("static", filename=self.src)
        return " ".join([
            ('id="'+os.path.basename(self.src)+'"'),
            ('class="bg-slide"'),
            ('style="background-image: url(\''+src+'\');"')
        ])
