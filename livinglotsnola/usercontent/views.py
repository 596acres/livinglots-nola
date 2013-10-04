from livinglots_usercontent.files.forms import FileForm
from livinglots_usercontent.files.models import File
from livinglots_usercontent.notes.forms import NoteForm
from livinglots_usercontent.notes.models import Note
from livinglots_usercontent.photos.forms import PhotoForm
from livinglots_usercontent.photos.models import Photo
from livinglots_usercontent.views import AddContentView


class AddFileView(AddContentView):
    content_type_model = File
    form_class = FileForm


class AddNoteView(AddContentView):
    content_type_model = Note
    form_class = NoteForm


class AddPhotoView(AddContentView):
    content_type_model = Photo
    form_class = PhotoForm
