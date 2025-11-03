"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from adrf.routers import DefaultRouter as AsyncDefaultRouter

from library_service.views.basket import BasketViewset
from library_service.views.bitrix import BitrixAuthView
from library_service.views.catalog import BookViewset, LibraryViewset, ScenarioViewset
from library_service.views.library_settings import LibrarySettingsViewSet
from library_service.views.order import BorrowedViewset, OrderViewset
from library_service.views.profile import ProfileViewset, ProfileBannedViewset
from library_service.views.staff_order import StaffOrderViewset, StaffOrderGetUpdateViewset, StaffBorrowedViewset
from library_service.views.comments import OrderCommentViewset, OrderItemCommentViewset
from library_service.views.auth import AuthViewset, AuthThirdPartyViewset

router = AsyncDefaultRouter()
router.register("book", BookViewset, basename="book")
router.register("library", LibraryViewset, basename="library")
router.register("scenario", ScenarioViewset, basename="scenario")
router.register("basket", BasketViewset, basename="basket")
router.register("profile", ProfileViewset, basename="profile")
router.register("profile/banned", ProfileBannedViewset, basename="profile-banned")
router.register("order", OrderViewset, basename="order")
router.register("borrowed", BorrowedViewset, basename="borrowed")
router.register("library-settings", LibrarySettingsViewSet, basename="library-settings")
router.register("staff", StaffOrderViewset, basename="staff")
router.register("staff/order", StaffOrderGetUpdateViewset, basename="staff/order")
router.register("staff/order/borrowed", StaffBorrowedViewset, basename="staff/order/borrowed")
router.register("reasons/cancel", OrderCommentViewset, basename="reasons/cancel")
router.register("reasons/notfound", OrderItemCommentViewset, basename="reasons/notfound")

urlpatterns = [
    path("admin/", admin.site.urls),
    #FIXME[Ilya] Эту строку раскомметировать следущую за ней удалить
    #path("api/auth/login/", AuthViewset.as_view()),
    path("api/auth/login/", TokenObtainPairView.as_view()),
    path("api/auth/bitrix-login/", BitrixAuthView.as_view()),
    path("api/auth/third-party/", AuthThirdPartyViewset.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),
    path("api/auth/logout/", TokenBlacklistView.as_view()),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
