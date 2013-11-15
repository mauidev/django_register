"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""




import httplib
import json
import urllib
import uuid
import unittest
import sqlite3



class TestUser(unittest.TestCase):
   
    
    def setUp(self):
        conn = sqlite3.connect('../register.db')
        cursor = conn.cursor()
        query = """delete from registerweb_user"""
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def test_01_get_not_found(self):
        """ 
        Get a user that does not exist 
        """
        # content type header is not necessary for a GET http request
        # create a uuid of a record that does not exist
        my_id = str(uuid.uuid1())
        conn  = httplib.HTTPConnection("localhost",8000)
        conn.request('GET','/demo/api/v1/users/%s' % my_id)
        resp = conn.getresponse()
        self.assertEqual(resp.status,404)
    
    def test_02_post_form_errors(self):
        """ 
        Create a user with missing fields in the post. 
        """
        conn  = httplib.HTTPConnection("localhost",8000)
        encoded_form = urllib.urlencode({'login_id': 'testLoginId', 
                                         'first_name': 'bob', 
                                         'password' : 'mypass',
                                         'email':'toddb43@gmail.com'})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn.request('POST','/demo/api/v1/users',encoded_form,headers)
        resp = conn.getresponse()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        self.assertEqual(result['status'],'error')
        self.assertEqual(resp.status,400)
        errors = result['errors']
        self.assertTrue(len(errors) ==1)
        self.assertTrue(errors.get('last_name'),msg='expected error message for last_name')
    
    def test_03_post_success(self):
        """ 
        Create a user successfully 
        """
        resp = self._addUser()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        self.assertEqual(resp.status,201)
        self.assertTrue(result.get('id'), "expected an id to be returned")
        return result.get('id')    
        
    def test_04_post_duplicate(self):
        """ 
        Test the case where the login id is already in the database.
        """
        # add the user the first time
        self._addUser()
        # add the same user again
        resp = self._addUser()
        
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        self.assertEqual(resp.status,400)
        self.assertEqual(result['status'],'duplicate') 
                      
    def test_05_get_success(self):
        """
        Retrieve an existing user.
        """
        # add a user first
        resp = self._addUser()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        uuid = result['id']
        
        # retrieve the user
        conn  = httplib.HTTPConnection("localhost",8000)
        conn.request('GET','/demo/api/v1/users/%s' % uuid)
        resp = conn.getresponse()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        user_data = result['data']
        self.assertEqual(resp.status,200)
        self.assertEqual(user_data['login_id'],'testLoginId')
                
                
    def test_06_put_success(self):
        """
        Update a user.
        """
        # add a user first
        resp = self._addUser()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        uuid = result['id']
        
        # update the user
        conn  = httplib.HTTPConnection("localhost",8000)
        encoded_form = urllib.urlencode({'login_id': 'testLoginId', 
                                         'first_name': 'newbob',
                                         'last_name' : 'dog', 
                                         'password' : 'mypass',
                                         'email':'toddb43@gmail.com'})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn.request('PUT','/demo/api/v1/users/%s' % uuid,encoded_form,headers)
        resp = conn.getresponse()
        self.assertEqual(resp.status,200)       
        
        
    def test_07_put_bad_pk(self):
        """
        Update a user, but the primary key is the wrong one.
        """
        conn  = httplib.HTTPConnection("localhost",8000)
        encoded_form = urllib.urlencode({'login_id': 'testLoginId', 
                                         'first_name': 'bob',
                                         'last_name' : 'dog', 
                                         'password' : 'mypass',
                                         'email':'toddb43@gmail.com'})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        my_id = str(uuid.uuid1())
        conn.request('PUT','/demo/api/v1/users/%s' % my_id,encoded_form,headers)
        resp = conn.getresponse()
        self.assertEqual(resp.status,404)      
            
            
    def test_08_put_form_errors(self):
        """
        Update a user, but the form contains errors.
        """
        # add a user first
        resp = self._addUser()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        uuid = result['id']
        
        conn  = httplib.HTTPConnection("localhost",8000)
        encoded_form = urllib.urlencode({'login_id': 'testLoginId', 
                                         'last_name' : 'dog', 
                                         'password' : 'mypass',
                                         'email':'toddb43@gmail.com'})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn.request('PUT','/demo/api/v1/users/%s' % uuid,encoded_form,headers)
        resp = conn.getresponse()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        self.assertEqual(result['status'],'error')
        self.assertEqual(resp.status,400)
        errors = result['errors']
        self.assertTrue(len(errors) ==1)
        self.assertTrue(errors.get('first_name'),msg='expected error message for first_name')
       
    def test_09_delete_user(self):
        """
        Delete user.
        """
        # add a user first
        resp = self._addUser()
        data = resp.read()
        decoder = json.JSONDecoder()
        result = decoder.decode(data)
        uuid = result['id']
        
        # delete the user
        conn  = httplib.HTTPConnection("localhost",8000)
        conn.request('DELETE','/demo/api/v1/users/%s' % uuid)
        resp = conn.getresponse()
        self.assertEqual(resp.status,200)
                                         
    def _addUser(self):
        conn  = httplib.HTTPConnection("localhost",8000)
        encoded_form = urllib.urlencode({'login_id': 'testLoginId', 
                                         'first_name': 'bob',
                                         'last_name' : 'dog', 
                                         'password' : 'mypass',
                                         'email':'toddb43@gmail.com'})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn.request('POST','/demo/api/v1/users',encoded_form,headers)
        return conn.getresponse()
          
            

if __name__ == '__main__':
    unittest.main()