from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from users.models import CustomUser
from books.models import Book, BookReview, Author


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Sitora", first_name="Sitichka98")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username='Sitora', password='somepass')


    def test_book_review_detail(self):
        book = Book.objects.create(title = 'Book1', description = 'description', isbn = '1212131')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')

        res = self.client.get(reverse("api:review-detail", kwargs={"id": br.id}))
    
        self.assertEqual(res.status_code, 200)

        # res.data[] - the way to take datas in DRF
        self.assertEqual(res.data['comment'], br.comment)
        self.assertEqual(res.data['stars_given'], br.stars_given)

        self.assertEqual(res.data['book']['title'], br.book.title)
        self.assertEqual(res.data['book']['isbn'], br.book.isbn)
        self.assertEqual(res.data['book']['description'], br.book.description)

        self.assertEqual(res.data['user']['username'], self.user.username)
        self.assertEqual(res.data['user']['first_name'], self.user.first_name)




    def test_book_review_list(self):
        book = Book.objects.create(title = 'Book1', description = 'description', isbn = '1212131')
        user_1 = CustomUser.objects.create(username='Mirshodbek', first_name='Mirshod')
        user_2 = CustomUser.objects.create(username='Madina', first_name='Madinabonu')
        review_1 = BookReview.objects.create(book=book, user=user_1, stars_given=3, comment='Nice book')
        review_2 = BookReview.objects.create(book=book, user=user_2, stars_given=5, comment='Bad book')

        response = self.client.get(reverse("api:review-list"))

        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['user']['username'], user_1.username)
        self.assertEqual(response.data['results'][1]['user']['username'], user_2.username)
        self.assertEqual(response.data['results'][0]['comment'], review_1.comment)
        self.assertEqual(response.data['results'][1]['comment'], review_2.comment)
        self.assertEqual(len(response.data['results']), 2)





class BookReviewCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Sitora", first_name="Sitichka98")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username='Sitora', password='somepass')


    def test_book_review_delete(self):
        book = Book.objects.create(title='Book1', description='description', isbn='1212131')
        review_1 = BookReview.objects.create(book=book, user=self.user, stars_given=2, comment='Nice book')
        review_2 = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Bad book')


        delete_reponse = self.client.delete(reverse("api:review-detail", kwargs={"id": review_1.id}))
        self.assertEqual(delete_reponse.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=review_1.id).exists())

        req = self.client.get(reverse("api:review-detail", kwargs={"id": review_2.id}))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.data['comment'], review_2.comment)
        self.assertEqual(req.data['stars_given'], review_2.stars_given)
        self.assertEqual(req.data['user']['username'], review_2.user.username)




    def test_book_review_update(self):
        book = Book.objects.create(title='Book1', description='description', isbn='1212131')
        review_1 = BookReview.objects.create(book=book, user=self.user, stars_given=2, comment='First review')

        update_req = self.client.put(
            reverse("api:review-detail",
                    kwargs={"id": review_1.id}),
                    data={"comment":"After updated review", "stars_given":5,
                    'user_id':self.user.id, 'book_id':book.id})

        review_1.refresh_from_db()
        self.assertEqual(review_1.stars_given, 5)
        self.assertEqual(review_1.comment, "After updated review")
        self.assertEqual(update_req.status_code, 200)

        res = self.client.get(reverse("api:review-detail", kwargs={"id": review_1.id}))
        self.assertEqual(res.data['comment'], 'After updated review')
        self.assertEqual(res.data['stars_given'], 5)
        self.assertNotEqual(res.data['comment'], 'First review')
        self.assertNotEqual(res.data['stars_given'], 2)





    def test_book_review_create(self):
        book = Book.objects.create(title='Book1', description='description', isbn='1212131')
        user_1 = CustomUser.objects.create(username='Mirshodbek', first_name='Mirshod')
        review_1 = BookReview.objects.create(book=book, user=self.user, stars_given=2, comment='First review')

        create_req = self.client.post(
            reverse("api:review-list"),
            data = {
            "comment":"second review",
             "stars_given": 5,
             "user_id":user_1.id,
              "book_id":book.id
             })

        self.assertEqual(create_req.status_code, 201)
        res = self.client.get(reverse("api:review-list"))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.data['results'][0]['book']['id'], book.id)
        self.assertEqual(res.data['results'][0]['user']['id'], review_1.user.id)
        self.assertEqual(res.data['results'][0]['comment'], review_1.comment)
        self.assertEqual(res.data['results'][0]['comment'], review_1.comment)
        self.assertEqual(res.data['results'][0]['stars_given'], review_1.stars_given)
        self.assertEqual(res.data['results'][0]['user']['username'], review_1.user.username)

        # check new created comment
        self.assertEqual(res.data['results'][1]['book']['id'], book.id)
        self.assertEqual(res.data['results'][1]['user']['id'], user_1.id)
        self.assertEqual(res.data['results'][1]['comment'], "second review")
        self.assertEqual(res.data['results'][1]['stars_given'], 5)
        self.assertEqual(res.data['results'][1]['user']['username'], user_1.username)




class Users_AuthorsTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Sitora", first_name="Sitichka98")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username='Sitora', password='somepass')


    def test_all_user(self):
        get_users = CustomUser.objects.all()
        self.assertEqual(get_users.count(), 1)
        self.assertIn(self.user, get_users)

        res = self.client.get(reverse("api:users-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['results'][0]['username'], self.user.username)



    def test_all_authors(self):
        auhtor_1 = Author.objects.create(first_name='Mirshod', last_name='Oripov', email='oripovmirshod9@gmail.com', bio='Developer')

        res = self.client.get(reverse("api:authors-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['results'][0]['first_name'], auhtor_1.first_name)
        self.assertEqual(res.data['results'][0]['last_name'], auhtor_1.last_name)
        self.assertEqual(res.data['results'][0]['email'], auhtor_1.email)
        self.assertEqual(res.data['results'][0]['bio'], auhtor_1.bio)