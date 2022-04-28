from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from src.profiles.models import SecureUser, Invite
from src.profiles.serializers import ListSendInviteSerializer, ListReceiveInviteSerializer


class InvitesApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_1 = SecureUser.objects.create_user(password='user_1', username='user_set_1', email='user1@mail.ru')
        self.user_2 = SecureUser.objects.create_user(password='user_1', username='user_set_2', email='user2@mail.ru')
        self.user_3 = SecureUser.objects.create_user(password='user_1', username='user_set_3', email='user3@mail.ru')
        self.user_4 = SecureUser.objects.create_user(password='user_1', username='user_set_4', email='user4@mail.ru')
        self.invite_1 = Invite.objects.create(from_user=self.user_1, to_user=self.user_2)
        self.invite_2 = Invite.objects.create(from_user=self.user_1, to_user=self.user_3)
        self.invite_3 = Invite.objects.create(from_user=self.user_1, to_user=self.user_4)

    def test_create_invite(self):
        url = f'/api/v1/user/invite/send/{self.user_3.pk}/'
        self.client.force_authenticate(self.user_2)
        res = self.client.post(url)
        self.assertEqual({'msg': 'created successfully'}, res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invite.objects.count(), 4)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'error': 'Invite already exists'}, res.data)

    def test_list_sent_invite(self):
        url = reverse('list_invite_send')
        self.client.force_authenticate(self.user_1)
        res = self.client.get(url)
        invites = Invite.objects.filter(from_user=self.user_1)
        serializer_data = ListSendInviteSerializer(invites, many=True).data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, res.data)

    def test_delete_sent_invite(self):
        self.assertNotEqual(Invite.objects.count(), 0)
        inv = Invite.objects.first()
        self.client.force_authenticate(self.user_1)
        url = f'/api/v1/user/invite/send/{inv.pk}/'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invite.objects.count(), 2)

    def test_list_receive_invite(self):
        url = reverse('list_invite_receive')
        self.client.force_authenticate(self.user_2)
        res = self.client.get(url)
        invites = Invite.objects.filter(to_user=self.user_2)
        serializer_data = ListReceiveInviteSerializer(invites, many=True).data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, res.data)

    def test_delete_receive_invite(self):
        self.assertNotEqual(Invite.objects.count(), 0)
        inv = Invite.objects.first()
        self.client.force_authenticate(self.user_2)
        url = f'/api/v1/user/invite/receive/{inv.pk}/'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invite.objects.count(), 2)

    def test_accept_invite(self):
        self.client.force_authenticate(self.user_2)
        url = f'/api/v1/user/invite/receive/accept/{self.invite_1.pk}/'
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual({'msg': 'User added successfully'}, res.data)
        self.assertEqual(Invite.objects.count(), 2)
        self.assertIn(self.user_2, self.user_1.safe_user.all())
        self.assertIn(self.user_1, self.user_2.safe_user.all())
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'error': 'Invite does not exist'}, res.data)
