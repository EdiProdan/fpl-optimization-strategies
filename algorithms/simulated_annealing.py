import math
import random
from typing import List

from lab.fpl_optimization_strategies.Player import Player
from lab.fpl_optimization_strategies.constraints import check_budget_constraint, check_club_constraint
from lab.fpl_optimization_strategies.utils import generate_neighbourhood, calculate_score, calculate_budget, get_club_dict


def simulated_annealing(initial_team: List[Player], instance: List[Player], temperature: float, temperature_decrement: float) -> List[Player]:
    temperature = temperature
    temperature_decrement = temperature_decrement
    team = initial_team.copy()
    club_dict = get_club_dict(instance)
    for player in team:
        club_dict[player.club] -= 1
    iters = 0

    instance_sorted_by_points = sorted(instance, key=lambda x: x.points, reverse=True)

    gk_neighbourhood = generate_neighbourhood("GK", instance_sorted_by_points, 50)
    def_neighbourhood = generate_neighbourhood("DEF", instance_sorted_by_points, 50)
    mid_neighbourhood = generate_neighbourhood("MID", instance_sorted_by_points, 50)
    fw_neighbourhood = generate_neighbourhood("FW", instance_sorted_by_points, 50)

    neighborhoods_dict = {"GK": gk_neighbourhood, "DEF": def_neighbourhood, "MID": mid_neighbourhood,
                          "FW": fw_neighbourhood}

    solution_qualities = [calculate_score(team[:11])]

    while temperature > 0.001:
        iters += 1

        current_team = permutate_current_team(team, neighborhoods_dict, club_dict)

        if check_acceptance_criteria(current_team, team, temperature):
            team = current_team
        else:
            club_dict = get_club_dict(instance)
            for player in team:
                club_dict[player.club] -= 1

        temperature *= temperature_decrement
        solution_qualities.append(calculate_score(team[:11]))

    return team


def one_sided_sigmoid(temperature: float) -> float:
    return 1 - math.exp(-temperature)


def permutate_current_team(team: List[Player], neighborhoods_dict: dict, club_dict: dict) -> List[Player]:
    current_team = team.copy()
    starting_team = current_team[:11]
    neighborhood_teams = []
    budget = calculate_budget(current_team)
    for player in starting_team:

        neighbourhood = neighborhoods_dict[player.position]
        for neighbour in neighbourhood:

            if (check_budget_constraint(100 - budget + player.price, neighbour.price)
                    and check_club_constraint(club_dict, neighbour.club, player.club)
                    and neighbour not in current_team):
                temp_team = team.copy()
                temp_team[temp_team.index(player)] = neighbour

                neighborhood_teams.append(temp_team)

    return random.choice(neighborhood_teams)


def check_acceptance_criteria(current_team: List[Player], team: List[Player], temperature: float) -> bool:
    delta_cost = calculate_score(current_team[:11]) - calculate_score(team[:11])

    if delta_cost > 0:
        return True

    probability = math.exp(- abs(delta_cost / temperature))
    return random.uniform(0, 1) < probability
