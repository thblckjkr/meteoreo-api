from locust import HttpUser, task

class API(HttpUser):
    @task
    def get_drivers(self):
        self.client.get("/api/v1/drivers/")

    @task
    def get_stations(self):
        self.client.get("/api/v1/stations/",  auth=("admin", "pass"))
