from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, parsers
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.api.v1.serializers import RegisterSerializer, LoginSerializer


class RegisterAPIView(APIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request) -> Response:
        """
        Handle user registration.

        Args:
            request: The HTTP request containing user registration data.

        Returns:
            Response: JWT tokens if registration is successful, or validation errors.
        """
        serializer: RegisterSerializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh: RefreshToken = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request) -> Response:
        """
        Handle user login.

        Args:
            request: The HTTP request containing user login data.

        Returns:
            Response: JWT tokens if login is successful, or error details.
        """
        serializer: LoginSerializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email: str = serializer.validated_data['email']
            password: str = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)

            if user:
                refresh: RefreshToken = RefreshToken.for_user(user)

                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)

            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
