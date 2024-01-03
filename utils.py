import json
from typing import List, Tuple

from lab.fpl_optimization_strategies.Player import Player


def read_instance(filename: str) -> List[Player]:
    with open("data/" + filename, "r", encoding="ISO-8859-1") as f:
        lines = f.readlines()
        instance_list = []
        for line in lines:
            line = line.strip()
            line = line.split(",")
            line = [int(line[0]), line[1], line[2], line[3], int(line[4]), float(line[5])]
            instance_list.append(Player(*line))

    return instance_list


def get_constraints(filename: str) -> Tuple[dict, dict, dict]:
    with open("../../lab/fpl_optimization_strategies/" + filename, "r") as file:
        constraints_data = json.load(file)

    max_dict = constraints_data["max_number_per_position"]
    min_dict = constraints_data["starting_11_min"]
    max_11_dict = constraints_data["starting_11_max_per_position"]

    return max_dict, min_dict, max_11_dict


def get_club_dict(pl: List[Player]) -> dict:
    dict_ = {}
    for p in pl:
        dict_[p.club] = 3
    return dict_


def calculate_score(team: List[Player]) -> int:
    score = 0
    for player in team:
        score += player.points
    return score


def calculate_budget(team: List[Player]) -> int:
    budget = 0
    for player in team:
        budget += player.price
    return budget


def print_team(team: List[Player]) -> str:
    first_team = team[:11]
    subs = team[11:]
    team_str = ''
    for i in range(11):
        team_str += str(first_team[i].player_id) + ","
    team_str = team_str[:-1]
    team_str += "\n"
    for i in range(4):
        team_str += str(subs[i].player_id) + ","
    team_str = team_str[:-1]
    return team_str


def write_results(team: List[Player], filename: str):
    team_str = print_team(team)
    with open("results/" + filename, 'w') as f:
        f.write(team_str)


def generate_neighbourhood(position, instance, neighbourhood_size):
    neighbourhood = []
    for player in instance:
        if len(neighbourhood) == neighbourhood_size:
            break
        if player.position == position:
            neighbourhood.append(player)

    return neighbourhood
