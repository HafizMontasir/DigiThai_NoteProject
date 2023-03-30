from django.urls import path
from .views import (
    NoteListView,
    NoteDetailView,
    NoteUpdateView,
    NoteDeleteView,
    NoteCreateView,
)

urlpatterns = [
    path("<int:pk>/", NoteDetailView.as_view(), name="note_detail"), 
    path("<int:pk>/edit/", NoteUpdateView.as_view(), name="note_edit"), 
    path("<int:pk>/delete/", NoteDeleteView.as_view(), name="note_delete"), 
    path("new/", NoteCreateView.as_view(), name="note_new"), 
    path("", NoteListView.as_view(), name="note_list"),
]
