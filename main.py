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
import customtkinter
from PIL import Image, ImageTk
# import tkinter as tk
from tkinter import ttk



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
            players[i] = (players_stats[i][-players_count - 4][:-1] + \
                          ' ' + players_stats[i][-players_count - 3], \
                            players_stats[i][-players_count - 1])
            games_results[i] = players_stats[i][-players_count:]
        games = []
        for i, player_games_results in enumerate(games_results):
            for j, game_result in enumerate(player_games_results):
                match game_result:
                    case '1':
                        games.append((players[i][0], players[j][0]))
                    case '½':
                        games.append((players[i][0], players[j][0]))
        return (tournament_name, dict(players), games)


def to_dict(games: list[tuple[str, str]]) -> dict[str, tuple[set[str], set[str]]]:
    '''
    Translate a list of games into a dictonary consisting of
    player names and two sets: to who did they lose and who
    did they overcome.

    :param games: list[tuple[str, str]], the list of tuples
    containing a winner and a loser of a game.
    :return: dict[str, tuple[set[str], set[str]]], the
    dictonary with wins and loses of every player.
    '''
    d = {}
    for v, u in games:
        if v not in d:
            d[v] = (set(), set())
        if u not in d:
            d[u] = (set(), set())
        d[v][1].add(u)
        d[u][0].add(v)
    return d



def get_tournaments_dict(tournament_file_paths_list: list[str]) -> dict[str, str]:
    '''
    Get the dictonary, where the key is a tournament name
    and country, and the value is a tournament file path.

    :param tournament_file_paths_list: list[str], the list of
    all the file paths containing tournamnt information
    :return: dict[str, str], a dictonary,
    where the key is a tournament name, and
    the value is a tournament file path
    '''
    d = {}
    for file_path in tournament_file_paths_list:
        with open(file_path, 'r', encoding='utf-8') as file:
            tournament_name = file.readline().strip()
            d[tournament_name] = file_path
    return d


# d = {
#     'A': ({'B', 'C'}, {'C'}),
#     'B': ({'D'}, {'A', 'C'}),
#     'D': ({'C'}, {'B', 'C'}),
#     'C': ({'A', 'B', 'D'}, {'A', 'D'})
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
    {'C': 4, 'D': 3, 'B': 2, 'A': 1}
    '''
    items = sorted(bench.items(), key=lambda x: -x[-1][-1])
    dt = {item[0]: len(items) - i + 1 for i, item in enumerate(items, 1)}
    return dt
def main():
    '''
    Main function
    '''
    mas = ['tournament_2.txt']
    d = get_tournaments_dict(mas)
    print(d)
    for key_, value_ in d.items():
        print()
        tournament_name, players, games = read_file(value_)
        print(tournament_name)
        for player in players:
            print(player)
        games = to_dict(games)
        players_page_rank = page_rank(games)
        for i in players_page_rank.items():
            print(i)
        players_page_rank = sort_by_rank(players_page_rank)
        for i in players_page_rank.items():
            print(i)


# main()

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x400")
root.title("PageRank")
root.resizable(False, False)


frame = customtkinter.CTkFrame(master=root, width=500, height=300)
frame.pack(pady=20, padx=20, fill="both")

label_1 = customtkinter.CTkLabel(master = frame, text="PageRank", font=('Roboto', 44))
label_1.pack(pady=12, padx=10)
label_2 = customtkinter.CTkLabel(master = frame, text="Оптимізована турнірна таблиця", font=('Roboto', 24))
label_2.pack(pady=2, padx=10)
label_3 = customtkinter.CTkLabel(master = frame, text="Chess Tournament", text_color="blue", font=('Roboto', 30))
label_3.pack(pady=2, padx=10)
label_4 = customtkinter.CTkLabel(master = frame, text="Оберіть турнір", font=('Roboto', 24))
label_4.pack(pady=16, padx=10)


def to_table(raw_prs: dict, page_ranks: dict, players_countries: dict) -> None:
    with open('tournament.csv', 'w', encoding='utf-8') as file:
        for name in page_ranks.keys():
            line = ','.join(map(str, [players_countries[name], name, page_ranks[name], round(raw_prs[name][-1], 3)]))
            file.write(line + '\n')

def clear_frame(frame):
    for widget in frame.winfo_children():
        if widget != optio_1 and widget != button_1 and widget != label_2 and widget != label_3 and widget != label_4:
            widget.destroy()

        



def start_button():
    file_path = d[optio_1.get()]
    tournament_name, players_countries, games = read_file(file_path)
    games = to_dict(games)
    raw_prs = page_rank(games)
    page_ranks = sort_by_rank(raw_prs)

    to_table(raw_prs, page_ranks, players_countries)

    clear_frame(frame)

    table.heading('Country', text="Country")
    table.heading('Name', text="Name")
    table.heading('PR', text="PR")
    table.heading('Raw', text="Data")
    table.pack( fill='both', expand=True)

    for row in table.get_children():
        table.delete(row)
    for n, name in enumerate(page_ranks.keys()):
        line = list(map(str, [players_countries[name], name, page_ranks[name], round(raw_prs[name][-1], 3)]))
        table.insert(parent='', index=n, values= line)

table = ttk.Treeview(root, columns=('Country', 'Name', 'PR', 'Raw'), show="headings")


mas = ['tournament_2.txt', 'tournament_3.txt', 'tournament_4.txt']
d = get_tournaments_dict(mas)

optio_1 = customtkinter.CTkOptionMenu(master=frame, values=list(d.keys()))
optio_1.pack(pady=10)
button_1 = customtkinter.CTkButton(master=frame, text="START",
                                    width=200, height=40,
                                    command=start_button, corner_radius=50)
button_1.pack(pady=20)

def graph_image():
    pass

root.mainloop()
if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
