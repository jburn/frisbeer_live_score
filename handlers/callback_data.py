from dataclasses import dataclass


@dataclass
class CallbackData:
    action: str
    gid: str | None = None
    team: str | None = None
    player: str | None = None
    index: str | None = None
    winner: str | None = None

    @classmethod
    def parse(cls, data: str):
        parts = data.split(":")
        action = parts[0]

        if action == "assign":
            _, gid, team, player = parts
            return cls(action, gid, team, player=player)

        if action == "mark":
            _, gid, team, index = parts
            return cls(action, gid, team, index=int(index))

        if action == "end_round":
            _, gid, winner = parts
            return cls(action, gid, winner=winner)

        _, gid = parts
        return cls(action, gid)
