from django.urls import path
from blog.views.api_views import BlogListCreateAPIView, BlogDetailAPIView

app_name = 'api'

urlpatterns = [
    path('blog', BlogListCreateAPIView.as_view(), name='blog_list'),
    path('blog/<int:pk>', BlogDetailAPIView.as_view(), name='blog_detail'),
]