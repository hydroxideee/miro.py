from enum import Enum


class BoardSharingPolicy(str,Enum):
    PRIVATE = "private"
    VIEW = "view"
    COMMENT = "comment"
    EDIT = "edit"

    def __repr__(self) -> str:
        return self.value


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


class MiroObjectType(str,Enum):
    TEAM = "team"
    BOARD = "board"
    WIDGET = "widget"
    USER = "user"
    TEAM_USER = "team-user-connection"
    BOARD_USER = "board-user-connection"
    PICTURE = "picture"

    def __repr__(self) -> str:
        return self.value