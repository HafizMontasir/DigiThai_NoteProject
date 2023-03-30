from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from .models import Note


class NoteCreationTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.url = reverse("note_new")

    def test_note_creation_success(self):
        response = self.client.post(
            self.url, {"title": "Test note", "body": "This is a test note."}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title="Test note").exists())

    def test_note_creation_failure(self):
        response = self.client.post(
            self.url, {"title": "", "body": "This is a test note."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")


class NoteEditingTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )
        self.note = Note.objects.create(
            title="Test note", body="This is a test note.", author=self.user
        )
        self.client.login(username="testuser", password="testpass")
        self.url = reverse("note_edit", args=[self.note.pk])

    def test_note_editing_success(self):
        response = self.client.post(
            self.url,
            {"title": "Updated test note", "body": "This is an updated test note."},
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated test note")
        self.assertEqual(self.note.body, "This is an updated test note.")

    def test_note_editing_failure(self):
        response = self.client.post(
            self.url, {"title": "", "body": "This is an updated test note."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
