from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    host = "http://xaleksandraxx.pythonanywhere.com"
    wait_time = between(1, 3)

    @task
    def get_posts_with_comments_and_users(self):
        self.client.get('/')

    @task
    def get_posts_with_comments_and_users_limit(self):
        self.client.get('/10/')

    @task
    def get_comments_for_post(self):
        self.client.get('/1/comments/')

    @task
    def get_comments_by_postid(self):
        self.client.get('/comments/?postId=1')

    @task
    def get_user_albums(self):
        self.client.get('/albums/')

    @task
    def login(self):
        csrf_token = self.client.get("/login/").cookies.get('csrftoken', '')
        response = self.client.post("/login/", {"username": "testuser", "password": "testpass123"}, headers={"X-CSRFToken": csrf_token})
        print(response.text)

    @task
    def register(self):
        csrf_token = self.client.get("/register/").cookies.get('csrftoken', '')
        response = self.client.post("/register/", {"username": "testuser", "password": "testpass123"}, headers={"X-CSRFToken": csrf_token})
        print(response.text)

