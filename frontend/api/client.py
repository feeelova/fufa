import requests
from typing import Tuple, Optional


class AuthAPI:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/auth"):
        self.base_url = base_url
        self.session = requests.Session()

    def _handle_response(self, response: requests.Response) -> Tuple[bool, str]:
        if response.status_code == 200:
            return True, ""
        try:
            error = response.json().get("detail", "Unknown error")
        except:
            error = f"HTTP error {response.status_code}"
        return False, error

    def login(self, email: str, password: str) -> Tuple[Optional[dict], str]:
        try:
            response = self.session.post(
                f"{self.base_url}/login/", json={"email": email, "password": password}
            )
            success, error = self._handle_response(response)
            return (response.json(), "") if success else (None, error)
        except requests.exceptions.RequestException:
            return None, "Connection error"

    def register(self, email: str, password: str) -> Tuple[bool, str]:
        try:
            response = self.session.post(
                f"{self.base_url}/register/",
                json={"email": email, "password": password},
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException:
            return False, "Connection error"

    def get_profile(self, token: str) -> Tuple[Optional[dict], str]:
        try:
            response = self.session.get(
                f"{self.base_url}/profile/",
                headers={"Authorization": f"Bearer {token}"},
            )
            return (
                (response.json(), "")
                if response.status_code == 200
                else (None, "Unauthorized")
            )
        except requests.exceptions.RequestException:
            return None, "Connection error"
