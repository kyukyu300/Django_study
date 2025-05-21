from django.urls import path
from blog.views import generics_views as views

app_name = 'generics_api'

urlpatterns = [
    path('blog', views.BlogListAPIView.as_view(), name='blog_list'),
    path('blog/<int:pk>', views.BlogRetrieveUpdateDestroyAPIView.as_view(), name='blog_detail'),
    path('comment/<int:blog_pk>', views.CommentListCreateAPIView.as_view(), name='comment_list'),
    path('comment/detail/<int:pk>', views.CommentUpdateDestroyAPIView.as_view(), name='comment_update'),

]