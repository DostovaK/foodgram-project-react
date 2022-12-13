from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginator import CustomPaginator
from api.serializers import ShowSubscriptionsSerializer, UserSerializer
from users.models import Follow, User


class UserViewSet(UserViewSet):
    """Users' model processing viewset."""
    serializer_class = UserSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Method returns a queryset with required properties."""
        user = get_object_or_404(User, id=self.request.user.id)
        is_subscribed = Follow.objects.filter(user=user, author=OuterRef('id'))
        return User.objects.annotate(
            is_subscribed=Exists(is_subscribed)
        )

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, **kwargs):
        """Method allows follow any user or unfollow."""
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = ShowSubscriptionsSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Follow, user=user, author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def subscriptions(self, request):
        """Method shows user's subscriptions."""
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = ShowSubscriptionsSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
