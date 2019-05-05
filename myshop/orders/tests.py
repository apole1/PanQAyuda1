from django.test import TestCase
'''
def create_test():
    c = Category("Prueba1", slugify("Prueba1"));
    c.save()
    p = Product("Producto1",slugify("Producto1"), 300.00, True, models.DateTimeField(auto_now_add=True),
                models.DateTimeField(auto_now=True))
    p.save()


class StatisticsViewTests(TestCase):

    def test_correct(self):
        response = self.client.get(
            "/shop/Prueba1"
        )
        self.assertEqual(response.status_code, 301)

    def test_category(self):
        response2 = self.client.get(
            "/shop/1/Producto1"
        )
        self.assertEqual(response2.status_code, 301)

'''