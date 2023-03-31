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


# test postdetail view
class PostDetailViewTests(APITestCase):
    def setUp(self):
        # create two users
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        # test both users making a post
        Post.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Post.objects.create(
            owner=brian, title='another title', content='brians content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        # test if a get request retieves the first post
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test can not retieve a post
    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test user can update a post
    def test_user_can_update_own_post(self):
        # first login as Reference (adam)
        self.client.login(username='adam', password='pass')
        # send a put (update) request to the url with their id
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        # fetch post from the database by id
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test if user can not update another users post
    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
