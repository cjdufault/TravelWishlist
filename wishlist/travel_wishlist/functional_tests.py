from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super.setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super.tearDownClass()
        
    def test_title_on_home_page(self):
        
        self.selenium.get(self.live_server_url)
        
        # test that the correct title is in the page
        self.assertIn('Travel Wishlist', self.selenium.title)
        

class AddPlacesTest(LiveServerTestCase):
    
    fixtures = ['test_places']
    
    @classmethod
    def setUpClass(cls):
        super.setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super.tearDownClass()
        
    def test_add_new_place(self):
        
        self.selenium.get(self.live_server_url)
        
        # put Denver in the text box
        input_name = self.selenium.find_element_by_id('id_name')
        input_name.send_keys('Denver')
        
        # push the add button
        add_button = self.selenium.find_element_by_id('add-new-place')
        add_button.click()
        
        # check that Denver has been added
        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', denver.text)
        
        # test that the right cities are on the page
        self.assertIn('Denver', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)
