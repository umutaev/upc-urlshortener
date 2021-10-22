import json

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import models


@csrf_exempt
def redirect_to_link(request, token):
    url = get_object_or_404(
        models.UrlModel.objects.filter(shortened_token__exact=token)
    )
    url.origin = "http://" + url.origin if not "http" == url.origin[0:4] else url.origin
    url.views += 1
    url.save()
    return redirect(url.origin, permanent=True, data="{}")


@csrf_exempt
def get_views(request, token):
    url = get_object_or_404(
        models.UrlModel.objects.filter(shortened_token__exact=token)
    )
    return JsonResponse({"viewCount": url.views})


@csrf_exempt
@require_http_methods(["POST"])
def generate_link(request):
    try:
        url = models.UrlModel(origin=json.loads(request.body)["urlToShorten"])
    except KeyError:
        return JsonResponse({"status": "Bad Request"}, status=400)
    url.save()
    return JsonResponse(
        {
            "status": "Created",
            "shortenedUrl": f"http://{request.META['HTTP_HOST']}{url.__str__()}",
        },
        status=201,
    )
