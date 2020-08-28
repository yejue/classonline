import re

from django.core import validators


class MediaUrlValidator(validators.URLValidator):
    def __call__(self, value):
        try:
            super().__call__(value)
        except Exception as e:
            if re.match(r'^/media/.*$', value):
                pass
            else:
                raise e
