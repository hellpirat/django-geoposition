from __future__ import unicode_literals

import json
from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None, None]

    def format_output(self, rendered_widgets):
        return render_to_string('geoposition/widgets/geoposition.html', {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
            'config': {
                'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
                'map_options': json.dumps(settings.MAP_OPTIONS),
                'marker_options': json.dumps(settings.MARKER_OPTIONS),
            }
        })

    class Media:
        js = (
            '//maps.googleapis.com/maps/api/js?key=%s&libraries=places' % settings.GOOGLE_MAPS_API_KEY,
            '//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
            'geoposition/geoposition.js',
            '//cdnjs.cloudflare.com/ajax/libs/geocomplete/1.7.0/jquery.geocomplete.js',

        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
