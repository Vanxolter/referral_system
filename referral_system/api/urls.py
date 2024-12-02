from django.urls import include, path
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import SendCodeView, VerifyCodeView, UserProfileView, ActivateInviteCodeView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="Referral System API",
        default_version='v1',
        description="API for the referral system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@referralapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

urlpatterns = [
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/send-code/", SendCodeView.as_view(), name="send_code"),
    path("api/v1/verify-code/", VerifyCodeView.as_view(), name="verify_code"),
    path('api/v1/profile/', UserProfileView.as_view(), name='profile'),
    path('api/v1/activate-invite/', ActivateInviteCodeView.as_view(), name='activate_invite'),
    path("api/v1/", include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
