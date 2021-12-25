import sendgrid
from decouple import config
from rest_framework import status
from rest_framework.generics import GenericAPIView
from sendgrid.helpers.mail import (Mail,
                                   Email,
                                   Personalization
                                   )
from python_http_client import exceptions
from rest_framework.response import Response
from rest.settings import DEFAULT_FROM_EMAIL, SENDGRID_API_KEY

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)


class MailSenderAPIView(GenericAPIView):

    def send_mail(self, template_id, sender, recipient, data_dict):
        mail = Mail()
        mail.template_id = template_id
        mail.from_email = Email(sender)
        personalization = Personalization()
        personalization.add_to(Email(recipient))
        personalization.dynamic_template_data = data_dict
        mail.add_personalization(personalization)

        try:
            sg.client.mail.send.post(request_body=mail.get())
        except exceptions.BadRequestsError as e:
            return Response(status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        recepient_email = request.data['recepient_email']
        subject = request.data['subject']
        fullname = request.data['fullname']
        body = request.data['body']
        template_id = config("template_id")
        sender = DEFAULT_FROM_EMAIL
        data_dict = {"subject": subject, "user_name": fullname, "body": body}
        MailSenderAPIView.send_mail(self, template_id, sender, recepient_email, data_dict)

        return Response({"status_code": status.HTTP_200_OK, "message": "Mail sent successfully."})
