import requests
import miro
from . import team, user


class Client:
    def __init__(self, access_token: str):
        self.access_headers = {
            "Authorization": f"Bearer {access_token}"}
        self.base_url = "https://api.miro.com/v1"
        data = self.get_request("/oauth-token")
        self.team = self.get_team(data["team"]["id"])

    def get_request(self, url: str, headers: dict = None, **url_values) -> dict:
        return self.request(method="GET", url=url, headers=headers, **url_values)

    def post_request(self, url: str, headers: dict = None, data: dict = None, **url_values) -> dict:
        return self.request(method="POST", url=url, headers=headers, data=data, **url_values)

    def patch_request(self, url: str, headers: dict = None, data: dict = None, **url_values) -> dict:
        return self.request(method="PATCH", url=url, headers=headers, data=data, **url_values)

    def delete_request(self, url: str, headers: dict = None, **url_values) -> dict:
        return self.request(method="DELETE", url=url, headers=headers, **url_values)

    def get_pagination_data(self, r_json: dict, headers: dict = None, method: str = "GET") -> list:
        data = r_json.get("data")
        while next_url := r_json.get("nextLink", None):
            r = requests.request(method=method, url=next_url,
                                 headers=self.access_headers if not headers else headers.update(self.access_headers))
            r_json = r.json()
            data.extend(r_json.get("data"))
        return data

    def request(self, method: str, url: str, headers: dict = None, data: dict = None, **url_values) -> dict:
        response = requests.request(method=method, url=self.base_url + url.format(**url_values),
                                    headers=self.access_headers if not headers else headers.update(self.access_headers),
                                    data=data)
        if not response.ok:
            raise miro.HTTPException(response)
        r_json = response.json()
        if data := self.get_pagination_data(r_json, headers):
            return {"data": data}
        return r_json

    def get_team(self, team_id: int | str) -> team.Team:
        return miro.Team(self.get_request("/teams/{id}", id=team_id), client=self)

    def get_user(self, user_id: int | str) -> user.FullUser:
        return user.FullUser(self.get_request("/users/{id}", id=user_id), client=self)

    def get_current_user(self) -> user.FullUser:
        return user.FullUser(self.get_request("/users/me"), client=self)

    def update_current_user(self, name: str) -> user.FullUser:
        return user.FullUser(self.patch_request("/users/me", data={"name": name}), client=self)
