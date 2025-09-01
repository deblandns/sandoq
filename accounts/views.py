from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializers
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiRequest, OpenApiResponse


# get the user from the users database
class UserView(APIView):
    serializer_class = UserSerializers
    def get(self, request):
        """get the user based on the requesting user to show the name of user"""
        user = request.user
        serializer = UserSerializers(instance=user)
        return Response(serializer.data , status=status.HTTP_200_OK)

    # to change the user name inside the users table 
    def put(self , request):
        """change the name of user from users table"""
        user = request.user
        serializer = UserSerializers(data=request.data , instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)