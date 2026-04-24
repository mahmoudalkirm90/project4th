from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .serializers import ( UserLoginSerializer,
                           ResendOtpSerializer,
                           VerifyOtpSerializer,
                           DeleteAccountSerializer,
                           PasswordResetSerializer,
                           EmailResetSerializer)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):   
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=200)

class ResendOtpView(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=200)

class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        refresh = RefreshToken.for_user(self.request.user)
        return Response(result, status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)   
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):

    permission_classes = [IsAuthenticated] 
    # allowed_methods = ['DELETE',"POST"]
    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)

class PasswordResetView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer

    def get_object(self):
        return self.request.user
    def update(self,request):
        serializer = self.get_serializer(self.get_object(),data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Password reseted successfully",
        },status=status.HTTP_200_OK)

class EmailResetView(generics.UpdateAPIView):
    queryset = User.objects.all()   
    permission_classes = [IsAuthenticated]
    serializer_class = EmailResetSerializer
    def update(self,request):
        serializer = self.get_serializer(self.get_object(),data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Email reseted successfully, please verify your new email",
         },status=status.HTTP_200_OK) 
    
    def get_object(self):
        return self.request.user