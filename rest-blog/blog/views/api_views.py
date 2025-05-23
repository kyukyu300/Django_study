from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer


class BlogListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        blog_list = Blog.objects.all().order_by('-created_at').select_related('author')
        paginator = PageNumberPagination()
        queryset = paginator.paginate_queryset(blog_list, request)

        serializer = BlogSerializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(APIView):
    object = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        blog.delete()

        return Response({
            'deleted': True,
            'pk': kwargs.get('pk', 0),
        }, status=status.HTTP_200_OK)

    def get_object(self, request, *args, **kwargs):
        if self.object:
            return self.object

        blog_list = Blog.objects.all().select_related('author')
        pk = kwargs.get('pk', 0)

        blog = get_object_or_404(blog_list, pk=pk)
        self.object = Blog
        return blog
