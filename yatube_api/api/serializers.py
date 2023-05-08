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
    following = serializers.StringRelatedField()
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = (
            "following",
            "user",
        )

    def validate(self, data):
        if "following" not in self.initial_data:
            raise ValidationError(detail="Нет поля following")

        if not User.objects.filter(
            username=self.initial_data["following"]
        ).exists():
            raise ValidationError(
                detail="Нет такого значения в поле following"
            )

        following = User.objects.get(username=self.initial_data["following"])
        if following.id == self.context["request"].user.id:
            raise ValidationError(detail="Нельзя подписаться на себя")

        if Follow.objects.filter(
            user=self.context["request"].user, following=following
        ).exists():
            raise ValidationError(detail="Подписка уже есть")

        return data
