from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Tag

class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
