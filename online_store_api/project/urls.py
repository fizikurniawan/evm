from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import RedirectView

from django.urls import path

from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class RedirectVerifyView(RedirectView):
    query_string = True


urlpatterns = [
    path(
        "api/",
        include(("api.urls", "api"), namespace="api"),
    ),
]


if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Evermos Online Store",
            default_version="v1",
            description="Assessment Test",
            contact=openapi.Contact(email="fizikurniawan@gmail.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        url=settings.BASE_URL,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns.append(
        url(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        )
    )
    urlpatterns.append(
        url(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        )
    )
    urlpatterns.append(
        url(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        )
    )

    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns.append(url(r"^", RedirectView.as_view(url="/swagger/")))
