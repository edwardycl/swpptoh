from django.test import TestCase, Client
from .models import Hero
from django.forms.models import model_to_dict
import json

class HeroTestCase(TestCase):
    def setUp(self):
        Hero.objects.create( name='Superman' )
        Hero.objects.create( name='Batman')
        Hero.objects.create( name='Joker')

        self.client = Client()

    def test_hero_str(self):
        batman = Hero.objects.get(name='Batman')
        self.assertEqual(str(batman), 'Batman')

    def test_hero_list_get(self):
        response = self.client.get('/api/hero')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)

    def test_hero_list_post(self):
        new_hero = {'name': 'SWPP'}
        response = self.client.post('/api/hero', json.dumps(new_hero), content_type='application/json')
        get_response = self.client.get('/api/hero/4')
        new_data = json.loads(get_response.content.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_data['name'], 'SWPP')

    def test_hero_list_delete(self):
        response = self.client.delete('/api/hero')
        self.assertEqual(response.status_code, 405)

    def test_hero_detail_get(self):
        # Test heroDetail with GET request
        response = self.client.get('/api/hero/1')
        data = json.loads(response.content.decode()) # Deserialize response data
        self.assertEqual(data['name'], 'Superman') # Verify the data
        self.assertEqual(response.status_code, 200) # Check the response code

    def test_hero_detail_get_fail(self):
        response = self.client.get('/api/hero/4')
        self.assertEqual(response.status_code, 404) # Check the response code

    def test_hero_detail_put(self):
        new_hero = {'name': 'SWPP'}
        response = self.client.put('/api/hero/3', json.dumps(new_hero), content_type='application/json')
        get_response = self.client.get('/api/hero/3')
        new_data = json.loads(get_response.content.decode())
        self.assertEqual(response.status_code, 204)

    def test_hero_detail_put_fail(self):
        new_hero = {'name': 'SWPP'}
        response = self.client.put('/api/hero/4', json.dumps(new_hero), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_delete(self):
        response = self.client.delete('/api/hero/2')
        get_response = self.client.get('/api/hero/2')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(get_response.status_code, 404)

    def test_hero_detail_delete_fail(self):
        response = self.client.delete('/api/hero/4')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_head(self):
        response = self.client.head('/api/hero/1')
        self.assertEqual(response.status_code, 405)
