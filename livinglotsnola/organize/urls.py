from django.conf.urls.defaults import patterns, url

from livinglots import get_organizer_model
from livinglots_organize.forms import OrganizerForm
from livinglots_organize.views import AddParticipantView
import livinglots_organize.urls as llurls


urlpatterns = llurls.urlpatterns + patterns('',

    url(r'^add/',
        AddParticipantView.as_view(
            form_class=OrganizerForm,
            model=get_organizer_model(),
        ),
        name='add_organizer'),

)
