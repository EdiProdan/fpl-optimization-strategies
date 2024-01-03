from lab.fpl_optimization_strategies.constraints import *
from lab.fpl_optimization_strategies.algorithms.greedy import greedy
from lab.fpl_optimization_strategies.utils import calculate_score, calculate_budget, get_club_dict, get_constraints, generate_neighbourhood


def grasp(alpha: float, max_iterations: int, instance: List[Player]) -> List[Player]:
    best_solution = 0
    best_team = []

    for i in range(max_iterations):
        (max_number_per_position_dict, starting_11_min_dict,
         starting_11_max_per_position_dict) = get_constraints("constraints.json")

        club_dict = get_club_dict(instance)
        team = greedy(alpha, instance, club_dict, starting_11_min_dict, starting_11_max_per_position_dict,
                      max_number_per_position_dict)

        optimized_team = local_search(team, instance, club_dict)
        optimized_team_score = calculate_score(optimized_team[:11])

        if optimized_team_score > best_solution:
            best_solution = optimized_team_score
            best_team = optimized_team

    return best_team


def local_search(team: List[Player], instance: List[Player], club_dict: dict) -> List[Player]:
    starting_team = team[:11]
    previous_score = calculate_score(starting_team)
    budget = calculate_budget(team)
    instance_sorted_by_points = sorted(instance, key=lambda x: x.points, reverse=True)
    instance_sorted_by_price_ascending = sorted(instance, key=lambda x: x.price)
    while True:
        for player in starting_team:
            neighbourhood = generate_neighbourhood(player.position, instance_sorted_by_points, 10)
            for neighbour in neighbourhood:
                if neighbour.points > player.points:
                    if (neighbour not in team
                            and check_budget_constraint(100 - budget + player.price, neighbour.price)
                            and check_club_constraint(club_dict, neighbour.club, player.club)):
                        club_dict[player.club] += 1
                        club_dict[neighbour.club] -= 1
                        index = team.index(player)
                        team[index] = neighbour
                        budget += neighbour.price - player.price
                        break

        current_score = calculate_score(starting_team)

        for player in team[11:]:
            neighbourhood = generate_neighbourhood(player.position, instance_sorted_by_price_ascending, 10)
            for neighbour in neighbourhood:
                if neighbour.price < player.price:
                    if (neighbour not in team
                            and check_budget_constraint(100 - budget + player.price, neighbour.price)
                            and check_club_constraint(club_dict, neighbour.club, player.club)):
                        club_dict[player.club] += 1
                        club_dict[neighbour.club] -= 1
                        index = team.index(player)
                        team[index] = neighbour
                        budget += neighbour.price - player.price
                        break

        if current_score > previous_score:
            previous_score = current_score
        else:
            break
    return team
