from django.urls import path, re_path
from . import views

# urlpatterns = [
#     path('list' , views.AdListApiView.as_view() , name='ads'),
#     path('create' , views.AdCreateApiView.as_view() , name='ad-create'),
#     path('Deatil/<int:pk>' , views.AdDetailApiView.as_view() , name='ad-Deatil'),
#     path('Update/<int:pk>' , views.AdUpdateApiView.as_view() , name='ad-update'),
#     path('Delete/<int:pk>' , views.AdDeleteApiView.as_view() , name='ad-delete'),
#     path('search' , views.AdSearchApiView.as_view() , name='ad-search'),
# ]

urlpatterns = [
    path('', views.AdListApiView.as_view(), name='ads-list'), # GET -> list, POST -> create
    path('<int:pk>/', views.AdDetailApiView.as_view(), name='ads-detail'),  # GET -> detail, PUT -> update, DELETE -> delete
]