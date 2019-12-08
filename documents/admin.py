from typing import Iterable, Union, Optional

from compat import URLResolver
from django import forms
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern, path
from django.utils.html import format_html

from documents.models import Document
from documents.operations import get_document, add_document


class AdminForm(forms.ModelForm):
    file = forms.FileField()

    def save(self, commit: bool = True) -> Document:
        file = self.cleaned_data['file']
        user = self.cleaned_data['user']
        return add_document(file, user)

    def save_m2m(self) -> None:
        pass

    class Meta:
        model = Document
        fields = ['user', 'file']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = AdminForm

    list_display = ('hash', 'user', 'name', 'size', 'content_type', 'created_at', 'download',)
    search_fields = ('hash', 'name', 'user__address', 'user__first_name', 'user__last_name', 'user__email',)

    def download(self, document: Document) -> str:
        return format_html(f'<a href="{document.pk}/download/">Download</a>')

    def has_change_permission(self, request: HttpRequest, obj: Optional[Document] = None):
        return False

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
