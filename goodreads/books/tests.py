from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author, Bookauthor, BookReview
from users.models import CustomUser


class BookTestCase(TestCase):

    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")



    def test_book_list(self):
        book1 = Book.objects.create(title = "Book1", description = "description1", isbn = "12")
        book2 = Book.objects.create(title = "Book2", description = "description2", isbn = "34")
        book3 = Book.objects.create(title = "Book3", description = "description3", isbn = "45")
        book4 = Book.objects.create(title = "Book4", description = "description4", isbn = "67")

        response = self.client.get(reverse("books:list"))
        books = Book.objects.all()

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse("books:list") + "?page=2")
        self.assertContains(response, book3.title)
        self.assertContains(response, book4.title)



    def test_detail_page(self):
        book1 = Book.objects.create(title = "Steve Jobs", description = "description1", isbn = "12")
        res = self.client.get(reverse("books:detail", kwargs={"id":book1.id}))

        self.assertContains(res, book1.title)
        self.assertContains(res, book1.description)



    def test_search_book(self):
        book1 = Book.objects.create(title = "Steve Jobs", description = "description1", isbn = "12")
        book2 = Book.objects.create(title = "Ilon Mask", description = "description2", isbn = "34")
        book3 = Book.objects.create(title = "Bill gates", description = "description3", isbn = "45")

        response = self.client.get(reverse("books:list") + '?q=steve')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + '?q=ilon')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + '?q=gates')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)



    # @property - This decorator property to provides you to use full_name function which is in your model
    @property
    def test_book_author(self):
        book = Book.objects.create(title = "Steve Jobs", description = "description1", isbn = "12")

        author1 = Author.objects.create(first_name = 'Mirshod', last_name = 'Oripov', email = 'mirshod99@gmail.com', bio = 'Fake author')
        author2 = Author.objects.create(first_name = 'Daler', last_name = 'Oripov', email = 'daler2022@gmail.com', bio = 'test author')

        book_author1 = Bookauthor.objects.create(book = book, author = author1)
        book_author2 = Bookauthor.objects.create(book = book, author = author2)

        res = self.client.get(reverse("books:detail", kwargs={"id":book.id}))

        book_auth = Bookauthor.objects.all()
        check_full_name = book_auth.full_name

        self.assertContains(res, book_author2.check_full_name)
        self.assertContains(res, book_author1.check_full_name)






class BookReviewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username="Sitora", first_name="Sitichka98")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username='Sitora', password='somepass')



    def test_add_review(self):
        book = Book.objects.create(title = 'Book1', description = 'description', isbn = '1212131')
        self.client.login(username = 'Sitora', password = "somepass")
        self.client.post(reverse("books:reviews", kwargs={"id" : book.id}), data={"stars_given" : 3, "comment" : "Nice book"})

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, self.user)




    def test_check_valid_stars_range(self):
        book = Book.objects.create(title = 'Book2', description = 'description1', isbn = '12121311')
        user = CustomUser.objects.create(username = 'Misha', first_name = 'Mirshod', last_name = 'Oripov', email = 'oripovmirshod9@gmail.com')
        user.set_password("somepass")
        user.save()

        self.client.login(username = 'Misha', password = "somepass")
        res = self.client.post(reverse("books:reviews", kwargs={"id" : book.id}), data={"stars_given" : 6, "comment" : "Nice book"})

        book_reviews = book.bookreview_set.all()

        self.assertFormError(res, "book_review_form", "stars_given", "Ensure this value is less than or equal to 5.")
        self.assertEqual(book_reviews.count(), 0)




    def test_update_comment(self):
        book = Book.objects.create(title = 'Book2', description = 'description1', isbn = '12121311')
        review_1 = BookReview.objects.create(user=self.user, book=book, comment="Before update", stars_given=5)

        update_req = self.client.post(reverse("books:edit-review", kwargs={"book_id": book.id, "review_id": review_1.id}), data={
            "comment": "After updating",
            "stars_given": 1
        })

        review_1.refresh_from_db()
        res = self.client.get(reverse("books:detail", kwargs={"id": book.id}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "After updating")
        self.assertContains(res, 1)




    def test_delete_review(self):
        book = Book.objects.create(title = 'Book2', description = 'description1', isbn = '12121311')
        review_1 = BookReview.objects.create(user=self.user, book=book, comment="deleting", stars_given=5)

        delete_req = self.client.get(reverse("books:delete_comment", kwargs={"book_id": book.id, "review_id": review_1.id}))

        all_reviews = BookReview.objects.all()
        self.assertEqual(all_reviews.count(), 0)



class AuthorPageTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username="Sitora", first_name="Sitichka98")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username='Sitora', password='somepass')

    def test_author_page(self):
        book = Book.objects.create(title='Java', description='nice book', isbn='2323232')
        book2 = Book.objects.create(title='Python', description='the great book', isbn='1212131')
        book_obj = Book.objects.count()

        creat_author = Author.objects.create(first_name='Mirshod', last_name='Oripov', email='fakeauthor21@gmail.com', bio='Great person')
        author_obj = Author.objects.count()

        add_book_author = Bookauthor.objects.create(book = book, author = creat_author)
        add_book_author2 = Bookauthor.objects.create(book = book2, author = creat_author)

        self.assertEqual(author_obj, 1)
        self.assertEqual(book_obj, 2)

        response = self.client.get(reverse("books:author", kwargs={"id":creat_author.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(author_obj, 1)
        self.assertEqual(book_obj, 2)

        self.assertContains(response, add_book_author.book.title)
        self.assertContains(response, add_book_author.book.description)
        self.assertContains(response, add_book_author.author.first_name)

        self.assertContains(response, add_book_author2.book.title)
        self.assertContains(response, add_book_author2.book.description)
        self.assertContains(response, add_book_author2.author.first_name)