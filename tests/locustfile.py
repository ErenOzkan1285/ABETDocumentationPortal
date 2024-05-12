import os
from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    def on_start(self):
        """on_start is called when a Locust start before any task is scheduled"""
        self.login()

    def login(self):
        self.client.post("/", data={"email": 'me@metu.edu.tr', "password": '1234'})

    @task(1)
    def upload_single_small_file(self):
        file_path = os.path.join(os.path.dirname(__file__), 'small.xlsx')
        with open(file_path, 'rb') as excel_file:
            self.client.post('/upload', files={'file': (excel_file, 'small.xlsx')})

    @task(2)
    def upload_single_large_file(self):
        file_path = os.path.join(os.path.dirname(__file__), 'large.xlsx')
        with open(file_path, 'rb') as excel_file:
            self.client.post('/upload', files={'file': (excel_file, 'large.xlsx')})

    @task(3)
    def upload_multiple_small_files(self):
        files = []
        for i in range(10):
            file_path = os.path.join(os.path.dirname(__file__), 'small.xlsx')
            files.append(('file', (open(file_path, 'rb'), 'small.xlsx')))
        self.client.post('/upload', files=files)

    @task(4)
    def upload_multiple_large_files(self):
        files = []
        for i in range(5):
            file_path = os.path.join(os.path.dirname(__file__), 'large.xlsx')
            files.append(('file', (open(file_path, 'rb'), 'large.xlsx')))
        self.client.post('/upload', files=files)

    @task(5)
    def upload_files_during_peak_usage(self):
        files = []
        for i in range(3):
            small_file_path = os.path.join(os.path.dirname(__file__), 'small.xlsx')
            large_file_path = os.path.join(os.path.dirname(__file__), 'large.xlsx')
            files.append(('file', (open(small_file_path, 'rb'), 'small.xlsx')))
            files.append(('file', (open(large_file_path, 'rb'), 'large.xlsx')))
        self.client.post('/upload', files=files)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
