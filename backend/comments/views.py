from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter

from comments.filters import CommentFilter
from comments.models import Comment
from comments.paginators import CustomCommentPagination
from comments.serializers import CommentSerializer, CommentListSerializer


class CommentView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
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

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            return queryset.prefetch_related(
                "user",
                "replies__user"
            )

        return queryset
