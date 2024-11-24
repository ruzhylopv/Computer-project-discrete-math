# white = []
# black = []
# with open('Computer-project-discrete-math/DEM-Meisterturnier Runden 1-3 (1).pgn', encoding='utf-8') as file:
#     for line in file:
#         if '[White "' in line:
#             white.append(line)
#         elif '[Black "' in line:
#             black.append(line)
# print(white)
# print(black)


def read_file(file_path: str) -> tuple[str, list[tuple[str, str]], list[tuple[str, str]]]:
    '''
    Read file with a tournament data and return a tuple with a tournament
    name, players information and games results.

    :param file_path: str, a path to the file, where tournament data is
    stored.
    :return: tuple[str, list[tuple[str, str]], list[tuple[str, str]]],
    a tuple with a tournament name the players info and the games results,
    in the format of tuples, where the first element is a winner, and the
    second, a loser.
    '''
    # (['s', 'ds', 'dh ff', 'kjscha'], [('a', 'b'), ('c', 'd')])
    with open(file_path, 'r', encoding='utf-8') as file:
        tournament_name = file.readline().strip()
        file.readline()
        file.readline()
        tournament_table_head = file.readline().strip().split()
        points_pos = tournament_table_head.index('Pts.') - len(tournament_table_head)
        players_stats = file.read().strip().split('\n')
        players_count = len(players_stats)
        players = [0] * players_count
        games_results = [0] * players_count
        for i, val in enumerate(players_stats):
            players_stats[i] = val.split()[:points_pos]
            players[i] = (players_stats[i][-players_count - 4][:-1] + ' ' + players_stats[i][-players_count - 3], players_stats[i][-players_count - 1])
            games_results[i] = players_stats[i][-players_count:]
        games = []
        for i, player_games_results in enumerate(games_results):
            for j, game_result in enumerate(player_games_results):
                match game_result:
                    case '1':
                        games.append((players[i][0], players[j][0]))
                    case '½':
                        games.append((players[i][0], players[j][0]))
        return (tournament_name, players, games)


for i in read_file('tournament_2.txt'):
    print(i)


def to_dict():


d = {
    'A': ({'B', 'C'}, {'C'}),
    'B': ({'D'}, {'A', 'C'}),
    'D': ({'C'}, {'B', 'C'}),
    'C': ({'A', 'B', 'D'}, {'A', 'D'})
}

len(d['A'])
def page_rank(graph: dict) -> dict[str, list[int]]:
    '''
    Finds a page rank of 2 iterations of teams given as a dictionary
    as a param graph.
    Returns a dictionary where each key is a name of a team, and
    each corresponding value is a list of page ranks of each iteration.
    >>> d = {
    ...     'A': ({'B', 'C'}, {'C'}),
    ...     'B': ({'D'}, {'A', 'C'}),
    ...     'D': ({'C'}, {'B', 'C'}),
    ...     'C': ({'A', 'B', 'D'}, {'A', 'D'})
    ... }
    >>> page_rank(d)
    {'A': [0.25, 0.08333333333333333, 0.125], \
'B': [0.25, 0.20833333333333331, 0.16666666666666666], \
'D': [0.25, 0.3333333333333333, 0.3333333333333333], \
'C': [0.25, 0.375, 0.375]}
    '''
    page_ranks = {key: [1/len(graph)] for key in graph}
    for i in range(1, 3):
        for key in graph:
            sum_ = sum((page_ranks[vertex][i-1]/len(graph[vertex][0]) for vertex in graph[key][1]))
            page_ranks[key] += [sum_]
    return page_ranks

def sort_by_rank(bench: dict) -> dict[str, int]:
    '''
    Sorts a dictionary with benchmarks (return of page_rank function).
    Returns a dictionary with each team as a key and each value is a page rank
    in comparison to every other team. The higher the rank, the more 'important'
    each team is.
    :param bench: dict, the dictionary with data from all iterations.
    :return: dict[str, int]
    >>> d = {
    ...     'A': ({'B', 'C'}, {'C'}),
    ...     'B': ({'D'}, {'A', 'C'}),
    ...     'D': ({'C'}, {'B', 'C'}),
    ...     'C': ({'A', 'B', 'D'}, {'A', 'D'})
    ... }
    >>> ranks = page_rank(d)
    >>> sort_by_rank(ranks)
    {'A': 1, 'B': 2, 'D': 3, 'C': 4}
    '''
    items = sorted(bench.items(), key=lambda x: x[-1][-1])
    dt = {item[0]: i for i, item in enumerate(items, 1)}
    return dt

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
