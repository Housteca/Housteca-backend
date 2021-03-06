from django.db import models


class Document(models.Model):
    hash = models.CharField(max_length=66, primary_key=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    content_type = models.CharField(max_length=128, null=True, blank=True)
    size = models.PositiveIntegerField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='documents')
    property = models.ForeignKey('properties.Property', on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self) -> str:
        return self.pk
