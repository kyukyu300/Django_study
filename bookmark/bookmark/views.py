from django.shortcuts import render

# Create your views here.

from django.http import Http404
from django.shortcuts import render
from bookmark.models import Bookmark

# Create your views here.

def bookmark_list(request):
    bookmarks = Bookmark.objects.all() # SELECT * FROM bookmark
    context = {'bookmarks': bookmarks}
    return render(request, "bookmark_list.html", context)

def bookmark_detail(request, pk):
    try:
        bookmark = Bookmark.objects.get(pk=pk)
    except:
        raise Http404
    context = {'bookmark': bookmark}
    return render(request, "book_info.html", context)