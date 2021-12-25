from django.conf.urls import url
from mailprovider.views import MailSenderAPIView

urlpatterns = [
    url('sendTemplateEmail', MailSenderAPIView.as_view(), name="mail-sender"),
]