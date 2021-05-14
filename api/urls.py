from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('news', views.News.as_view(), name="news"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/swagger', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('docs', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]

app_name = 'api'