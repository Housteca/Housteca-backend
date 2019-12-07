from rest_framework import status

from common.test_utils import BaseTestAPI
from users.models import User


class UserAPITest(BaseTestAPI):
    def test_create_user_should_work(self) -> None:
        data = {
            'address': self.user.address,
            'email': 'test@test.com',
        }
        authorization = self.credentials()
        User.objects.all().delete()
        response = self.client.post('/api/v1/users/', data=data, format='json', **authorization)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        user = User.objects.get(address=response.data['address'])
        self.assertEqual(user.address, response.data['address'])
        self.assertEqual(user.email, response.data['email'])
