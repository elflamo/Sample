from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from main import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token/obtain', obtain_jwt_token),
    url(r'^token/verify', verify_jwt_token),
    url(r'^token/refresh', refresh_jwt_token),
    url(r'^signup$', views.SignupView.as_view(), name="signup"),
    url(r'^login$', views.LoginView.as_view(), name="login")

]
