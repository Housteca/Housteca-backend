import os

from django.conf import settings

from common.ethereum import w3


def get_document(document_hash: str) -> bytes:
    path = os.path.join(settings.STORAGE_PATH, document_hash)
    if not os.path.isfile(path):
        raise ValueError('Invalid path')
    with open(path, 'rb') as file:
        return file.read()


def add_document(contents: bytes) -> str:
    document_hash = w3.keccak(contents).hex()
    path = os.path.join(settings.STORAGE_PATH, document_hash)
    with open(path, 'wb') as file:
        file.write(contents)
    return document_hash
