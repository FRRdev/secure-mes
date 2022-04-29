from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from src.profiles.models import SecureUser
from src.mes_app.models import CurrentKey, Key, Message
from src.mes_app.serializers import GetMessageSendSerializer, GetMessageReceiveSerializer


class MessageApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_1 = SecureUser.objects.create_user(password='user_1', username='user_set_1', email='user1@mail.ru')
        self.user_2 = SecureUser.objects.create_user(password='user_1', username='user_set_2', email='user2@mail.ru')
        self.user_3 = SecureUser.objects.create_user(password='user_1', username='user_set_3', email='user3@mail.ru')
        self.key = Key.objects.create(value='jksdnvjosfnvsfjv')
        self.ck = CurrentKey.objects.create(first_user=self.user_1, second_user=self.user_2, key=self.key)
        self.mes = Message.objects.create(sender=self.user_1, recipient=self.user_2, content=b'dqwdqed', key=self.key)

    def test_send_message(self):
        self.client.force_authenticate(self.user_1)
        url = f'/api/v1/message/{self.user_2.pk}/'
        test_data = {
            'text': 'Hello World!'
        }
        res = self.client.post(path=url, data=test_data)
        mes = Message.objects.last()
        serializer_data = GetMessageSendSerializer(instance=mes).data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, res.data)
        url_error = f'/api/v1/message/{self.user_3.pk}/'
        res_error = self.client.post(path=url_error, data=test_data)
        self.assertEqual(res_error.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_message(self):
        self.client.force_authenticate(self.user_1)
        url = f'/api/v1/message/{self.user_2.pk}/'
        test_data = {
            'text': 'Hello World!'
        }
        self.client.post(path=url, data=test_data)
        self.client.force_authenticate(self.user_2)
        mes = Message.objects.last()
        url = f'/api/v1/message/read/{mes.pk}/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, res.data)
        self.client.force_authenticate(self.user_3)
        url = f'/api/v1/message/read/{mes.pk}/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_message(self):
        self.client.force_authenticate(self.user_2)
        url = f'/api/v1/message/update/{self.mes.pk}/'
        res = self.client.patch(url)
        mes = Message.objects.get(pk=self.mes.pk)
        self.assertFalse(mes.is_active)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_sent_message(self):
        self.client.force_authenticate(self.user_1)
        url = reverse('list_send_message')
        res = self.client.get(url)
        mes = Message.objects.filter(sender=self.user_1)
        serializer_data = GetMessageSendSerializer(instance=mes, many=True).data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer_data)

    def test_received_message(self):
        self.client.force_authenticate(self.user_2)
        url = reverse('list_receive_message')
        res = self.client.get(url)
        mes = Message.objects.filter(recipient=self.user_2)
        serializer_data = GetMessageReceiveSerializer(instance=mes, many=True).data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer_data)
