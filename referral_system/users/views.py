from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.serializers import PhoneNumberSerializer, CodeVerificationSerializer, UserProfileSerializer
import logging

from users.services.generating import generate_verify_code, temp_stor_for_codes
from users.services.sending_code import sending_process

logger = logging.getLogger(__name__)
User = get_user_model()


class SendCodeView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = generate_verify_code()

        temp_stor_for_codes(phone_number=phone_number, code=code, process="add")
        sending_process(phone_number, code)

        # Логирование кода, т.к. это имитация отправки смс
        logger.info(f"Code for {phone_number}: {code}")

        return Response({"message": "Code sent successfully"}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = CodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        if temp_stor_for_codes(phone_number=phone_number, process="get") != int(code):
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        temp_stor_for_codes(phone_number=phone_number, process="remove")

        user, created = User.objects.get_or_create(phone_number=phone_number)

        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ActivateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invite_code = request.data.get('invite_code')
        if not invite_code:
            raise ValidationError({"error": "Invite code is required"})

        try:
            inviter = User.objects.get(invite_code=invite_code)
        except User.DoesNotExist:
            return Response({"error": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.activated_invite_code:
            return Response(
                {"error": "You have already activated an invite code"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.activated_invite_code = invite_code
        request.user.save()

        inviter.referred_users.add(request.user)
        inviter.save()

        return Response({"message": "Invite code activated successfully"}, status=status.HTTP_200_OK)
