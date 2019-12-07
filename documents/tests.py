import base64
from typing import Dict, Any

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.response import Response

from common.ethereum import w3
from common.test_utils import BaseTestAPI
from documents.models import Document


class DocumentCreateListAPITest(BaseTestAPI):
    def setUp(self) -> None:
        super().setUp()
        self.file_name = 'test.txt'
        self.file_contents = b'sample content'

    def upload_document(self) -> Response:
        file = SimpleUploadedFile(self.file_name, self.file_contents, content_type="text/plain")
        return self.client.post('/api/v1/documents/', {'file': file}, **self.credentials())

    def check_response(self, data: Dict[str, Any]) -> None:
        self.assertEqual(data['name'], self.file_name)
        self.assertEqual(data['content_type'], 'text/plain')
        self.assertEqual(data['hash'], w3.keccak(self.file_contents).hex())
        self.assertEqual(data['contents'], base64.b64encode(self.file_contents).decode())
        self.assertEqual(data['user'], self.user.pk)

    def test_upload_document_should_work(self) -> None:
        response = self.upload_document()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.check_response(response.data)

    def test_list_documents_should_work(self) -> None:
        response = self.upload_document()
        self.check_response(response.data)
        response = self.client.get('/api/v1/documents/', **self.credentials())
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        self.check_response(response.data[0])

    def test_retrieve_documents_should_work(self) -> None:
        response = self.upload_document()
        self.check_response(response.data)
        document_hash = response.data['hash']
        response = self.client.get(f'/api/v1/documents/{document_hash}/', **self.credentials())
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.check_response(response.data)
