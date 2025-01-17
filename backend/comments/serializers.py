from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "home_page",
            "user",
            "text",
            "updated_at",
            "created_at",
            "attached_image",
            "attached_file",
            "parent"
        ]
        read_only_fields = [
            "user",
            "id",
            "created_at",
            "updated_at",
            "parent"
        ]


class CommentListSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "home_page",
            "user",
            "text",
            "updated_at",
            "created_at",
            "attached_image",
            "attached_file",
            "replies"
        ]
        read_only_fields = [
            "user",
            "id",
            "created_at",
            "updated_at",
            "parent"
        ]

    def get_user(self, obj: Comment):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email
        }

    def get_replies(self, obj: Comment):
        comments = obj.replies.all()

        return CommentListSerializer(comments, many=True).data
