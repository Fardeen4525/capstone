import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# AUTH_EXECUTIVEP=os.environ.get('AUTH_EXECUTIVEP')
# AUTH_CASTINGD=os.environ.get('AUTH_CASTINGD')
# AUTH_CASTINGA=os.environ.get('AUTH_CASTINGA')

AUTH_EXECUTIVEP='''Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBwbnB2ZUFSU3hWRVdLM092WUlVSCJ9.eyJpc3MiOiJodHRwczovL2ZhZGRvLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYWJmN2VlNTZjNDBjNmQ4NGU2ZjYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTkwMzg5OTA1LCJleHAiOjE1OTA0NzYzMDQsImF6cCI6IklYR0NNb1VVWUY1QTUxczJFV0NYQW5BZ2dvbDBUYXlvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.3i6spkt95c8p3DaAsgP8YsVsyl5mf-VKZuO3Hze0cpvSD3LjRXsnHSyXnFLFZYHKpZfSuMZpeyaZGYkbbYJL8jlQ9QjKJMih-o01G-Q6uX11FoUit6KQPt9HM6au-ZCvr2wEvQ3Okx6KOGf0Rdvs6fBsfnn-R7y0yS9bZGjcMRnBFVLC03EmELJNIKMa6tWgOE_Dcty78x6P3KnV8Gp4SSJ6IN9_doF8yp171ug_ja4uL2yQrvP47LRRKvL0WVS68oUx91QSNGtvAY6N7xaILjW4fdYNWfJa1Xen9GRrYe-oZv7BmleF050b50eOzL55oygcBp3tcDPf6CV6XXNEBQ'''
AUTH_CASTINGD='''Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBwbnB2ZUFSU3hWRVdLM092WUlVSCJ9.eyJpc3MiOiJodHRwczovL2ZhZGRvLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYWJjZWY3OTA4YzBjNjhhNWQyNWUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTkwMzkwMDA0LCJleHAiOjE1OTA0NzY0MDMsImF6cCI6IklYR0NNb1VVWUY1QTUxczJFV0NYQW5BZ2dvbDBUYXlvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.NvfsPoiz0EzDPxgFt4LZscn5z7nwtKcNTfnrdShu96FEOkCk2kMc357R2ZSisht7wu1KhcL05lqgCkzKRAo8hEC0KArrJCojXI5OWI-DOlevk2-qpDMftdikkq8pkLSz4IMQVmA4L2vYKNWK6X4q28jhbqZ-StnVZviNLnw8v2rDxO_fAjp5PhLR1pyymqxAmzAOI5TxO0_lBbwmRmK8uN56X8BdJ_nQBJwsFHsNg2UK7wnSZBs457OPp6-j4eZsGoejF6UfMZN-Hp1Tb3uVtDI2StF1eLjotIlD25UxuIy5LjMV5LN6ZibWzzw_zCRQ8bjyWGxoBmrvBiiQ2XP5jA'''
AUTH_CASTINGA='''Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBwbnB2ZUFSU3hWRVdLM092WUlVSCJ9.eyJpc3MiOiJodHRwczovL2ZhZGRvLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYWI5NjkyZGNlODBjNmYxN2E5OWQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTkwMzkwMTI2LCJleHAiOjE1OTA0NzY1MjUsImF6cCI6IklYR0NNb1VVWUY1QTUxczJFV0NYQW5BZ2dvbDBUYXlvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.w-AgUYif60IZ4UERdLyCPu6-029wm_i3tQGOWtw-BJB1vNlhzUBcmFA53OQ8YzmEs7NR0sf5L77qiG1zv-XnLvep76-T9waXb0UzENLzr8R51O_Bq7Hi2ISrXF3t8zN7Ri0OOjpPJPhKifrVrVtYVcTxDvvGEprXYL6vI0cMWmz6PpKba0q-ZtH6hcyGF6TFdBIC5HCupXLUJ3cTftU2JlJqxvB7yRwNPAvA4bdodTbt9_I6KNtegYMt4370xtejOU_4tJU1qvON2KiVJBBxUaBgrxSLqVsxctEgFgkR7OwK7iAV05KJCFcmntu72NX1JEaLjV_aySfssiwf6kxNrA'''



class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "catest"
        self.database_path = "postgres://{}:{}@{}/{}".format('fardeen', 'admin','localhost', self.database_name)
        setup_db(self.app, self.database_path)
        self.access_token_ep={'Authorization': AUTH_EXECUTIVEP}
        self.access_token_cd={'Authorization': AUTH_CASTINGD}
        self.access_token_ca={'Authorization': AUTH_CASTINGA}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.access_token_ep)
        #print(res.headers)
        
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['actors']))
        self.assertTrue((data['total_actors']))

    def test_add_actor(self):
        res = self.client().post('/actors',
        json={'name': 'fake actor',
              'age': 55,
              'gender': 'fake female'
              }, headers=self.access_token_ep)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor(self):
        res = self.client().patch('actors/2',
        json={'name': 'dalia mahmoud',
               'age': 20,
               'gender': 'female',
                },headers=self.access_token_ep)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor_2(self):
        res = self.client().patch('actors/24',
        json={'name': 'sameh gaber karar ',
               'age': 44,
               'gender': 'male',
                } ,headers=self.access_token_ep)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")


    def test_delete_actor(self):
        res = self.client().delete('/actors/1' ,headers=self.access_token_ep)
        data =json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    #testing deleting a actor ( non-successful trial)
    def test_delete_actor_2(self):
        res = self.client().delete('/actors/102' ,headers=self.access_token_ep)
        data =json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "resource not found")



    def test_get_movies(self):
        res = self.client().get('/movies' ,headers=self.access_token_ep)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
      
    #Testing adding a new movie 
    def test_add_movie(self):
        res = self.client().post('/movies',
        json={'title': 'too hot to handle',
              'release_date': '25nd april '
              } ,headers=self.access_token_ep)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['created'])

    #test editing a movie (successful trail)
    def test_patch_movie(self):
        res = self.client().patch('movies/3',
        json={'title': 'lacasa is over ',
               'release_date': 'october ao'
                } ,headers=self.access_token_ep)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))
        self.assertTrue(data['updated_movie_id'])
    
    #test editing a movie (non-successful trial)
    def test_patch_movie_2(self):
        res = self.client().patch('movies/22',
        json={'title': 'my movie ',
               'release_date': 'a long ago'
                } , headers=self.access_token_ep)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    #testing deleting a movie (successful trial )
    def test_delete_movie(self):
        res = self.client().delete('/movies/5',headers=self.access_token_ep) 
        data =json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    #testing deleting a movie (non-successful trial ))
    def test_delete_movie_2(self):
        res = self.client().delete('/movies/102', headers=self.access_token_ep)
        data =json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "resource not found")


    def test_delete_movie_3(self):
        res = self.client().delete('/movies/5' , headers=self.access_token_cd)
        data =json.loads(res.data)
        self.assertEqual(res.status_code,403)

    
    def test_add_movie(self):
        res = self.client().post('/movies',
        json={'title': 'Elite',
              'release_date': '25th april '
              } , headers=self.access_token_cd )
        data = json.loads(res.data)
        self.assertEqual(res.status_code,403)

    def test_delete_movie_4(self):
        res = self.client().delete('/movies/5' , headers=self.access_token_ca)
        data =json.loads(res.data)
        self.assertEqual(res.status_code,403)


    def test_add_movie_1(self):
        res = self.client().post('/movies',
        json={'title': 'Elite',
              'release_date': '25th april '
              } , headers=self.access_token_ca)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,403)



if __name__ == "__main__":
    unittest.main()
