from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import UserSerializers

class UserView(APIView):
    serializer_class = UserSerializers

    def get(self, request):
        user = request.user
        serializer = UserSerializers(instance=user)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def put(self , request):
        user = request.user
        serializer = UserSerializers(data=request.data , instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)