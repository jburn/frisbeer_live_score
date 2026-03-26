import sqlite3
import json
from domain.models import Game, Team
from domain.actions import SwitchSides, AssignKnocks, StartGame, StartRound, EndRound


class Storage:
    def __init__(self, path="games.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            data TEXT
        )
        """)

    def save(self, game: Game):
        data = json.dumps(game.to_dict())
        self.conn.execute(
            "INSERT OR REPLACE INTO games (id, data) VALUES (?, ?)", (game.id, data)
        )
        self.conn.commit()

    def load(self, gid: str) -> Game:
        cur = self.conn.execute("SELECT data FROM games WHERE id = ?", (gid,))
        row = cur.fetchone()
        if not row:
            return None

        raw = json.loads(row[0])

        history = []
        for a in raw.get("history", []):
            if a["type"] == "SwitchSides":
                history.append(SwitchSides(message_ids=a["message_ids"]))
            elif a["type"] == "AssignKnocks":
                history.append(
                    AssignKnocks(
                        a["team"],
                        a["player"],
                        a["knocked_beers"],
                        message_ids=a["message_ids"],
                    )
                )
            elif a["type"] == "StartGame":
                history.append(StartGame(message_ids=a["message_ids"]))
            elif a["type"] == "StartRound":
                history.append(
                    StartRound(round_n=a["round_n"], message_ids=a["message_ids"])
                )
            elif a["type"] == "EndRound":
                history.append(
                    EndRound(winner=a["winner"], message_ids=a["message_ids"])
                )

        game = Game(
            id=raw["id"],
            timestamp=raw["timestamp"],
            team1=Team(**raw["team1"]),
            team2=Team(**raw["team2"]),
            history=history,
        )

        return game

    def delete(self, gid):
        self.conn.execute("DELETE FROM games WHERE id = ?", (gid,))
        self.conn.commit()

    def list_games(self) -> list[Game]:
        cursor = self.conn.execute("""
            SELECT 
                id,
                json_extract(data, '$.timestamp') AS timestamp,
                json_extract(data, '$.team1.name') AS team1_name,
                json_extract(data, '$.team1.emoji') AS team1_emoji,
                json_extract(data, '$.team2.name') AS team2_name,
                json_extract(data, '$.team2.emoji') AS team2_emoji
            FROM games
            ORDER BY rowid DESC
        """)

        return cursor.fetchall()
