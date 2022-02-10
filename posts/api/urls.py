from django.urls import path
from .views import PostList, PostDetail, post_like, post_unlike


urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/like/', post_like, name='post_like'),
    path('<int:pk>/unlike/', post_unlike, name='post_unlike'),
]