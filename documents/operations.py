import os

import ipfshttpclient
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from common.ethereum import w3
from documents.models import Document
from users.models import User

MAX_SIZE = 10485760


def _validate_size(size: int) -> None:
    if size > MAX_SIZE:
        raise ValueError('Maximum file size is 10MB')


def get_document(document_hash: str) -> bytes:
    path = os.path.join(settings.STORAGE_PATH, document_hash)
    if not os.path.isfile(path):
        raise ValueError('Invalid path')
    with open(path, 'rb') as file:
        return file.read()


def add_document(file: UploadedFile, user: User) -> Document:
    document_hash = store_document(file.read())
    obj, _ = Document.objects.update_or_create(
        hash=document_hash,
        name=file.name,
        content_type=file.content_type,
        size=file.size,
        user=user,
    )
    return obj


def store_document(contents: bytes) -> str:
    _validate_size(len(contents))
    document_hash = w3.keccak(contents).hex()
    path = os.path.join(settings.STORAGE_PATH, document_hash)
    with open(path, 'wb') as file:
        file.write(contents)
    return document_hash


def add_image_to_ipfs(contents: bytes) -> str:
    _validate_size(len(contents))
    with ipfshttpclient.connect(settings.IPFS_URI) as client:
        return client.add_bytes(contents)
