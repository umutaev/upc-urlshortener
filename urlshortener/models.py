from math import nan
import nanoid
from django.db import models
from django.urls import reverse


def generate_token() -> str:
    token = "abcdefgh"
    return token


class UrlModel(models.Model):
    origin = models.URLField("original_link_url")
    shortened_token = models.TextField(
        "shortened_url_token",
        max_length=8,
        unique=True,
        default=nanoid.generate,
    )
    views = models.IntegerField("link_views", default=0)

    def __str__(self) -> str:
        return reverse("url_shortener:token_redirect", args=(self.shortened_token,))
