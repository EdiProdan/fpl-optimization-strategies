from lab.fpl_optimization_strategies.algorithms.grasp import grasp
from lab.fpl_optimization_strategies.algorithms.greedy import greedy
from lab.fpl_optimization_strategies.algorithms.simulated_annealing import simulated_annealing
from lab.fpl_optimization_strategies.algorithms.tabu_search import tabu_search
from lab.fpl_optimization_strategies.utils import *

ALPHA_GREEDY = 0

if __name__ == "__main__":
    instance = ""
    player_list = read_instance("data/{}".format(instance))

    for player in player_list:
        player.points_per_price = player.points / player.price

    team_greedy = greedy(ALPHA_GREEDY, player_list, get_club_dict(player_list),
                         get_constraints("constraints.json")[1], get_constraints("constraints.json")[2],
                         get_constraints("constraints.json")[0])

    team_random = greedy(1, player_list, get_club_dict(player_list),
                         get_constraints("constraints.json")[1], get_constraints("constraints.json")[2],
                         get_constraints("constraints.json")[0])

    team_grasp = grasp(0.2, 10, player_list)

    team_ts_greedy = tabu_search(team_greedy, player_list, 10, max_iter=50)
    team_ts_random = tabu_search(team_random, player_list, 10, max_iter=50)

    team_sa_greedy = simulated_annealing(team_greedy, player_list, 600, temperature_decrement=0.99)
    team_sa_random = simulated_annealing(team_random, player_list, 600, temperature_decrement=0.99)
