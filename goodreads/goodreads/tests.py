from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title = 'Book2', description = 'description1', isbn = '12121311')
        user = CustomUser.objects.create(username = 'Misha', first_name = 'Mirshod', last_name = 'Oripov', email = 'oripovmirshod9@gmail.com')
        user.set_password("somepass")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Nice book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Useful book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Great book")

        res = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(res, review2.comment)
        self.assertContains(res, review1.comment)
        self.assertNotContains(res, review3.comment)

