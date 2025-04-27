import requests
from typing import Tuple, Optional


class TaskAPI:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/tasks"):
        self.base_url = base_url
        self.session = requests.Session()

    def _get_headers(self, token: str):
        return {"Authorization": f"Bearer {token}"}

    def create_task(self, token: str, title: str, description: str):
        try:
            response = self.session.post(
                f"{self.base_url}/",
                json={"title": title, "description": description},
                headers=self._get_headers(token)
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return None, "Connection error"

    def get_tasks(self, token: str, is_done: bool = None):
        try:
            params = {"is_done": is_done} if is_done is not None else {}
            response = self.session.get(
                f"{self.base_url}/",
                params=params,
                headers=self._get_headers(token)
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return None, "Connection error"

    def update_task(self, token: str, task_id: int, is_done: bool):
        try:
            response = self.session.put(
                f"{self.base_url}/{task_id}/",
                json={"is_done": is_done},
                headers=self._get_headers(token)
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def delete_task(self, token: str, task_id: int):
        try:
            response = self.session.delete(
                f"{self.base_url}/{task_id}/",
                headers=self._get_headers(token)
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False