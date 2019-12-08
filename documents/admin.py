from typing import Iterable, Union

from compat import URLResolver
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern, path
from django.utils.html import format_html

from documents.models import Document
from documents.operations import get_document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('hash', 'user', 'name', 'size', 'content_type', 'created_at', 'download')

    def download(self, document: Document) -> str:
        return format_html(f'<a href="{document.pk}/download/">Download</a>')

    download.short_description = 'Download'
    download.allow_tags = True

    @staticmethod
    def download_document(_: HttpRequest, object_id: str) -> HttpResponse:
        document_bytes = get_document(document_hash=object_id)
        document = Document.objects.get(pk=object_id)
        response = HttpResponse(
            content=document_bytes,
            content_type=document.content_type,
        )
        response['Content-Disposition'] = f'attachment; filename={document.name}'
        return response

    def get_urls(self) -> Iterable[Union[URLPattern, URLResolver]]:
        urls = super().get_urls()
        extra_urls = [
            path('<path:object_id>/download/', self.admin_site.admin_view(self.download_document),
                 name='documents_document_download'),
        ]
        return extra_urls + urls
