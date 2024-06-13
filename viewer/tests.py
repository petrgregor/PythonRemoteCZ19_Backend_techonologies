from django.test import TestCase


class ExampleTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up data for all class method.")

    def setUp(self):
        print("\nsetUp: Run once for every test method to setup data.")

    def test_false(self):
        print("Test method: test_false")
        result = False
        self.assertFalse(result)

    def test_add(self):
        print("Test method: test_add")
        result = 1 + 4
        self.assertEqual(result, 5)
