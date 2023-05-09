from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import (
    SlugRelatedField,
    StringRelatedField,
    PrimaryKeyRelatedField,
)
from rest_framework.exceptions import ValidationError

from posts.models import Group, Post, Comment, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    group = PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )
    comments = StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    post = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        model = Follow
        fields = (
            "following",
            "user",
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=[
                    "user",
                    "following",
                ],
                message="Подписка уже есть",
            )
        ]

    def validate_following(self, value):
        following = get_object_or_404(User, username=value)
        if not following:
            raise ValidationError(
                detail="Нет такого значения в поле following"
            )
        if following.id == self.context["request"].user.id:
            raise ValidationError(detail="Нельзя подписаться на себя")
        return following
