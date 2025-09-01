from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Ad
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AdSerializer
from .pagination import StandardResultsSetPagination
from rest_framework.parsers import MultiPartParser
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .permissions import IsPublisherOrReadOnly

# list the ads and create ads with search and without the search 
class AdListApiView(APIView , StandardResultsSetPagination):
    serializer_class = AdSerializer
    parser_classes = (MultiPartParser, )


    def get_permissions(self):
        # If query param 'q' exists, require auth
        if self.request.method == "GET" and self.request.GET.get('q'):
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                description="Search ads by title or caption",
                location=OpenApiParameter.QUERY,
                required=False,
                examples=[
                    OpenApiExample(name="Search Test", value="Test"),
                    OpenApiExample(name="Search Laptop", value="Laptop")
                ]
            )
        ],
        responses={
            200: OpenApiResponse(
                response=AdSerializer(many=True),
                examples=[
                    OpenApiExample(
                        name="Example List Response",
                        value=[{
                            "id": 1,
                            "publisher": "user1",
                            "date_added": "2025-08-31T13:35:46.661Z",
                            "title": "Test Ad",
                            "caption": "This is a test",
                            "image": "image_url",
                            "is_public": True
                        }]
                    )
                ]
            )
        }
    )
    def get(self, request):
        """Get List Of Ads Or Search Using the query parameter"""
        q = request.GET.get('q')  # query param
        queryset = Ad.objects.filter(is_public=True)
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(caption__icontains=q))
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=AdSerializer,
                description="Created ad successfully",
                examples=[
                    OpenApiExample(
                        name="Example Created Response",
                        value={
                            "id": 2,
                            "publisher": "user2",
                            "date_added": "2025-08-31T14:00:00.000Z",
                            "title": "New Ad",
                            "caption": "New ad caption",
                            "image": "image_url",
                            "is_public": True
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Validation error")
        }
    )
    def post(self, request):
        """Create Ads"""
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get detail, update, delete ad
class AdDetailApiView(APIView):
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsPublisherOrReadOnly)
    parser_classes = (MultiPartParser, )

    @extend_schema(
        parameters=[OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="ID of the ad",
            required=True
        )],
        responses={
            200: OpenApiResponse(
                response=AdSerializer,
                examples=[
                    OpenApiExample(
                        name="Example Detail Response",
                        value={
                            "id": 1,
                            "publisher": "user1",
                            "date_added": "2025-08-31T13:35:46.661Z",
                            "title": "Test Ad",
                            "caption": "This is a test",
                            "image": "image_url",
                            "is_public": True
                        }
                    )
                ]
            ),
            204: OpenApiResponse(description="Deleted successfully")
        }
    )
    def get(self, request, pk):
        """get the ad detail"""
        ad = Ad.objects.get(id=pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)

    @extend_schema(request=AdSerializer, responses={200: AdSerializer})
    def put(self, request, pk):
        """update the ad details"""
        ad = Ad.objects.get(id=pk)
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """delete the advertisement with ad id"""
        ad = Ad.objects.get(id=pk)
        ad.delete()
        return Response(status=204)