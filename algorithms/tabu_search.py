from typing import Tuple

from lab.fpl_optimization_strategies.constraints import *
from lab.fpl_optimization_strategies.utils import calculate_score, generate_neighbourhood, calculate_budget, get_club_dict


def tabu_search(initial_team: List[Player], instance: List[Player], tabu_tenure: int, max_iter: int) -> List[Player]:
    team = initial_team.copy()
    budget = calculate_budget(team)
    club_dict = get_club_dict(instance)
    for player in team:
        club_dict[player.club] -= 1

    incumbent_solution = (team, calculate_score(team[:11]), calculate_budget(team))

    instance_sorted_by_points = sorted(instance, key=lambda x: x.points, reverse=True)

    tabu_list: List[Tuple[Player, int]] = []
    for player in instance_sorted_by_points:
        tabu_list.append((player, 0))

    gk_neighbourhood = generate_neighbourhood("GK", instance_sorted_by_points, 50)
    def_neighbourhood = generate_neighbourhood("DEF", instance_sorted_by_points, 50)
    mid_neighbourhood = generate_neighbourhood("MID", instance_sorted_by_points, 50)
    fw_neighbourhood = generate_neighbourhood("FW", instance_sorted_by_points, 50)

    neighborhoods_dict = {"GK": gk_neighbourhood, "DEF": def_neighbourhood, "MID": mid_neighbourhood,
                          "FW": fw_neighbourhood}

    solutions = [calculate_score(team[:11])]

    for _ in range(max_iter):

        starting_team = team[:11]
        neighborhood_scores = []
        for player in starting_team:

            neighbourhood = neighborhoods_dict[player.position]
            for neighbour in neighbourhood:

                if check_if_player_in_tabu(tabu_list, neighbour) or neighbour in team:
                    continue

                if (check_budget_constraint(100 - budget + player.price, neighbour.price)
                        and check_club_constraint(club_dict, neighbour.club, player.club)):
                    temp_team = team.copy()
                    temp_team[temp_team.index(player)] = neighbour
                    temp_team_score = calculate_score(temp_team[:11])
                    replaced_player_tuple = (player, neighbour)

                    neighborhood_scores.append((temp_team, temp_team_score, replaced_player_tuple))

        best_candidate_score, best_candidate_index = find_best_candidate_solution(neighborhood_scores)

        players_replaced = neighborhood_scores[best_candidate_index][2]

        team = neighborhood_scores[best_candidate_index][0]  # Candidate team

        solutions.append(calculate_score(team[:11]))

        incumbent_solution = update_solution(incumbent_solution, team)

        player = players_replaced[0]
        neighbour = players_replaced[1]
        club_dict[player.club] += 1
        club_dict[neighbour.club] -= 1
        budget += neighbour.price - player.price

        tabu_list = update_tabu_list(tabu_list, players_replaced, tabu_tenure)

    return incumbent_solution[0]


def update_tabu_list(tabu_list: List[Tuple[Player, int]], players_replaced: Tuple[Player, int],
                     tabu_tenure: int) -> List[Tuple[Player, int]]:
    for player, tenure in tabu_list:
        if player.player_id == players_replaced[0].player_id:
            tabu_list[tabu_list.index((player, tenure))] = (player, tabu_tenure)

        elif tenure > 0:
            tabu_list[tabu_list.index((player, tenure))] = (player, tenure - 1)

    return tabu_list


def check_if_player_in_tabu(tabu_list: List[Tuple[Player, int]], player: Player) -> bool:
    player_in_tabu = False
    for tabu_player, tenure in tabu_list:
        if tenure > 0 and tabu_player.player_id == player.player_id:
            player_in_tabu = True
            break

    return player_in_tabu


def find_best_candidate_solution(neighborhood_scores) -> Tuple[int, int]:
    best_candidate_score, best_candidate_index = float('-inf'), None

    for i, neighborhood_score in enumerate(neighborhood_scores):
        if neighborhood_score[1] > best_candidate_score:
            best_candidate_score = neighborhood_score[1]
            best_candidate_index = i

    return best_candidate_score, best_candidate_index


def update_solution(incumbent_solution, team):
    candidate_score = calculate_score(team[:11])
    if candidate_score > incumbent_solution[1]:
        incumbent_solution = (
            team, candidate_score, calculate_budget(team))  # Candidate team is better than incumbent team

    return incumbent_solution
