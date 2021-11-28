import miro
from . import base, picture
from enum import Enum

class UserState(str,Enum):
    REGISTERED = "registered"
    NOT_REGISTERED = "not_registered"
    TEMPORARY = "temporary"
    DELETED = "deleted"

    def __repr__(self) -> str:
        return self.value


class TeamUserRole(str,Enum):
    NON_TEAM = "non_team"
    MEMBER = "member"
    ADMIN = "admin"

    def __repr__(self) -> str:
        return self.value


class User(base.MiroObject):
    def __init__(self, data: dict, client):
        super().__init__(data.get("id"), client, base.MiroObjectType.USER)
        self.name = data.get("name")

    def __repr__(self):
        attrs = ("name", "id")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        return f"<User {' '.join(resolved)}>"


class TeamUser(base.MiroObject):
    def __init__(self, data: dict, client):
        super().__init__(data.get("id"), client, base.MiroObjectType.TEAM_USER)
        self.user = User(data.get("user"), client)
        self.team = client.team
        self.role = TeamUserRole(data.get("role"))
        self.created_at = miro.utils.parse_date(data.get("createdAt", ""))
        self.modified_at = miro.utils.parse_date(data.get("modifiedAt", ""))
        self.created_by = User(data.get("createdBy"), client)
        self.modified_by = User(data.get("modifiedBy"), client)

    def __repr__(self):
        attrs = ("user", "id", "team", "role")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        return f"<TeamUser {' '.join(resolved)}>"


class BoardUser(User):
    pass


class FullUser(User):
    def __init__(self, data: dict, client):
        super().__init__(data,client)
        self.created_at = miro.utils.parse_date(data.get("createdAt",""))
        self.company = data.get("company",None)
        self.role = data.get("role")
        self.industry = data.get("industry",None)
        self.email = data.get("email")
        self.state = UserState(data.get("state"))
        self.picture = picture.Picture(data.get("picture"),self)

    def __repr__(self):
        attrs = ("name", "id", "state", "company", "role")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        return f"<FullUser {' '.join(resolved)}>"
