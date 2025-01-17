from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import generics

from comments.filters import CommentFilter
from comments.models import Comment


class CommentView(generics.ListCreateAPIView):
    model = Comment
    queryset = Comment.objects.all()
    filterset_class = CommentFilter
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = [
        "created_at",
        "user__username",
        "user__email"
    ]
