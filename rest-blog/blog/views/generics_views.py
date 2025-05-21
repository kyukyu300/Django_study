from django.utils import timezone

from django.db.models import Q
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from utils.permissions import IsAuthorOrReadOnly
from blog.models import Blog, Comment
from blog.serializers import BlogSerializer, CommentSerializer

class BlogQuerySetMixin:
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            Q(published_at__isnull=True) |
            Q(published_at__lte=timezone.now())
        ).order_by('-created_at').select_related('author')


class BlogListAPIView(BlogQuerySetMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogRetrieveUpdateDestroyAPIView(BlogQuerySetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        blog = self.get_blog_object()
        serializer.save(author=self.request.user, blog=blog)

    def get_queryset(self):
        queryset = super().get.queryset()
        blog = self.get_blog_object()
        return queryset.filter(blog=blog)

    def get_blog_object(self):
        blog = Blog.objects.get(pk=self.kwargs['blog_pk'])

class CommentUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
