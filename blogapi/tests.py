from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

# Create your tests here.

class UserTest(APITestCase):

    def setUp(self):
        self.valid_data = {
            "username": "test",
            "password": "secure123",
        }

        self.invalid_data1 = {
            "username": "test", 
            "password": "insecure1", #wrong pass
        }

        self.invalid_data2 = {
            "username": "test2", # Wong username
            "password": "secure123",
        }

        self.signup_url = reverse('signup')
        self.login_url = reverse("login")
        
        response = self.create_user(data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        self.token = response.data.get("token")
         
        return super().setUp()
    
    def create_user(self, data):
        """ Create new user """
        response = self.client.post(path=self.signup_url, data=data, format="json")
        return response

    def login(self, data):
        """ Perform login """
        response = self.client.post(path=self.login_url, data=data, format="json")
        return response
   
    def test_user_registration(self):
        """ Test API registration for existing user """

        response = self.create_user(data=self.valid_data)
        self.assertEqual(response.status_code, 400) # User already exists
        self.token = response.data.get("token")

    def test_user_login(self):
        """ Test user login """

        response = self.login(data=self.valid_data)
        self.assertEqual(response.status_code, 200) # Ok

    def test_invlid_login1(self):
        """ Login with invalid usename """

        response = self.login(data=self.invalid_data1)
        self.assertEqual(response.status_code, 400) # Invalid credentials
    
    def test_invalid_login2(self):
        """ Login with invalid passwors """

        response = self.login(data=self.invalid_data2)
        self.assertEqual(response.status_code, 400) 


class PostTest(APITestCase):
    def setUp(self):
        self.list_url = reverse("post-list")

        data = {
            "username": "test",
            "password": "secure123",
        }
        url = reverse("signup")
        response = self.client.post(path=url, data=data, format="json")
        self.token = response.data.get("token")
        self.headers = {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}
        return super().setUp()
    
    def test_create_unatuhorized(self):

        data = {
            "title": "Test post",
            "subitle": "Sub",
            "section": "tech",
            "content": "Repeating blocks" * 20,
        }

        response = self.client.post(path=self.list_url, data=data, format="json", headers={})
        self.assertEqual(response.status_code, 401) # User must be autenticated to make post
        self.assertEqual(response.data["detail"], "User must be authenticated to create a post.")

    def test_create_authorized(self):

        data = {
            "title": "Test post",
            "subitle": "Sub",
            "section": "tech",
            "content": "Repeating blocks" * 20,
        }

        response = self.client.post(path=self.list_url, data=data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 201) # User is autenticated 
    
    def test_view_authorized(self):
        """ Test post viewing for authorized accounts """

        response = self.client.get(path=self.list_url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_view_unauthorized(self):
        """ Test post viewing for unauthorized accounts """

        response = self.client.get(path=self.list_url)
        self.assertEqual(response.status_code, 200)