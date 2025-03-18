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
        
        response = self.client.post(path=self.signup_url, data=self.valid_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.token = response.data.get("token")
         
        return super().setUp()
    
    def login(self, url, data):
        """ Perform login """
        response = self.client.post(path=url, data=data, format="json")
        return response
   
    def test_user_registration(self):
        """ Test API registration for existing user """

        url = reverse('signup')
        
        response = self.client.post(path=url, data=self.valid_data, format="json")
        self.assertEqual(response.status_code, 400) # User already exists
        self.token = response.data.get("token")

    def test_user_login(self):
        """ Test user login """

        response = self.login(self.login_url, self.valid_data)
        self.assertEqual(response.status_code, 200) # Ok

    def test_invlid_login1(self):
        """ Login with invalid usename """

        response = self.login(self.login_url, self.invalid_data1)
        self.assertEqual(response.status_code, 400) # Invalid credentials
    
    def test_invalid_login2(self):
        """ Login with invalid passwors """

        response = self.login(self.login_url, self.invalid_data2)
        self.assertEqual(response.status_code, 400) 