from dataclasses import dataclass, field
from typing import List
from domain.actions import action_to_dict, action_from_dict


@dataclass
class Team:
    name: str
    emoji: str
    players: List[str]

    def to_dict(self):
        return {"name": self.name, "emoji": self.emoji, "players": self.players}

    @staticmethod
    def from_dict(data: dict) -> "Team":
        return Team(name=data["name"], emoji=data["emoji"], players=data["players"])


@dataclass
class GameState:
    team1_beers: List[str]
    team2_beers: List[str]
    reverse: bool = False


@dataclass
class Game:
    id: str
    timestamp: float
    team1: Team
    team2: Team
    history: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "team1": self.team1.to_dict(),
            "team2": self.team2.to_dict(),
            "history": [action_to_dict(a) for a in self.history],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Game":
        team1 = Team.from_dict(data=["team1"])
        team2 = Team.from_dict(data=["team2"])

        raw_history = data.get("history", [])
        history = []

        for item in raw_history:
            try:
                history.append(action_from_dict(item))
            except Exception:
                continue  # skip corrupted actions

        return cls(
            id=data["id"],
            timestamp=data.get("timestamp", 0),
            team1=team1,
            team2=team2,
            history=history,
        )
