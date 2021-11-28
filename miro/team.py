import miro
from . import user, base, picture, enums, board
from typing import List


class Team(base.MiroObject):
    def __init__(self,data: dict, client):
        super().__init__(data.get("id"),client,enums.MiroObjectType.TEAM)
        self.created_at = miro.utils.parse_date(data.get("createdAt",""))
        self.modified_at = miro.utils.parse_date(data.get("modifiedAt",""))
        self.created_by = user.User(data.get("createdBy"),client)
        self.modified_by = user.User(data.get("modifiedBy"),client)
        self.name = data.get("name")
        if picture_data := data.get("picture"):
            self.picture = picture.Picture(picture_data, self)
        else:
            self.picture = None
        self.users = self.get_team_users()
        self.boards = self.get_team_boards()

    def __repr__(self) -> str:
        attrs = ("name", "id")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        resolved.append(f"user_count={len(self.users)}")
        return f"<Team {' '.join(resolved)}>"

    def get_team_users(self) -> List[user.TeamUser]:
        return [user.TeamUser(data, client=self.client, team=self) for data in self.client.get_request("/teams/{id}/user-connections",id=self.id)["data"]]

    def get_team_boards(self) -> List[board.Board]:
        return [board.Board(data, client=self.client, team=self) for data in self.client.get_request("/teams/{id}/boards",id=self.id)["data"]]

    def get_current_user(self) -> user.TeamUser:
        return user.TeamUser(self.client.get_request("/teams/{id}/user-connections/me".format(id=self.id))["data"], client=self.client)

    def invite(self,*emails: str) -> List[user.TeamUser]:
        return [user.TeamUser(data, client=self.client) for data in self.client.post_request("/teams/{id}/invite",id=self.id, data={"emails":emails})["data"]]

    def update(self, **data) -> None:
        pass