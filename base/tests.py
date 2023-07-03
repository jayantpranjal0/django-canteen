from django.test import TestCase


class TestUser(TestCase):
    def setUp(self):
        User.objects.create(
            username='testuser',
            email='testuser@test.com',
            full_name='Test User',
            password='testpassword',
        )

    def test_user(self):
        pass

    def test_cart_items(self):
        pass

    def test_update_cart(self):
        pass


def TestOrganization(TestCase):
    def setUp(self):
        Organization.objects.create(
            name='Test Organization',
            description='Test Organization Description',
        )

    def test_get_canteens(self):
        pass


def TestCanteen(TestCase):
    def setUp(self):
        Canteen.objects.create(
            name='Test Canteen',
            description='Test Canteen Description',
        )

    def test_get_meals(self):
        pass

def TestMeal(TestCase):
    def setUp(self):
        Meal.objects.create(
            name='Test Meal',
            description='Test Meal Description',
        )

    def test_get_meals(self):
        pass
