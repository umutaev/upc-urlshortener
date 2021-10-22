from django.urls import path

from . import views

app_name = "url_shortener"
urlpatterns = [
    path("shorten", views.generate_link, name="shorten"),
    path("<str:token>", views.redirect_to_link, name="token_redirect"),
    path("<str:token>/views", views.get_views, name="views_count"),
]
