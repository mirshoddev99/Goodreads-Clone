from django.contrib.auth import get_user
from django.test import TestCase
from django.shortcuts import reverse
from users.models import CustomUser


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"Sitora",
                "first_name":"Sitora",
                "last_name":"Davlatovna",
                "email":"admin421@gmail.com",
                "password":"somepassword"
            }
        )


        user = CustomUser.objects.get(username="Sitora")

        self.assertEqual(user.first_name, "Sitora")
        self.assertEqual(user.last_name, "Davlatovna")
        self.assertEqual(user.email, "admin421@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))



    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name":"Sitora",
                "email":"admin421@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")



    def test_invalid_email(self):
        response = self.client.post(
            # template manzil
            reverse("users:register"),
            # post qilmoqchi bolgan qiymat
            data={
                "username":"Sitora",
                "first_name":"Sitora",
                "last_name":"Davlatovna",
                "email":"invalid-email",
                "password":"somepassword"
            }
        )

        user_email = CustomUser.objects.count()
        self.assertEqual(user_email, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")



    def test_unique_username(self):
        # 1. Create a user using django ORM
        user = CustomUser.objects.create(username="Sitora", first_name="Sitora")
        user.set_password("somepass")
        user.save()

        # 2. Try to create another user with that same username
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Sitora",
                "first_name": "Sitora",
                "password": "somepass"
            }
        )

        # 3. Check that second user was not created
        unique_username = CustomUser.objects.count()
        self.assertEqual(unique_username, 1)

        # 4. Check that form contains error message
        self.assertFormError(response, "form", "username", "A user with that username already exists.")




class LoginTestCase(TestCase):

    # user birinchi yaratiladi va pastda foydalaniladi.
    def setUp(self):
        self.user = CustomUser.objects.create(username="Sitora", first_name="Sitichka98")
        self.user.set_password("somepass")
        self.user.save()


    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
            "username":"Sitora",
            "password":"somepass"
            })

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)



    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepass"
            })

        # getting username through using self.client method
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Sitora",
                "password": "wrong-password"
            })

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_logout(self):
        login = self.client.login(username = "Sitora", password = "somepass")
        logout = self.client.get(reverse("users:logout"))
        gt_user = get_user(self.client)
        self.assertTrue(login)
        self.assertFalse(gt_user.is_authenticated)



    def test_check_form_error(self):
        response = self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepass"
            })

        # getting username through using self.client method
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertFormError(response, "form", "username", [])





class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        # Check that user redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")


    def test_profile_details(self):
        user = CustomUser.objects.create(username = "Mirshod", first_name = "Mirshodbek", last_name="Oripov", email="oripovmirshod9@gmail.com")
        user.set_password('somepass')
        user.save()

        # self.client.login(2 parameter) - it is used when you want to log in app
        self.client.login(username = 'Mirshod', password = 'somepass')
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)



    def test_profile_update(self):
        create_user = CustomUser.objects.create(username = "Mirshod", first_name = "Mirshodbek", last_name="Oripov", email="oripovmirshod9@gmail.com")
        create_user.set_password('somepass')
        create_user.save()

        self.client.login(username = "Mirshod", password = "somepass")
        response = self.client.post(reverse("users:profile_edit"), data={
            "username":"Mirshod",
            "first_name":"Mirshodbek",
            "last_name":"Umarov",
            "email":"oripovmirshod99@gmail.com"
        })

        #1. The way to take a user from updated db
        user = CustomUser.objects.get(pk=create_user.pk)

        # 2. The way to take a user from updated db
        # user.refresh_from_db()

        self.assertEqual(user.last_name, "Umarov")
        self.assertEqual(user.email, "oripovmirshod99@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))

