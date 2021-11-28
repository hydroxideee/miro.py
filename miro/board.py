import miro
from . import user, base, picture, enums
from typing import List


class SharingPolicy:
    def __init__(self,data: dict):
        self.access = enums.BoardSharingPolicy(data.get("access"))
        self.team_access = enums.BoardSharingPolicy(data.get("teamAccess"))
        self.account_access = enums.BoardSharingPolicy(data.get("accountAccess"))


class Board(base.MiroObject):
    def __init__(self, data: dict, client, team=None):
        super().__init__(data.get("id"), client, enums.MiroObjectType.BOARD)
        self.team = team or client.team
        self.created_at = miro.utils.parse_date(data.get("createdAt",""))
        self.modified_at = miro.utils.parse_date(data.get("modifiedAt",""))
        self.created_by = user.User(data.get("createdBy"),client)
        self.modified_by = user.User(data.get("modifiedBy"),client)
        self.owner = user.User(data.get("owner"),client)
        self.name = data.get("name")
        self.description = data.get("description")
        if picture_data := data.get("picture"):
            self.picture = picture.Picture(picture_data,self)
        else:
            self.picture = None
        self.view_url = data.get("viewLink")
        self.sharing_policy = SharingPolicy(data.get("sharingPolicy"))
        if current_user_connection := data.get("currentUserConnection"):
            self.current_user_connection = user.BoardUser(current_user_connection, client=self.client)
        else:
            self.current_user_connection = None

    def __repr__(self) -> str:
        attrs = ("name", "id")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        resolved.append(f"user_count={len(self.users)}")
        return f"<Board {' '.join(resolved)}>"

    def get_board_users(self) -> List[user.BoardUser]:
        return [user.BoardUser(data, client=self.client) for data in self.client.get_request("/boards/{id}/user-connections",id=self.id)["data"]]

    def share(self, *emails, role: enums.BoardRole, message: str = None, team_invitation_strategy: enums.TeamInvitationStrategy = None) -> List[user.BoardUser]:
        data = {"emails": emails,"role":role}
        if message:
            data["message"] = message
        if team_invitation_strategy:
            data["teamInvitationStrategy"] = team_invitation_strategy
        return [user.BoardUser(data, client=self.client) for data in self.client.post_request("/boards/{id}/share", id=self.id, data=data)["data"]]