import django_filters

from comments.models import Comment


class CommentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="user__username",
        lookup_expr="icontains"
    )
    text = django_filters.CharFilter(
        field_name="text",
        lookup_expr="icontains"
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    class Meta:
        model = Comment
        fields = [
            "user",
            "text",
            "created_at"
        ]
