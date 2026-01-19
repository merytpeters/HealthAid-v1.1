from fastapi.testclient import TestClient

from main import app

_base_client = TestClient(app)


class APIV1Client:
    @property
    def cookies(self):
        return _base_client.cookies

    def get(self, url, **kwargs):
        return _base_client.get(f"/api/v1{url}", **kwargs)

    def post(self, url, **kwargs):
        return _base_client.post(f"/api/v1{url}", **kwargs)

    def put(self, url, **kwargs):
        return _base_client.put(f"/api/v1{url}", **kwargs)

    def delete(self, url, **kwargs):
        return _base_client.delete(f"/api/v1{url}", **kwargs)


client = APIV1Client()
