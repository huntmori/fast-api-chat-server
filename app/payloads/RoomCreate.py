from app.entities.room import JoinType, RoomType


class RoomCreate:

    join_type: JoinType
    room_type: RoomType
    room_name: str
    room_password: str | None
    max_users: int

    def __init__(self, **data):
        self.__dict__.update(data)

    @staticmethod
    def from_dict(data: dict):
        room = RoomCreate(**data)
        return room

    def __str__(self):
        return str(self.__dict__)