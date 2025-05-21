"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog_project/', include('blog_project.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views import View

from blog import views,cb_views
from member import views as member_views
from django.views.generic import RedirectView,TemplateView

# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# class TestView(TemplateView):
#     def get(self, request):
#         pass


urlpatterns = [
    path("admin/", admin.site.urls),

    # FBV
    # path("blog/", views.blog_list, name="blog"),
    # path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    # path('create/', views.blog_create, name='blog_create'),
    # path('update/<int:pk>/', views.blog_update, name='blog_update'),
    # path('delete/<int:pk>/', views.blog_delete, name='blog_delete'),

    path('',include('blog.urls')),

    #auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.signup, name='signup'),
    path('login/', member_views.login, name='login'),
#     path('about/', AboutView.as_view(), name='about'),
#     path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    path('summernote/', include('django_summernote.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)