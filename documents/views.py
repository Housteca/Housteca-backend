from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document
from documents.operations import add_document, add_image_to_ipfs
from documents.serializers import DocumentSerializer


class ListCreateDocumentAPI(ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self) -> QuerySet:
        return Document.objects.filter(user=self.request.user)

    def create(self, request: Request, *args, **kwargs) -> Response:
        file = self.request.FILES['file']
        if not file:
            raise APIException('No file found')
        contents = file.read()
        document_hash = add_document(contents)
        data = {
            'hash': document_hash,
            'name': file.name,
            'content_type': file.content_type,
            'size': file.size,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveDocumentAPI(RetrieveAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self) -> QuerySet:
        return Document.objects.filter(user=self.request.user)


class UploadImageToIPFSAPI(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        image = request.FILES['image']
        if not image:
            raise APIException('No image found')
        if image.content_type not in ('image/jpeg', 'image/png'):
            raise APIException('Only JPEF and PNG formats are supported')
        contents = image.read()
        document_hash = add_image_to_ipfs(contents)
        return Response({'hash': document_hash}, status=status.HTTP_201_CREATED)
