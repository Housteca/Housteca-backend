from django.urls import re_path

from documents.views import ListCreateDocumentAPI, RetrieveDocumentAPI, UploadImageToIPFSAPI

urlpatterns = [
    re_path(r'^$', ListCreateDocumentAPI.as_view(), name='list_create_document_api'),
    re_path(r'^(?P<pk>0x[0-9a-f]{64})/?$', RetrieveDocumentAPI.as_view(), name='retrieve_document_api'),
]
