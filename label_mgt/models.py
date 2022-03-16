from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey(
        'self', related_name='children', null=True, blank=True,
        on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    metadata_outcome = models.CharField(max_length=255, blank=True)
    metadata_politics = models.CharField(max_length=255, blank=True)
    labelled_by = models.ForeignKey(
        User, related_name='labelled_datapoints', null=True, blank=True,
        verbose_name=_("User"), on_delete=models.SET_NULL)
    label = models.ForeignKey(
        Category, related_name='datapoints', null=True, blank=True,
        on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
