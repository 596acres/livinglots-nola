from livinglots_usercontent.files.forms import FileForm
from livinglots_usercontent.notes.forms import NoteForm
from livinglots_usercontent.photos.forms import PhotoForm
from livinglots_usercontent.views import AddContentView

from lots.models import Lot


class AddFileView(AddContentView):
    content_type_model = Lot
    form_class = FileForm


class AddNoteView(AddContentView):
    content_type_model = Lot
    form_class = NoteForm


class AddPhotoView(AddContentView):
    content_type_model = Lot
    form_class = PhotoForm
