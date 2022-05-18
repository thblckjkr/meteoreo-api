from locust import HttpUser, task

class API(HttpUser):
    @task
    def get_incidents(self):
        self.client.get("/api/v1/incidents/")

    @task
    def get_stations(self):
        self.client.get("/api/v1/stations/",  auth=("admin", "pass"))
