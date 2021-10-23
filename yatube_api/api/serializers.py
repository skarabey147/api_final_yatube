from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Group, Comment, Post, Follow, User
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username', read_only=True, default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    # def validate_following(self, following):
    #     user = self.context['request'].user
    #     if user != following:
    #         return following
    #     raise serializers.ValidationError('Нельзя подписаться на самого себя')

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]
