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


class CommentListSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()

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

    def get_replies(self, obj: Comment):
        comments = obj.replies.prefetch_related("user").all()

        return CommentListSerializer(comments, many=True).data
