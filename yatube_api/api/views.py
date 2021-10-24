from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Получение списка публикаций, с пагинацией при
    установке параметров limit, offset. Удаление, редактирование
    для авторизованных пользователей
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    Получение списка сообществ и информация отдельного сообщества
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получение списка комментариев, с пагинацией при
    установке параметров limit, offset. Удаление, редактирование
    для авторизованных пользователей
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created',)

    def get_queryset(self, **kwargs):
        queryset = Comment.objects.filter(
            post_id=int(self.kwargs.get('post_id'))
        )
        return queryset

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            post_id=int(self.kwargs.get('post_id'))
        )


class FollowViewSet(viewsets.ModelViewSet):
    """
    Просмотр подписок пользователя.
    Подписка, отписка на авторов для авторизованных пользователей
    """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        queryset = user.follower.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
