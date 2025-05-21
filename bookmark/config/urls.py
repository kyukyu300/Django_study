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

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, Http404
from django.shortcuts import render
from bookmark import views

game_list = [
    {"title": "리그 오브 레전드", "genre": "aos"},
    {"title": "오버워치", "genre": "fps"},
    {"title": "발로란트", "genre": "fps"},
    {"title": "메이플스토리", "genre": "rpg"},
]

def index(request):
    return HttpResponse("Hello, world!")

def book_list(request):
    # book_text = ""
    # for i in range(0,10):
    #     book_text += f'book {i}<br>'

    return render(request, 'book_list.html', {'range': range(0,10)})

def book(request, num):
    return render(request, 'book_detail.html', {'num': num})

def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다.')

def games(request):
    # games_title = [game['title'] for game in game_list]
    # response_text = ""
    # for index, game in enumerate(games_title):
    #     response_text += f'<a href = "/games/{index}/">{game}<a><br>'
    # return HttpResponse(response_text)
    return render(request, 'games.html', {'game_list': game_list})

def game_detail(request, index):
    if index >= len(game_list) - 1:
        raise Http404
    game = game_list[index]
    response_text = f'<h1>이름: {game["title"]}</h1> <p>장르: {game["genre"]}</p>'
    return render(request, 'game_detail.html', {'game': game})

def gugu(request, num):
    context = {
        'num': num,
        "results": [num * i for i in range(1, 10)]
    }

    return render(request, 'gugu.html', context)
urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", index),
    # path("book_list/", book_list),
    # path("book_list/<int:num>/", book),
    # path("language/<str:lang>", language),
    # path("games/", games),
    # path("games/<int:index>/", game_detail),
    # path("gugu/<int:num>/", gugu),
    path("book/", views.bookmark_list),
    path("book/<int:pk>/", views.bookmark_detail),
]
