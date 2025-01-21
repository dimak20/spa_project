from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from faker.proxy import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

from comments.models import Comment
from comments.serializers import CommentListSerializer

COMMENT_URL = reverse("comments:comment-list")
fake = Faker()


def detail_url(comment_id: int) -> str:
    return reverse(
        "comments:comment-detail",
        args=(str(comment_id),)
    )


def generate_random_email() -> str:
    return fake.email()


def generate_random_username() -> str:
    return fake.user_name()


def generate_random_password() -> str:
    return fake.password()


def generate_random_sentence() -> str:
    return fake.sentence()


class UnauthenticatedCommentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(COMMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedCommentApiTests(TestCase):
    def sample_user(self, **params) -> get_user_model():
        email = generate_random_email()
        username = generate_random_username()
        password = generate_random_password()
        defaults = {
            "username": username,
            "email": email,
            "password": password,
        }
        defaults.update(params)
        return get_user_model().objects.create(**defaults)

    def sample_comment(self, **params) -> Comment:
        text = generate_random_sentence()
        defaults = {
            "user": self.user,
            "text": text,
        }
        defaults.update(params)
        return Comment.objects.create(**defaults)

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="user123", email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_comment_list(self):
        [self.sample_comment() for _ in range(5)]
        comments = Comment.objects.order_by("-created_at")
        comment_serializer = CommentListSerializer(comments, many=True)
        response = self.client.get(COMMENT_URL)

        self.assertEqual(
            response.data["results"],
            list(comment_serializer.data)
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_filter_comment_by_text(self):
        [self.sample_comment() for _ in range(5)]
        self.sample_comment(text="test_text")
        correct_comment = Comment.objects.filter(text__icontains="test")
        comment_serializer = CommentListSerializer(correct_comment, many=True)
        response = self.client.get(
            COMMENT_URL,
            {
                "text": "test"
            }
        )

        self.assertEqual(
            list(response.data["results"]),
            list(comment_serializer.data)
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_order_comment_by_created_at_desc(self):
        [self.sample_comment() for _ in range(15)]
        comments_desc = Comment.objects.order_by("-created_at")
        comments_desc_serializer = CommentListSerializer(comments_desc, many=True)

        response = self.client.get(
            COMMENT_URL,
            {
                "ordering": "-created_at"
            }
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        self.assertEqual(
            list(response.data["results"]),
            list(comments_desc_serializer.data)
        )

    def test_order_comment_by_created_at_asc(self):
        [self.sample_comment() for _ in range(15)]
        comments_asc = Comment.objects.order_by("created_at")
        comments_asc_serializer = CommentListSerializer(comments_asc, many=True)

        response = self.client.get(
            COMMENT_URL,
            {
                "ordering": "created_at"
            }
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        self.assertEqual(
            list(response.data["results"]),
            list(comments_asc_serializer.data)
        )

    def test_comment_list_paginated(self):
        [self.sample_comment() for _ in range(50)]
        comments = Comment.objects.all()[25:50]
        comments_serializer = CommentListSerializer(comments, many=True)

        response = self.client.get(
            COMMENT_URL,
            {
                "page": 2
            }
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        self.assertEqual(
            response.data["results"],
            list(comments_serializer.data)
        )

    @patch("comments.views.verify_recaptcha", return_value={"success": True})
    def test_comment_create(self, mock_verify_recaptcha):
        payload = {
            "text": generate_random_sentence(),
            "user": self.user.id,
            "captcha": "123"
        }

        response = self.client.post(
            COMMENT_URL,
            payload
        )

        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )
        mock_verify_recaptcha.assert_called_once_with("123")
        self.assertEqual(
            response.data["text"],
            payload["text"]
        )
