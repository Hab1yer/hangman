import unittest
from unittest.mock import patch
from game import HangmanGame
from server import app

class Tests(unittest.TestCase):
    def test_engine(self):
        g=HangmanGame('apple'); self.assertNotIn('word',g.state())
        for c in 'aple': g.guess(c)
        self.assertEqual(g.state()['status'],'won')
        with self.assertRaises(RuntimeError): g.guess('z')
        g=HangmanGame('apple')
        for c in 'bcdfgh': g.guess(c)
        self.assertEqual(g.state()['status'],'lost')
        self.assertEqual(g.state()['word'],'apple')
    def test_validation(self):
        g=HangmanGame('apple')
        for value in ['',None,1,'ab','é']:
            with self.assertRaises(ValueError): g.guess(value)
        g.guess('A')
        with self.assertRaises(RuntimeError): g.guess('a')
        self.assertEqual(g.state()['remaining_guesses'],6)
    def test_api(self):
        c=app.test_client()
        for difficulty in ['easy','medium','hard']:
            r=c.post('/api/games',json={'difficulty':difficulty});self.assertEqual(r.status_code,201)
            s=r.get_json();self.assertNotIn('word',s)
            url='/api/games/'+s['game_id']
            self.assertEqual(c.get(url).status_code,200)
            self.assertEqual(c.post(url+'/guess',json={'letter':'a'}).status_code,200)
            self.assertEqual(c.post(url+'/guess',json={'letter':'a'}).status_code,409)
            self.assertEqual(c.post(url+'/guess',json={'letter':'ab'}).status_code,400)
        self.assertEqual(c.post('/api/games',json={'difficulty':[]}).status_code,400)
        self.assertEqual(c.post('/api/games',json=[]).status_code,400)
        self.assertEqual(c.get('/api/games/missing').status_code,404)
        with c.get('/') as response:
            self.assertEqual(response.status_code,200)

    def test_complete_games_and_restart(self):
        c = app.test_client()
        for letters, outcome in [('aple', 'won'), ('bcdfgh', 'lost')]:
            with patch('server.choice', return_value='apple'):
                initial = c.post('/api/games', json={'difficulty': 'easy'}).get_json()
            url = '/api/games/' + initial['game_id']
            for letter in letters:
                response = c.post(url + '/guess', json={'letter': letter})
                self.assertEqual(response.status_code, 200)
                state = response.get_json()
                if state['status'] == 'playing': self.assertNotIn('word', state)
            self.assertEqual(state['status'], outcome)
            self.assertEqual(state['word'], 'apple')
            self.assertEqual(c.post(url + '/guess', json={'letter': 'z'}).status_code, 409)
            fresh = c.post('/api/games', json={'difficulty': 'hard'}).get_json()
            self.assertNotEqual(fresh['game_id'], initial['game_id'])
            self.assertEqual(fresh['remaining_guesses'], 6)
            self.assertEqual(c.get(url).get_json()['status'], outcome)

    def test_bad_requests(self):
        c = app.test_client()
        for payload in [[], {}, {'difficulty': None}, {'difficulty': '../game'}, {'difficulty': 'easy', 'word': 'cheat'}]:
            self.assertEqual(c.post('/api/games', json=payload).status_code, 400)
        response = c.post('/api/games', data='{', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(c.post('/api/games', data='text').status_code, 415)

if __name__=='__main__': unittest.main()
