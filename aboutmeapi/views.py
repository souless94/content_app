from rest_framework import viewsets, permissions, authentication
from aboutmeapi import serializers
from core.models import Content


class ContentViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.ContentSerializer
    queryset = Content.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    filterset_fields = '__all__'
