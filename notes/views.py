from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q  
from .models import Note

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "note_list.html"
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Note.objects.filter(Q(title__icontains=query))
        return Note.objects.all()
    

class NoteDetailView(LoginRequiredMixin, DetailView): 
    model = Note
    template_name = "note_detail.html"


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Note
    fields = (
        "title",
        "body",
    )
    template_name = "note_edit.html"
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    model = Note
    template_name = "note_delete.html"
    success_url = reverse_lazy("note_list")
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = "note_new.html"
    fields = (
        "title",
        "body",
    )
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
