import random

from lab.fpl_optimization_strategies.constraints import *


def rcl_first_team(alpha: float, instance_sorted: List[Player]) -> List[Player]:
    c_max = instance_sorted[0].points_per_price
    c_min = instance_sorted[-1].points_per_price
    threshold = c_max - alpha * (c_max - c_min)
    return [player for player in instance_sorted if player.points_per_price >= threshold]


def rcl_subs(alpha: float, instance_sorted: List[Player]) -> List[Player]:
    c_min = instance_sorted[0].price
    c_max = instance_sorted[-1].price
    threshold = c_max + alpha * (c_max - c_min)
    return [player for player in instance_sorted if player.price <= threshold]


def greedy(alpha: float, instance: List[Player], club_dict: dict, starting_11_min_dict: dict,
           starting_11_max_per_position_dict: dict, max_number_per_position_dict: dict) -> List[Player]:
    team = []
    budget = 100
    instance_sorted_by_price_ascending = sorted(instance, key=lambda x: x.price)
    instance_sorted_by_points_per_price = sorted(instance, key=lambda x: x.points_per_price, reverse=True)
    n = len(instance)
    for i in range(n):
        if len(team) == 11:
            break
        player = random.choice(rcl_first_team(alpha, instance_sorted_by_points_per_price[i:]))

        if (check_budget_constraint(budget, player.price)
                and check_club_constraint(club_dict, player.club, player.club)
                and not check_min_player_constraint(starting_11_min_dict, player.position, team)
                and check_team_positions_constraint(starting_11_min_dict,
                                                    starting_11_max_per_position_dict,player.position)
                and player not in team

        ):
            if starting_11_min_dict[player.position] > 0:
                starting_11_min_dict[player.position] -= 1
            if starting_11_max_per_position_dict[player.position] > 0:
                starting_11_max_per_position_dict[player.position] -= 1
            if club_dict[player.club] > 0:
                club_dict[player.club] -= 1
            if max_number_per_position_dict[player.position] > 0:
                max_number_per_position_dict[player.position] -= 1
            team.append(player)
            budget -= player.price

    for i in range(n):
        if len(team) == 15:
            break

        player = random.choice(rcl_subs(alpha, instance_sorted_by_price_ascending[i:]))

        if (check_budget_constraint(budget, player.price)
                and check_club_constraint(club_dict, player.club, player.club)
                and max_number_per_position_dict[player.position] > 0
        ):
            if max_number_per_position_dict[player.position] > 0:
                max_number_per_position_dict[player.position] -= 1
            if club_dict[player.club] > 0:
                club_dict[player.club] -= 1
            team.append(player)
            budget -= player.price

    return team
