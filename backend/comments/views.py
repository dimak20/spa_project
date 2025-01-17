from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from comments.filters import CommentFilter
from comments.models import Comment
from comments.paginators import CustomCommentPagination


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    filterset_class = CommentFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = [
        "created_at",
        "user__username",
        "user__email"
    ]
    ordering = ["-created_at"]
    pagination_class = CustomCommentPagination
