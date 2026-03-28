from dataclasses import dataclass


@dataclass
class CallbackData:
    action: str
    gid: str | None = None
    team: str | None = None
    player: str | None = None
    index: str | None = None
    winner: str | None = None
    round_n: str | None = None


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

        if action == "start_round":
            _, gid, round_n = parts
            return cls(action, gid, round_n=round_n)

        _, gid = parts
        return cls(action, gid)
