import re
from django import forms
from django.utils.safestring import mark_safe

def mobile_number_validation(mobile_number_original):
    mobile_number = str(mobile_number_original).replace(' ', '').replace('+', '').replace('-', '')
    if len(mobile_number) < 8:
        return False
    return mobile_number

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """renders horizontal radio buttons.
    found here:
    https://wikis.utexas.edu/display/~bm6432/Django-Modifying+RadioSelect+Widget+to+have+horizontal+buttons
    """

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))