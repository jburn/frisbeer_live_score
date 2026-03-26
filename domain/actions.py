from dataclasses import dataclass, field
from typing import List


@dataclass
class Action:
    message_ids: List[int] = field(default_factory=list, kw_only=True)


@dataclass
class StartGame(Action):
    pass


@dataclass
class StartRound(Action):
    round_n: int


@dataclass
class EndRound(Action):
    winner: str  # "team1" or "team2"


@dataclass
class AssignKnocks(Action):
    team: str  # "team1" or "team2"
    player: str
    knocked_beers: dict[tuple[str, int] : int]


@dataclass
class SwitchSides(Action):
    pass


def action_to_dict(action: Action):
    if isinstance(action, SwitchSides):
        return {"type": "SwitchSides", "message_ids": action.message_ids}
    if isinstance(action, AssignKnocks):
        return {
            "type": "AssignKnocks",
            "team": action.team,
            "player": action.player,
            "knocked_beers": action.knocked_beers,
            "message_ids": action.message_ids,
        }
    if isinstance(action, StartGame):
        return {"type": "StartGame", "message_ids": action.message_ids}
    if isinstance(action, StartRound):
        return {
            "type": "StartRound",
            "round_n": action.round_n,
            "message_ids": action.message_ids,
        }
    if isinstance(action, EndRound):
        return {
            "type": "EndRound",
            "winner": action.winner,
            "message_ids": action.message_ids,
        }
    raise ValueError(f"Unknown action: {action}")


def action_from_dict(data: dict):
    t = data["type"]

    if t == "SwitchSides":
        return SwitchSides(message_ids=data["message_ids"])
    if t == "AssignKnocks":
        return AssignKnocks(
            team=data["team"],
            player=data["player"],
            knocked_beers=data["knocked_beers"],
            message_ids=data["message_ids"],
        )
    if t == "StartGame":
        return StartGame(message_ids=data["message_ids"])
    if t == "StartRound":
        return StartRound(round_n=data["round_n"], message_ids=data["message_ids"])
    if t == "EndRound":
        return EndRound(winner=data["winner"], message_ids=data["message_ids"])
    raise ValueError(f"Invalid action data: {data}")
