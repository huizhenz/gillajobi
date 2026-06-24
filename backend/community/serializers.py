from rest_framework import serializers
from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    label_name = serializers.CharField(source='label.name', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    class CommentSerializer(serializers.ModelSerializer):
        username = serializers.CharField(source='user.username', read_only=True)
        class Meta:
            model = Comment
            fields = '__all__'

    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    label_name = serializers.CharField(source='label.name', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)

    def get_comment_count(self, obj):
        return obj.comments.count()


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')