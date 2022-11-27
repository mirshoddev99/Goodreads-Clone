from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from books.forms import BookReviewForm
from books.models import Book, BookReview, Bookauthor, Author


# Django generic viewda yozilgan viewlar
# class BooksView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all().order_by('id')
#     context_object_name = "book_list"
#     paginate_by = 2
#


# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     queryset = Book.objects.all()
#     pk_url_kwarg = "id"
#     context_object_name = "book"
#









# Qo'lda yoziladigan viewlar
class BooksView(View):
    def get(self, request):
        book_list = Book.objects.all().order_by('id')
        page_size = request.GET.get('page_size', 2)
        search_query = request.GET.get('q', '')
        if search_query:
            book_list = book_list.filter(title__icontains=search_query)


        # the page is divided into 2
        paginator = Paginator(book_list, page_size)

        # Get default first page
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        contex = {"page_obj":page_obj, "search_query":search_query}
        return render(request, "books/list.html", contex)





class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        book_review_form = BookReviewForm()
        contex = {"book":book, "book_review_form":book_review_form}
        return render(request, "books/detail.html", contex)




class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        book_review_form = BookReviewForm(data=request.POST)

        if book_review_form.is_valid():
            BookReview.objects.create(
                book = book,
                user = request.user,
                stars_given = book_review_form.cleaned_data['stars_given'],
                comment = book_review_form.cleaned_data['comment']
            )

            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "books/detail.html", {"book":book, "book_review_form":book_review_form})






class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        contex = {"book":book, "review":review, "review_form":review_form}

        return render(request, "books/edit_review.html", contex)


    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)
        contex = {"book":book, "review":review, "review_form":review_form}

        if review_form.is_valid():
            review_form.save()
            messages.info(request, "You have successfully edited your comment!")
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "books/edit_review.html", contex)





class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        contex = {"book":book, "review":review}
        return render(request, "books/delete_review.html", contex)




class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        review.delete()
        messages.success(request, "you have successfully deleted your comment")
        return redirect(reverse("books:detail", kwargs={"id": book.id}))







class BookAuthorView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        contex = {"author":author}
        return render(request, 'books/author.html', contex)
























