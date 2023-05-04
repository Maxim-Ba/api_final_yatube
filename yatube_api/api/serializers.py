from rest_framework import serializers
from rest_framework.relations import (
    SlugRelatedField,
    StringRelatedField,
    PrimaryKeyRelatedField,
)
from posts.models import Group, Post, Comment, Follow


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
    following = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = ("following", "user")
