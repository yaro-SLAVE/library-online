from django.test import Client
import pytest

from rest_framework.test import APIClient

from django.test import TestCase
from library_service.models.order import Order, OrderHistory, OrderItem, Library
from library_service.tests.test_auth import authorize

from library_service.tests.opac_mock import BookId

from django.contrib.auth import get_user_model

User = get_user_model()

class ModelsTest(TestCase):
    def test_order_creation(self):
        user = User.objects.get(pk = 1)
        library = Library.objects.get(pk = 1)
        order = Order.objects.create(user = user, library = library)
        order_item = OrderItem.objects.create(order=order, book_id=BookId.ISTU_AAAA_XXXX.value)
        order_history = OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW)


        self.assertEqual(order.user.email, user.email)
        self.assertEqual(order.library.address, library.address)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_history.order, order)
        self.assertEqual(order_history.status, OrderHistory.Status.NEW)

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_orders(self):
        user = User.objects.get(pk = 1)
        library = Library.objects.get(pk = 1)
        order = Order.objects.create(user = user, library = library)
        order_item = OrderItem.objects.create(order=order, book_id=BookId.ISTU_AAAA_XXXX.value)
        order_history = OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW)

        response = self.client.get('/api/staff/order/?status=new')

        assert response.status_code == 200

    def test_get_order_by_id(self):
        user = User.objects.get(pk = 1)
        library = Library.objects.get(pk = 1)
        order = Order.objects.create(user = user, library = library)
        order_item = OrderItem.objects.create(order=order, book_id=BookId.ISTU_AAAA_XXXX.value)
        order_history = OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW)

        response = self.client.get(f'/api/staff/order/{order.pk}/')

        assert response.status_code == 200

    def test_put_status(self):
        user = User.objects.get(pk = 1)
        library = Library.objects.get(pk = 1)
        order = Order.objects.create(user = user, library = library)
        order_item = OrderItem.objects.create(order=order, book_id=BookId.ISTU_AAAA_XXXX.value)
        order_history = OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW)

        authorize(self.client)

        response = self.client.put(f'/api/staff/order/{order.pk}/', 
            {
                "status": {
                    "status": "processing",
                    "description": "описание"
                },
                "books": []
            },
            content_type="application/json"
        )
        
        assert response.status_code == 200

        
