from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class AppTests(TestCase):
    
    def setUp(self):
        """Add test user"""
        Post.query.delete()
        User.query.delete()
        user = User(first_name='Test', last_name='User', img_url='')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        post = Post(title='Test', content='Post', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """Clean up transactions"""
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="mb-4">Blogly Recent Posts</h1>', html)

    def test_not_found(self):
        with app.test_client() as client:
            res = client.get('/users/0000/edit')
            self.assertEqual(res.status_code, 308)
            res = client.get(f'/users/0000/edit', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="card-header">Page Not Found</div>', html)

    ############ TESTING USERS ROUTES ############

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="list-group">', html)

    def test_show_user(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="card-text">User Info...</p>', html)
            self.assertIn('<ul class="list-group list-group-flush">', html)

    def test_create_user(self):
        with app.test_client() as client:
            data = {
                'first-name': 'New', 
                'last-name': 'User', 
                'img-url': 'https://upload.wikimedia.org/wikipedia/commons/1/1e/Default-avatar.jpg'
                }
            res = client.post('/users/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_update_user(self):
        with app.test_client() as client:
            data = {
                'first-name': 'New', 
                'last-name': 'Update', 
                'img-url': 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'
                }
            res = client.post(f'/users/{self.user_id}/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    ############ TESTING POSTS ROUTES ############

    def test_show_post(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="card mb-3 post-card">', html)

    def test_add_post(self):
        with app.test_client() as client:
            data = {
                'title': 'Post', 
                'content': 'Content', 
                }
            res = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="card-text">User Info...</p>', html)
            self.assertIn('<li class="list-group-item d-flex justify-content-between align-items-start">', html)

    def test_update_post(self):
        with app.test_client() as client:
            data = {
                'title': 'Test', 
                'content': 'Content', 
                }
            res = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="card mb-3 post-card">', html)

    def test_delete_post(self):
        with app.test_client() as client:
            res = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="card-text">User Info...</p>', html)
            self.assertIn('<ul class="list-group list-group-flush">', html)