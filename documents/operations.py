import os

import ipfshttpclient
from django.conf import settings

from common.ethereum import w3

MAX_SIZE = 10485760


def _validate_image_size(size: int) -> None:
    if size > MAX_SIZE:
        raise ValueError('Maximum file size is 10MB')


def get_document(document_hash: str) -> bytes:
    path = os.path.join(settings.STORAGE_PATH, document_hash)
    if not os.path.isfile(path):
        raise ValueError('Invalid path')
    with open(path, 'rb') as file:
        return file.read()


def add_document(contents: bytes) -> str:
    _validate_image_size(len(contents))
    document_hash = w3.keccak(contents).hex()
    path = os.path.join(settings.STORAGE_PATH, document_hash)
    with open(path, 'wb') as file:
        file.write(contents)
    return document_hash


def add_image_to_ipfs(contents: bytes) -> str:
    _validate_image_size(len(contents))
    client = ipfshttpclient.connect(settings.IPFS_URI)
    ipfs_hash = client.add_bytes(contents)
    client.close()
    return ipfs_hash
