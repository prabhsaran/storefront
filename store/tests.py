from django.test import TestCase
from django.urls import reverse

from store.constants import PRODUCT_SEARCH_VIEW_NAME
from store.models import Product, Category, Tag


class ProductSearchTestCase(TestCase):
    """
    Test case for the product search functionality.

    This test case includes the following tests:
    - `test_search_by_description`: Tests searching for products by their description.
    - `test_search_by_tags`: Tests searching for products by their associated tags.
    - `test_search_by_category`: Tests searching for products by their category.
    - `test_search_and_filter`: Tests searching for products by description and filtering by tags.

    The `setUp` method initializes the test data, including creating categories, tags, and products.
    """

    def setUp(self):
        self.url = reverse(
            PRODUCT_SEARCH_VIEW_NAME
        )  # Use reverse to dynamically generate the URL

        # Create test categories and tags
        self.category = Category.objects.create(
            title="Electronics", description="Electronic items"
        )
        self.tag1 = Tag.objects.create(label="Eco-Friendly")
        self.tag2 = Tag.objects.create(label="Best Seller")

        # Create test products
        self.product1 = Product.objects.create(
            title="Wireless Earbuds",
            slug="wireless-earbuds",
            description="High quality wireless earbuds with noise cancellation",
            unit_price=99.99,
            inventory=10,
            category=self.category,
        )
        self.product1.tags.add(self.tag1, self.tag2)

        self.product2 = Product.objects.create(
            title="Bluetooth Speaker",
            slug="bluetooth-speaker",
            description="Portable Bluetooth speaker with deep bass",
            unit_price=49.99,
            inventory=15,
            category=self.category,
        )
        self.product2.tags.add(self.tag1)

    def test_search_by_description(self):
        response = self.client.get(self.url, {'search': 'wireless'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Earbuds")
        self.assertNotContains(response, "Bluetooth Speaker")

    def test_search_by_tags(self):
        response = self.client.get(self.url, {'tags': [self.tag1.id, self.tag2.id]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Earbuds")
        self.assertNotContains(response, "Bluetooth Speaker")

    def test_search_by_category(self):
        response = self.client.get(self.url, {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Earbuds")
        self.assertContains(response, "Bluetooth Speaker")

    def test_search_and_filter(self):
        response = self.client.get(
            self.url, {'search': 'wireless', 'tags': [self.tag1.id]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Earbuds")
        self.assertNotContains(response, "Bluetooth Speaker")
