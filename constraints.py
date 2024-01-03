from typing import List

from lab.fpl_optimization_strategies.Player import Player

MAX_STARTING_PLAYERS = 11


def check_budget_constraint(budget: float, price: float) -> bool:
    return budget - price >= 0


def check_club_constraint(club_dict: dict, neighbour_club: str, player_club: str) -> bool:
    return club_dict[neighbour_club] > 0 or neighbour_club == player_club


def check_min_player_constraint(dict_: dict, position: str, team: List[Player]) -> bool:
    """
    Returns true if after adding a player, there would be no more
    slots left for other positions that need to be fulfilled
    """
    dict_copy = dict_.copy()
    if dict_copy[position] > 0:
        dict_copy[position] -= 1

    slots_left_local = MAX_STARTING_PLAYERS - len(team)

    minimum_slots_left_local = sum(dict_copy.values())

    return slots_left_local == minimum_slots_left_local


def check_team_positions_constraint(starting_11_min_dict: dict, starting_11_max_per_position_dict: dict,
                                    position: str) -> bool:
    return starting_11_min_dict[position] > 0 or starting_11_max_per_position_dict[position] > 0


def check_duplicate(player: Player, team: List[Player]) -> bool:
    if player.player_id in [p.player_id for p in team]:
        return False
