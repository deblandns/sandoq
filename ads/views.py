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

# # show list of all ads using the pagination to just show specific ads
# class AdListApiView(APIView , StandardResultsSetPagination):
#     serializer_class = AdSerializer

#     # def get(self,request):
#     #     queryset = Ad.objects.filter(is_public=True)
#     #     result = self.paginate_queryset(queryset , request)
#     #     serializer = AdSerializer(instance=result, many=True)
#     #     return self.get_paginated_response(serializer.data)
#     def get(self, request):
#         """Get List Of Ads Or Search Using the query parameter"""
#         q = request.GET.get('q')  # query param برای search
#         queryset = Ad.objects.filter(is_public=True)
#         if q:
#             queryset = queryset.filter(Q(title__icontains=q) | Q(caption__icontains=q))
#         result = self.paginate_queryset(queryset, request)
#         serializer = AdSerializer(result, many=True)
#         return self.get_paginated_response(serializer.data)
    
#     def post(self, request):
#         """Create Ads"""
#         serializer = AdSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['publisher'] = request.user
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdListApiView(APIView , StandardResultsSetPagination):
    serializer_class = AdSerializer
    parser_classes = (MultiPartParser, )


    def get_permissions(self):
        # If query param 'q' exists, require auth
        if self.request.method == "GET" and self.request.GET.get('q'):
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

# # create advertisement but it need some dependecies like authenticated user
# class AdCreateApiView(APIView):
#     """Create Ads"""
#     serializer_class = AdSerializer
#     parser_classes = (MultiPartParser,)
#     permission_classes = (IsAuthenticated,)
#     # get the published user and then if the data is right will create add for user
#     @extend_schema(request=AdSerializer, responses={201: OpenApiTypes.STR}, methods=['POST'])
#     def post(self,request):
#         serializer = AdSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['publisher'] = request.user
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # show detail of each ad that we input its id
# class AdDetailApiView(APIView):
#     """Return Detail Of Unique Ad"""
#     # serializer_class = AdSerializer
#     serializer_class = AdSerializer
#     permission_classes = (IsAuthenticated, IsPublisherOrReadOnly)
#     parser_classes = (MultiPartParser, )
#     # show the ad using the priamry key of it
#     # @extend_schema(
#     #     parameters=[
#     #         OpenApiParameter(
#     #             name="id",
#     #             type=OpenApiTypes.INT,
#     #             location=OpenApiParameter.PATH, # ensure there is no duplicated id generated from openapi(id)
#     #             description="The ID of the ad you want to see")])
#     # def get(self, request, pk):
#     #     queryset = Ad.objects.get(id=pk)
#     #     serializer = AdSerializer(instance=queryset)
#     #     return Response(serializer.data , status=status.HTTP_200_OK)

#     def get(self, request, pk):
#         ad = Ad.objects.get(id=pk)
#         serializer = AdSerializer(ad)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         ad = Ad.objects.get(id=pk)
#         serializer = AdSerializer(ad, data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['publisher'] = request.user
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, pk):
#         ad = Ad.objects.get(id=pk)
#         ad.delete()
#         return Response(status=204)

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
        ad = Ad.objects.get(id=pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)

    @extend_schema(request=AdSerializer, responses={200: AdSerializer})
    def put(self, request, pk):
        ad = Ad.objects.get(id=pk)
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        ad = Ad.objects.get(id=pk)
        ad.delete()
        return Response(status=204)

# # update the ad by using put operation and must user be authenticated
# class AdUpdateApiView(APIView):
#     """Update Specific Ad"""
#     serializer_class = AdSerializer
#     permission_classes = (IsAuthenticated,IsPublisherOrReadOnly)
#     parser_classes = (MultiPartParser, )
#     @extend_schema(request=AdSerializer, responses={200: AdSerializer}, parameters=[OpenApiParameter(name='id', type=OpenApiTypes.INT, description="The Id Of ad that you want to change the data of it", required=True, location=OpenApiParameter.PATH)])
#     def put(self,request,pk):
#         queryset = Ad.objects.get(id=pk)
#         serializer = AdSerializer(instance=queryset, data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['publisher'] = request.user
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # delete ad 
# class AdDeleteApiView(APIView):
#     """Delete Specific Ad Based On ID"""
#     serializer_class = AdSerializer
#     permission_classes = (IsAuthenticated,IsPublisherOrReadOnly)
#     parser_classes = (MultiPartParser,)

#     @extend_schema(parameters=[OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description="ID of the Ad to delete", required=True)])
#     def delete(self, request, pk):
#         queryset = Ad.objects.get(id=pk)
#         queryset.delete()
#         return Response(status=status.HTTP_200_OK)
    

# # search for ad by Api View 
# class AdSearchApiView(APIView , StandardResultsSetPagination):
#     """Give User List Of Searched Ads Based On Input From Title And Caption"""
#     serializer_class = AdSerializer
#     @extend_schema(
#     parameters=[OpenApiParameter(
#             name="q",
#             type=str,
#             description="Search query parameter Like This: '/api/adssearch/?q=Test'",
#             location=OpenApiParameter.QUERY,
#             required=True,
#             examples=[
#                 OpenApiExample(
#                     name="Search for Test",
#                     value="Test"
#                 ),
#                 OpenApiExample(
#                     name="Search for Laptop",
#                     value="Laptop"
#                 ),
#             ]
#         )
#     ],
#     responses={
#         200: OpenApiResponse(
#             response=AdSerializer,
#             examples=[
#                 OpenApiExample(
#                     name="Example Response",
#                     value={
#                         "id": 0,
#                         "publisher": "string",
#                         "date_added": "2025-08-31T13:35:46.661Z",
#                         "title": "string",
#                         "caption": "string",
#                         "image": "string",
#                         "is_public": True
#                         }
#                     )
#                 ]
#             )
#         }
#     )

#     def get(self,request):
#         q = request.GET.get('q')
#         queryset = Ad.objects.filter(Q(title=q) | Q(caption=q)) # search based on title and caption
#         result = self.paginate_queryset(queryset, request)
#         serializer = AdSerializer(result, many=True)
#         return Response(serializer.data , status=status.HTTP_200_OK)
