from locust import HttpUser, between, task, TaskSet

class SampleTest(TaskSet):
    @task
    def index(self):
        self.client.get("/")

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [SampleTest]
    