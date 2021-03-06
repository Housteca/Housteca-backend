from typing import Dict, Any

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.response import Response

from common.ethereum import w3
from common.test_utils import BaseTestAPI

SAMPLE_FILE = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x03\x15IDATx\xda\xccWMh\x13A\x14\x9eM@+H"\x1e\xeaAm{\x8f)\xed\xcd*\xc2\xd6\xbfJ\x91\x80\xc5\x16\x8a\x95T\xf4\x10\x7f\x0em\x10k\xea%\x1e\xac\xb4\x87\xc4\x83H\x0f\x8a\x15-\x85\xf6\xe0\x0fR\xf0\x94\x04\x11s2\xfe4\x17E\xd06BU\x10\xa2\x82\xc4\x8b\xbeo\x98\xd5]\x9b\xddy\xeb\xa9\x0f\x96Ivg\xe6\xbdy\xdf\xf7~\xc6\x10>e\xf3\xc6\xf5&\r\xa6\xfa\xdb\xac\xc6\xf7j\xcc\x7f\xf8\xf2=\xefg?\xc3\x87\xd28=\x83\xcc}\xa7\xe8\xb9\xc51\xc6\xd0(n\xa3!k;\xb1_\x81\x01\xc3d\xc8s\xb7\t\x01\x0f\xe5C4\x94\xbc\x94\x87\xc2a\x9d\x01X[R{\xd5\x95\xa0\x8b\xf2\x9b4\x9c\xd7\xed^(>\x13\xe5\x85W\xa2\xb2\xb4\xa8\x9bz \xb4nM\xcb\xb7\x1f?\xefk=\xa0\x94k\xb1N\x8e\x8c\x8a-MM"{u\x92\x0b\xc7\xa0\xda\xdb\xdd\x03\xcaU\xda\x93o%\xc57n\xcf\xfc\x85\xc10\xc4\xd3\'\x8f9F\xb4\x91\'\xaa\xe4\x89\xe2\n\x12*\xc2\x958\xbb\xcc=\x98\x17\x1d;w9\xdeu\xb4G\xc4\xd2\xe2"\xd7\x1b\xed\x161\xed\x10d9+\xfb\xfa\x8f\xacP\x0e\xc9\xf0\xa1p\xe8\n\xda\xe2<\xad[\x05w\xdf\x99\xbd+\xd664\xd4\x81\xa5Y\x92\x11\xa4dH\x0bAQ (\xdeY\x1e\x88sV]\xbc4\xee\x19zi\xcd\xf7\x7f$n\x87@\xcbz\xb8\xbd\x97\xdc\xaf\xf3\x10\x8c\xe4F\x85$\xa1r\x7fN7\xbbX*\xcb\xb0\xe3Ho\xac\x9b\x1b\x15\x9d\x01N\x9a\xb5b\x9e\xcd0>!\xcd \x91\xc1\xf42\xc2\x1e\xf3\\\xf1\x91\x1b\n\x01\xdd\x8c4\x1fS\xa7\xd7\xce\xa5\xa4\xf1:\xd1\x1bpaD\xcc\xcdL\xfbR^\xa1\x84t\xfch?+1i\r\xc0&\xc3g\x12,b}\xadV\xa5\xc1\xdb)+>\x9a\x7f\xc82Vk@d[\xab\x1c\xa1\x1cF$\xc9\x98J\x9d\x93]\x9f\xbc&\x15c\xb4\xb8\xc3\x85\xc0\xb3k\x89D\xa3\x8e\xdc?Kp\xec7w\x88\xcc\xc4eyb\x18\x86:\x80\x93\xe3?\x08\x88\xa8Ajf@\x907T*\xfe\xa5\x0b+$!p!31\xe6\xba\xf1\x89\xc4)"\xdf\xa8\xfc\ro\xc0 /\xa1\x82d\xc8Z\x80f\x01\xa5\xd2m"Ni\xee\xd9K\xcf>*F\x03\xb2\x16\x94\x17^\x8aZ\xad&\xbfwu\x1f\x14\xd3T#b=\x87\xe5\xb7\x81\xbe\x1e\xf1\xf6\xcdkm\xdf\x88\x06\xc5\xb0\x15\xa3\x9c\x8e\x0b\x80\xc2\xca\xf58\x1d\xbc\x01\xe5\xf6\xea\x08h2\xe3c\xac,\x88\xa6\xd5\xde\x0f\xe4tY\x11\xa5\xd8\xab\xecZD\xe54\xab\xa4\xbc\xd3\xd1\x11\x11\x0c/hHx\xadB\xa9E\xd9\x8dD[\xeb\x86`\xack\xf7\x1fX4r\x88\xdc\xbf\xec0\x00/\xd0.\xa1\x81\xf4Zi\xf1\xa1\xb1q\x93\xe3=\x13w\xa1\xda\xf4{u\xf3\x00}\xb8\xa2.\x15\x9e\xc9&y\xfa\xa4\x83\xe1\xc0\x9dY\xfd\xa6\x94\x0e\xf7\xb6\x1c\xcc\xd4E\xc5\xe7O\x1f\xe5\x03\x02B1\x92\x13S\xf91\xd6\xbd@\x19\xe1\t\x07\xf8\x10\no\x10\xa9\xb3C\x1c\xdc\xe1\xf6\xd4\xaa\xbc\x9a\xad\xee\xcb)\xe3znu\xa0\xd5\xff\xbd\x9e\xff\x16`\x00\xa4\x82VA\xfe\xcf\xcf\xe8\x00\x00\x00\x00IEND\xaeB`\x82'


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
        self.assertEqual(response.data, self.file_contents)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={self.file_name}')
        self.assertEqual(response['Content-Type'], 'text/plain')


class IPFSUploadTest(BaseTestAPI):
    def test_upload_to_ipfs_should_work(self) -> None:
        image = SimpleUploadedFile('image.png', SAMPLE_FILE, content_type="image/png")
        response = self.client.post('/api/v1/images/', {'file': image}, **self.credentials())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['hash'], 'QmQ6me2j1NDDwppuCm1PGAm1GQdjeRjChxSGbio7Zh7pQP')
