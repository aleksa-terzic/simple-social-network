import json

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from src.retry import retry_session
from users.models import User
from users.tasks import enrich_user

from .serializers import UserSerializer


def is_deliverable(email):
    data = {}
    session = retry_session(retries=3)
    response = session.get(
        f"https://emailvalidation.abstractapi.com/v1/?api_key={settings.ABS_API_KEY_EMAIL}&email={email}")
    data = response.content
    return json.loads(data)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            check = is_deliverable(email)
            if check['deliverability'] == 'DELIVERABLE':
                user = serializer.save()
                if user:
                    data = serializer.data
                    enrich_user.delay(data['id'])
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'not allowed, email not deliverable'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserData(APIView):
    permission_classes = [permissions.IsAuthenticated]  # [IsAdminUser]

    def get(self, request, pk, format='json'):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
