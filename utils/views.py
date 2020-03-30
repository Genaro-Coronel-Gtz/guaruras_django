"""
    Created by: @pdonaire1 October 06, 2016
    Ing. Pablo Alejandro González Donaire
"""
from django import forms
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from utils.temporary_token import TemporaryToken
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token # Optional if you will use extra_token
from rest_framework.response import Response

class ResetPasswordViewSet(APIView):
    permission_classes = ()
    
    def send_forgot_password_email(self, user, email_token):
        template = render_to_string('email/forgot_password.html',
            {
                'email_token': email_token,
                'username': user.username})
        # try:
        subject = "Recuperar usuario @ MyAPP"
        email_to = user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        text_plain = "Hello,\n. Enter to retrieve your user.\Thanks."
        send_mail(subject, text_plain, from_email, [email_to], html_message=template)
        # except: pass

    def get(self, request, format=None):
        username = request.GET.get("email", None)
        if username and User.objects.filter(email=username).exists():
            user = User.objects.get(email=username)
            # Let's send an email to recover password
            temporary_token = TemporaryToken(user)
            token = Token.objects.get_or_create(user=user)  # Optional
            token = token[0].key  # Optional for extra security
            email_token = temporary_token.hash_user_encode(
                hours_limit=24, extra_token=token)
            self.send_forgot_password_email(user, email_token)
            return Response([{
                "message": "An email has been send to your user",
                "success": True
            }])
        return Response([{
            "POST": "Reset password params: {email_token, new_password, username}",
            "GET": "Send email forgot password params: {username}",
        }])

    def post(self, request, format=None):
        """
            This function recibe: 
            email_token, new_password, username
        """
        # email_token = request.data["email_token"]
        email = request.data["email"]
        new_password = request.data["new_password"]
        # username = request.data["username"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # temporary_token = TemporaryToken(user)
            # Optional this step is if was created an extra_token:
            # token = Token.objects.get(user=user).key
            # if temporary_token.hash_user_valid(email_token, extra_token=token):
            user.set_password(new_password)
            user.save()
            return Response(
                [{"message": "Password changed", "success": True}], 
                status=status.HTTP_201_CREATED)

        return Response([{"message": "Token or username error", "success": False}],
            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordViewSet(APIView):
    permission_classes = ()
    
    def post(self, request, format=None):
        """
            This function recibe: 
            old_password, new_password, username
        """
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        # username = request.data["username"]
        # user = User.objects.get(username=username)
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        if  user.check_password(old_password):    
            user.set_password(new_password)
            user.save()
            return Response(
                [{"message": "Clave cambiada satisfactoriamente", "success": True}], 
                status=status.HTTP_201_CREATED)

        return Response([{"message": "Datos invalidos", "success": False}],
            status=status.HTTP_400_BAD_REQUEST)

