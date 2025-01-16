from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import signing
from django.urls import reverse
from .models import File, CompanyUser

class FileDownloadTestCase(TestCase):
    def setUp(self):
        self.ops_user = CompanyUser.objects.create_user(
            username='opsuser', password='password', user_type='Ops'
        )
        self.client_user = CompanyUser.objects.create_user(
            username='clientuser', password='password', user_type='Client'
        )
        self.client = Client()
        self.client.login(username='clientuser', password='password')
        self.test_file = SimpleUploadedFile(
            "testfile.docx", b"Test file content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        self.file_instance = File.objects.create(
            name=self.test_file.name,
            file=self.test_file,
            uploaded_by=self.ops_user,
        )
        self.token = signing.dumps({'file_id': self.file_instance.id})
        self.download_url = reverse('download_file') + f'?token={self.token}'

    def test_download_file_success(self):
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.test_file.name}"')

    def test_download_file_invalid_token(self):
        invalid_url = reverse('download_file') + '?token=invalidtoken'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or expired token", response.json()['error'])

    def test_download_file_unauthorized_user(self):
        self.client.logout()
        self.client.login(username='opsuser', password='password')  # Login as Ops user
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Unauthorized access", response.json()['error'])

    def test_download_file_no_authentication(self):
        self.client.logout()
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Unauthorized access", response.json()['error'])
