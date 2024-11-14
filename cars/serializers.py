from rest_framework import serializers
from .models import Car, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'car']

class CarSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year', 'description', 
                 'created_at', 'updated_at', 'owner', 'comments']