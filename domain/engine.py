from domain.models import GameState, Game
from domain.actions import Action, StartRound, EndRound, StartGame, AssignKnocks

ASSIGN_MAP = {"b": "b", "k": " ", "f": "u", "u": "u", " ": " "}


def assign_format_beer(current: str) -> str:
    return ASSIGN_MAP.get(current, current)


def initial_state() -> GameState:
    return GameState(team1_beers=["b"] * 8, team2_beers=["b"] * 8, reverse=False)


def apply_action(state: GameState, action: Action) -> GameState:
    if action.__class__.__name__ == "SwitchSides":
        state.reverse = not state.reverse

    elif action.__class__.__name__ == "AssignKnocks":
        knocks = action.knocked_beers
        for knock in knocks:
            team, index, to = knock
            index = int(index)
            beers = getattr(state, f"{team}_beers")
            beers[index] = assign_format_beer(to)

    elif action.__class__.__name__ == "StartGame":
        pass

    elif action.__class__.__name__ == "EndRound":
        state = initial_state()

    return state


def compute_state(game: Game) -> GameState:
    state = initial_state()

    for i in reversed(range(len(game.history))):
        if isinstance(game.history[i], (StartRound, StartGame)):
            start_i = i
            break

    actions = game.history[start_i:]

    for action in actions:
        state = apply_action(state, action)

    return state


def get_current_round_knocks(actions: list[Action]) -> list[AssignKnocks]:
    """
    Return a list of AssignKnocks events from the latest player or ongoing round.
    """
    start_i = None

    for i in reversed(range(len(actions))):
        if isinstance(actions[i], (StartRound, StartGame)):
            start_i = i
            break

    if start_i is None:
        return []

    for j in range(start_i + 1, len(actions)):
        if isinstance(actions[j], EndRound):
            return list(
                filter(lambda x: isinstance(x, AssignKnocks), actions[start_i + 1 : j])
            )

    return list(filter(lambda x: isinstance(x, AssignKnocks), actions[start_i:]))


def count_player_knocks(game, actions: list[AssignKnocks]):
    results = {
        "team1": {player: [0, 0] for player in game.team1.players},
        "team2": {player: [0, 0] for player in game.team2.players},
    }
    for knock in actions:
        team = knock.team
        player = knock.player
        beers = knock.knocked_beers
        for beer in beers:
            owner, _, res = beer
            if res != "k":
                continue
            if team == owner:
                results[team][player][1] += 1
                continue
            results[team][player][0] += 1
    return results


def count_round_wins(actions):
    round_results = [a for a in actions if isinstance(a, EndRound)]
    t1_score = len([round for round in round_results if round.winner == "team1"])
    t2_score = len([round for round in round_results if round.winner == "team2"])

    return t1_score, t2_score
