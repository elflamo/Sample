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
    url(r'^send/reset/otp$', views.SendResetOtpView.as_view(), name="send-otp-email"),
    url(r'^check/otp$', views.CheckOtpView.as_view(), name="check-otp"),
    url(r'^reset/password$', views.ResetPasswordView.as_view(), name="reset-password"),
    url(r'^dashboard/basics$', views.DashboardBaseView.as_view(), name="dashboard-base"),
    url(r'^store/$', views.ListCreateStoreView.as_view(), name="list-create-store"),
    url(r'^store/(?P<pk>\d+)/$', views.RUDStoreView.as_view(), name="RUD-Store")

]
