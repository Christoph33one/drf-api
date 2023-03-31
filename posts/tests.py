from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    # setup method is the first to run
    def setUp(self):
        # creatig a user to Reference in the tests for this class
        User.objects.create_user(username='adam', password='pass')

    # test if we can list posts in the data base
    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        # test a get network request for posts
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    # test login user can create a post
    def test_logged_in_user_can_create_post(self):
        # first we need to login is as a user, using the client method
        self.client.login(username='adam', password='pass')
        # test post request to 'post' with post data and save response to Variable
        response = self.client.post('/posts/', {'title': 'a title'})
        # count all posts
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_loggedin_to_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
