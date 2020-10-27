from django.test import TestCase
from django.urls import reverse
from .models import Place

# Create your tests here.


class TestHomePage(TestCase):
    
    def test_load_home_page_shows_empty_list_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        
        # test that no places are found
        self.assertContains(response, 'You have no places in your wishlist')
        

class TestWishList(TestCase):
    
    # known sample data
    fixtures = ['test_places']
    
    def test_view_wishlist_contains_not_visited_places(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        
        # test that unvisited places are listed...
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        
        # ... and not visited places
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')
        

class TestVisitedNotPlacesVisited(TestCase):
    
    def test_no_places_visited(self):
        visited_page_url = reverse('places_visited')
        response = self.client.get(visited_page_url)
        
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        
        # test no visited places are found
        self.assertContains(response, 'You haven\'t visited any places yet')
        
class TestVistedWithPlacesVisited(TestCase):
    
    # known sample data
    fixtures = ['test_places']
    
    def test_with_places_visited(self):
        visited_page_url = reverse('places_visited')
        response = self.client.get(visited_page_url)
        
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        
        # test visited places are listed...
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        
        # ... and not unvisited places
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')
        

class TestAddNewPlace(TestCase):
    
    def test_add_new_unvisited_place_to_wishlist(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}
        
        response = self.client.post(add_place_url, new_place_data, follow=True)
        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        
        # the data that was used to fill in template
        response_places = response.context['places']
        
        # test that the place we just added, and only that, is there
        self.assertEqual(len(response_places), 1)
        # the place we just added
        tokyo_response = response_places[0]
        
        # look for place we just added in database, exception causes test to fail
        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)
        
        # test that place we sent is identical to place in DB
        self.assertEqual(tokyo_from_database, tokyo_response)
        

class TestVisitPlace(TestCase):
    
    # known sample data
    fixtures = ['test_places']
    
    def test_visit_place(self):
        
        # do POST to mark New York (pk 2) as visited
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)
        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        
        # New York shouldn't be in unvisited places
        self.assertNotContains(response, 'New York')
        
        # get New York from db and test that it's visited
        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)
        
    def test_visit_nonexistent_place(self):
        
        visit_place_url = reverse('place_was_visited', args=(200, ))
        response = self.client.post(visit_place_url, follow=True)
        
        # response code should be 404
        self.assertEqual(404, response.status_code)

        
