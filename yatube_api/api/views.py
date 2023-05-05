from rest_framework import viewsets, permissions, mixins, filters
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

# from django.http import HttpResponseBadRequest
from posts.models import Post, Group, Follow, User
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer,
)
from .permissions import CheckAllowChange
from rest_framework.exceptions import ValidationError


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (CheckAllowChange,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (
        CheckAllowChange,
        permissions.IsAuthenticated,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if "following" not in self.request.data:
            raise ValidationError
        try:
            following = User.objects.get(
                username=self.request.data["following"]
            )
            if following.id == self.request.user.id:
                raise ValidationError(detail="Нельзя подписаться на себя")
            if Follow.objects.filter(
                user=self.request.user, following=following
            ).exists():
                raise ValidationError(detail="Подписка уже есть")
            serializer.save(user=self.request.user, following=following)
        except Exception:
            raise ValidationError


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CheckAllowChange,)

    def get_queryset(self):
        post = self.get_post_from_url_params(self.kwargs)
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post_from_url_params(self.kwargs)
        serializer.save(author=self.request.user, post=post)

    def get_post_from_url_params(self, kwargs):
        post_id = kwargs.get("post_id")
        return get_object_or_404(Post, pk=post_id)
