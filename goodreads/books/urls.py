from django.urls import path
from books.views import BooksView, BookDetailView, AddReviewView, EditReviewView, DeleteReviewView, DeleteCommentView, BookAuthorView


app_name = "books"

urlpatterns = [

    path("", BooksView.as_view(), name='list'),
    path("<int:id>/", BookDetailView.as_view(), name='detail'),
    path("<int:id>/reviews/", AddReviewView.as_view(), name="reviews"),
    path("<int:book_id>/reviews/<int:review_id>/edit/", EditReviewView.as_view(), name="edit-review"),
    path("<int:book_id>/reviews/<int:review_id>/delete_review/", DeleteReviewView.as_view(), name="delete_review"),
    path("<int:book_id>/reviews/<int:review_id>/delete/", DeleteCommentView.as_view(), name="delete_comment"),
    path("<int:id>/author", BookAuthorView.as_view(), name='author'),

]