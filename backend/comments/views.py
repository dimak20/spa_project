from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework_extensions.cache.decorators import cache_response

from comments.filters import CommentFilter
from comments.models import Comment
from comments.paginators import CustomCommentPagination
from comments.serializers import CommentSerializer, CommentListSerializer
from comments.utils import verify_recaptcha, generate_key


class CommentView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Comment.objects.filter(parent=None)
    filterset_class = CommentFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["created_at", "user__username", "user__email"]
    ordering = ["-created_at"]
    pagination_class = CustomCommentPagination

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        return CommentSerializer

    # @cache_response(60 * 3, key_func=generate_key)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        recaptcha_token = self.request.data.get("captcha")
        result = verify_recaptcha(recaptcha_token)

        if not result.get("success"):
            return ValidationError("Invalid reCAPTCHA.")
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            return queryset.prefetch_related("user", "replies__user")

        return queryset
