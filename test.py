from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()  # Create a test client
        app.config['TESTING'] = True  # Enable testing mode
        self.boggle_game = Boggle()
        with self.client.session_transaction() as session:
            session['board'] = self.boggle_game.make_board()

    def test_index(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<table', response.data)
            self.assertIn(b'<form', response.data)

    def test_check_word_valid(self):
        with self.client:
            response = self.client.post('/check_word', json={'word': 'CAT'})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['result'], 'ok')
            self.assertIn('score', data)

    def test_check_word_invalid(self):
        with self.client:
            response = self.client.post(
                '/check_word', json={'word': 'INVALIDWORD'})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['result'], 'not-on-board')

    def test_update_stats(self):
        with self.client:
            response = self.client.post('/update_stats', json={'score': 10})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['result'], 'ok')
            self.assertIn('total_plays', data)
            self.assertIn('highest_score', data)


if __name__ == '__main__':
    unittest.main()
