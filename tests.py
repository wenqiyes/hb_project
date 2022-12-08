"""Tests for Apartment Finder's Flask app."""

import unittest
import model
import server


class serverTests(unittest.TestCase):
    """Tests for aprtment finder site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        model.connect_to_db(server.app,'favorites')

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)

    def test_all_listings_no_zipcode(self):
        """Can we reach the listings page without any input?"""

        result = self.client.get("/listings",
                                follow_redirects=True)
        self.assertIn(b"valid input", result.data)

    def test_all_listings_withn_zipcode(self):
        """Can we reach the listings page with zipcode?"""

        result = self.client.get("/listings?zipcode=55414")
        self.assertIn(b"Search Results", result.data)
        self.assertIn(b"Minneapolis", result.data)

    def test_logout(self):
        result = self.client.get('/logout', follow_redirects = True)
        self.assertIn(b"Login", result.data)

    def test_login(self):
        pass

   

if __name__ == "__main__":
    unittest.main()
