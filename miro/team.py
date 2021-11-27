import miro
from . import user, board, picture
from typing import List

class Team:
    def __init__(self,data: dict, client):
        self.id = data.get("id")
        self.created_at = miro.utils.parse_date(data.get("createdAt",""))
        self.modified_at = miro.utils.parse_date(data.get("modifiedAt",""))
        self.created_by = user.User(data.get("createdBy"))
        self.modified_by = user.User(data.get("modifiedBy"))
        self.name = data.get("name")
        self.picture = picture.Picture(data.get("picture"))
        self.client = client
    def get_team_users(self) -> List[user.TeamUser]:
        return [user.TeamUser(data) for data in self.client.get_request("/teams/{id}/user-connections",id=self.id)["data"]]
    def get_current_user(self) -> user.TeamUser:
        return user.TeamUser(self.client.get_request("/teams/{id}/user-connections/me".format(id=self.id))["data"])
    def invite(self,*emails: str) -> List[user.TeamUser]:
        return [user.TeamUser(data) for data in self.client.post_request("/teams/{id}/invite",id=self.id,data={"emails":emails})["data"]]
    def update(self, **data) -> None:
        pass