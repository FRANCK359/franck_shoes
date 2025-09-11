from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product

class ShoesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Chaussures de Sport',
            slug='chaussures-sport'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=99.99,
            category=self.category,
            available_sizes=['38', '39', '40'],
            stock=10
        )

    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_product_list(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        self.assertContains(response, self.product.name)

    def test_product_detail(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, self.product.name)

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_to_cart', args=[self.product.slug]), {
            'size': '39',
            'quantity': 1
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after adding to cart

    def test_search_functionality(self):
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)