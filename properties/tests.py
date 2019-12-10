from rest_framework import status

from common.test_utils import BaseTestAPI
from documents.models import Document
from properties.models import Property
from users.models import User


class PropertyListAPITest(BaseTestAPI):
    def setUp(self) -> None:
        super().setUp()
        self.local_node = User.objects.create_user('test_local_node', 'localnode@test.com')
        self.property = Property.objects.create(
            country_code='ES',
            city='Jaen',
            risk=20,
            user=self.user,
            local_node=self.local_node,
        )
        self.document = Document.objects.create(
            hash='32413412341234214',
            size=14,
            name='test.txt',
            user=self.user,
            property=self.property,
            content_type='text/plain',
        )

    def test_listing_properties_should_work(self) -> None:
        response = self.client.get('/api/v1/properties/', **self.credentials())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        property_data = response.data[0]
        self.assertEqual(property_data['id'], self.property.pk)
        self.assertEqual(property_data['country_code'], self.property.country_code)
        self.assertEqual(property_data['city'], self.property.city)
        self.assertEqual(property_data['risk'], self.property.risk)
        self.assertEqual(len(property_data['documents']), 1)
        document = property_data['documents'][0]
        self.assertEqual(document['hash'], self.document.hash)
        self.assertEqual(document['size'], self.document.size)
        self.assertEqual(document['content_type'], self.document.content_type)
