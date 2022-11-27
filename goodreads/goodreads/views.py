from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from books.models import BookReview, Book


def landing_page(request):
    if request.user.is_authenticated:
        return render(request, 'landing.html')
    else:
        return render(request, 'default.html')



def home(request):

    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(book_reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    contex = {"page_obj":page_obj}

    return render(request, "home_page.html", contex)