from rest_framework.test import APITestCase
from rest_framework import status

from src.profiles.models import SecureUser
from src.profiles.serializers import GetPublicSecureUserSerializer


class ProfilesCRUDApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_1 = SecureUser.objects.create_user(password='user_1', username='user_set_1', email='user1@mail.ru')
        self.user_2 = SecureUser.objects.create_user(password='user_1', username='user_set_2', email='user2@mail.ru')
        self.user_3 = SecureUser.objects.create_user(password='user_1', username='user_set_3', email='user3@mail.ru')

    def test_create_user(self):
        url = '/api/v1/user/secureuser/'
        for i in range(5):
            user_data = {
                "password": f"user_{i}",
                "username": f"user_{i}",
                "first_name": f"user_{i}",
                "last_name": "string",
                "email": f"user_{i}@example.com",
            }
            res = self.client.post(url, data=user_data)
            self.assertEqual(res.status_code, 201)
        self.assertEqual(8, SecureUser.objects.count())

    def test_list_user(self):
        url = '/api/v1/user/secureuser/'
        users = SecureUser.objects.all()
        self.client.force_authenticate(self.user_1)
        res = self.client.get(url)
        serializer_data = GetPublicSecureUserSerializer(users, many=True).data
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(serializer_data, res.data)

    def test_update_user(self):
        url = f'/api/v1/user/secureuser/{self.user_1.id}/'
        self.client.force_authenticate(self.user_1)
        user_data = {
            "password": "user_1",
            "username": "user_1_changed",
            "first_name": "user_1_changed",
            "last_name": "string",
            "email": "user_1@example.com",
            "phone": "string",
            "date_of_birth": "2022-04-28",
            "gender": "male",
            "city": "string",
            "bio": "string"
        }
        res = self.client.put(url, data=user_data)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(res.data['username'], 'user_1_changed')
        self.assertEqual(res.data['first_name'], 'user_1_changed')

    def test_no_auth_user(self):
        url = f'/api/v1/user/secureuser/{self.user_1.id}/'
        user_data = {
            "password": "user_1",
            "username": "user_1_changed_error",
            "first_name": "user_1_changed_error",
            "last_name": "string",
        }
        res = self.client.put(url, data=user_data)
        self.assertEqual(res.status_code, 401)

    def test_delete_user(self):
        url = f'/api/v1/user/secureuser/{self.user_1.id}/'
        self.client.force_authenticate(self.user_1)
        self.assertEqual(3, SecureUser.objects.count())
        res = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        self.assertEqual(2, SecureUser.objects.count())
