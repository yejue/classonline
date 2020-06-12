
from django.template import Library
from django.forms.widgets import CheckboxInput

register = Library()


@register.filter()
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)


@register.filter()
def is_url_field(field):
    return True if 'url' in field.label else False
