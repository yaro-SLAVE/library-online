"""Test URLs configuration - uses TokenObtainPairView instead of OPAC-based auth"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from app.urls import router
from library_service.views.bitrix import BitrixAuthView
from library_service.views.auth import AuthThirdPartyViewset

urlpatterns = [
    path("admin/", admin.site.urls),
    # Use standard JWT auth for tests instead of OPAC-based auth
    path("api/auth/login/", TokenObtainPairView.as_view()),
    path("api/auth/bitrix-login/", BitrixAuthView.as_view()),
    path("api/auth/third-party/", AuthThirdPartyViewset.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),
    path("api/auth/logout/", TokenBlacklistView.as_view()),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
