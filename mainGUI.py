import customtkinter as ctk
from tkinter import ttk
import csv
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


PAGE_RANK_DELTA = 0.01


def graph_visualize(games: list, prs: dict, filename: str = "images/graph.png"):
    """
    Visualize a directed graph of tournaments, showing who won and who lost,
    with nodes colored based on the number of arrows going into them (in-degree),
    keeping the same hue but varying intensity.
    The graph is saved as a PNG image.
    :param rankings: dictionary where keys are players and values are their ranks (higher rank means higher skill).
    :param filename: The name of the file to save the image (default is 'graph.png').
    :returns: None
    """
    plt.close()
    plt.figure(figsize=(4, 4))
    G = nx.DiGraph()

    G.add_nodes_from(list(prs.keys()))
    G.add_edges_from(games)
    max_pr = max(prs.values())
    norm = mcolors.Normalize(vmin=0, vmax=max_pr)


    cmap = plt.cm.viridis_r
    # node_colors = [max(0.4, cmap(norm(prs[node]))) for node in G.nodes()]
    # node_colors = [(0.204, 0.153, 0.255, max(0.4, norm(prs[node]))) for node in G.nodes()]

    node_colors = []
    for node in G.nodes():
        rgba = list(cmap(norm(prs[node])))
        rgba[3] = min(0.6, rgba[3])
        node_colors.append(tuple(rgba))
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca(), fraction=0.03, pad=0.02)

    pos = nx.spring_layout(G, k=0.8, iterations=100)


    nx.draw_networkx_labels(G, pos, font_size=6, font_color=(0.204, 0.153, 0.255, 1), bbox=dict(facecolor="white", alpha=0.5))
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=1500, edge_color='gray', arrowsize=10)

    plt.savefig(filename, format="PNG")





#----------------PAGE RANK ALGHORITHM FUNCTIONS---------------#
# read_file                 52
# page_rank                 92
# sort_by_rank             118
# to_dict                  140
# get_tournaments_dict     163



def read_file(file_path: str) -> tuple[str, list[tuple[str, str]], list[tuple[str, str]]]:
    '''
    Read file with a tournament data and return a tuple with a tournament
    name, players information (their countries) and games results.

    :param file_path: str, a path to the file, where tournament data is
    stored.
    :return: tuple[str, list[tuple[str, str]], list[tuple[str, str]]],
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
    ind = True
    i = 1
    while ind:
        for key in graph:
            sum_ = sum((page_ranks[vertex][i-1]/len(graph[vertex][0]) for vertex in graph[key][1]))
            page_ranks[key] += [sum_]
        ind = False
        for player_page_rank in page_ranks.values():
            if abs(player_page_rank[-1] - player_page_rank[-2]) > PAGE_RANK_DELTA:
                ind = True
        i += 1
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



# ---------- UI TOOL FUNCTIONS --------------#
def clear_frame(frame):
    """
     Clears all widgets from a frame.

    This function iterates through all the widgets of the frame
    and destroys them.

    Parameters:
    frame (tk.Frame): The frame whose widgets will be cleared.

    Returns:
    None
    """
    for widget in frame.winfo_children():
        widget.destroy()

def show_graph():
    """
    Displays a graphical image in the application window.

    This function loads an image of a graph from the file path 'images/graph.png'
    and displays it as a label in the main application window. 

    Returns:
    None
    """
    global graph_label
    graph = Image.open('images/graph.png')
    graph_image = ctk.CTkImage(light_image= graph, size=(400, 400))
    
    graph_label = ctk.CTkLabel(master=root, image=graph_image, text='')
    graph_label.pack(pady=10, side='bottom')

def remove_graph():
    """
    Removes the displayed graph image from the application window.

    This function checks if the `graph_label` widget exists, and if so,
    destroys it to remove the graph image from the window.

    Returns:
    None
    """
    global graph_label
    if graph_label != None:
        graph_label.destroy()
        graph_label = None



# ------------UI WINDOW FUNCTIONS----------------#
def start_screen():
    """
    Initializes the start screen of the application.

    This function sets up the main interface for the user to select a file and start the PageRank algorithm.

    Returns:
    None
    """

    root.geometry("600x400")
    clear_frame(root)
    ctk.CTkLabel(root, text="Optimized tournament table\nChoose a file:", font=("Roboto", 24)).pack(pady=20)

    global file_menu
    file_menu = ctk.CTkOptionMenu(root, values=list(d.keys()))
    file_menu.pack(pady=10)

    ctk.CTkButton(root, text="START", command=main_screen).pack(pady=20)


def load_table_and_graph(file_path):
    '''
    Loads data from a file, processes it, and updates the tournament table and graph.

    This function:
    1. Clears the current table.
    2. Reads the tournament data from the provided file path.
    3. Processes the data to calculate player ranks using PageRank and visualizes the data as a graph.
    4. Saves the processed data to a CSV file (`tournament.csv`).
    5. Populates the table with data from the CSV file.
    6. Displays the graph on the UI.

    Parameters:
    file_path (str): Path to the file containing tournament data.

    Returns:
    None
    '''
    for row in table.get_children():
        table.delete(row)

    tournament_name, players_countries, games = read_file(file_path)
    dict_games = to_dict(games)
    raw_prs = page_rank(dict_games)
    global page_ranks
    page_ranks = sort_by_rank(raw_prs)

    graph_visualize(games, page_ranks)

    remove_graph()
    show_graph()

    with open('tournament.csv', 'w', encoding='utf-8') as file:
        file.write('Country,Name,PR,Raw Data\n')
        for name in page_ranks.keys():
            line = ','.join(map(str, [players_countries[name], name, page_ranks[name], round(raw_prs[name][-1], 3)]))
            file.write(line + '\n')

    with open('tournament.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            table.insert("", "end", values=row)



def main_screen():
    '''
    Initializes and displays the main screen of the application.

    Returns:
    None
    '''
    root.geometry("800x600")
    selected_file = d[file_menu.get()]
    clear_frame(root)
    style = ttk.Style()
    style.configure('Treeview', font=('Roboto', 14))


    global table
    table = ttk.Treeview(root, columns=("Country", "Name", "PR", "Raw Data"), show="headings")
    table.pack(fill="both", expand=False, padx=10, pady=10, side='left')
    table.column("Country", width=70)
    table.column("Name", width=300)
    table.column("PR", width=70)
    table.column("Raw Data", width=100)

    for col in ("Country", "Name", "PR", "Raw Data"):
        table.heading(col, text=col)

    global graph_label
    graph_label = None 

    load_table_and_graph(selected_file)
    ctk.CTkLabel(root, text="Choose another tournament:", font=("Roboto", 14)).pack(pady=5)
    switch_menu = ctk.CTkOptionMenu(root, values=list(d.keys()))
    switch_menu.pack(pady=10)
    ctk.CTkButton(root, text='Parse', command=lambda: load_table_and_graph(d[switch_menu.get()])).pack(pady=10, side='top')
    ctk.CTkButton(root, text="Back", command=start_screen).pack(pady=10)

def main():
    """
    The main function that runs the application.

    Returns:
    None
    """
    import doctest
    print(doctest.testmod())
    global tournaments
    tournaments = list(map(lambda x: 'tournaments/' + x, ['tournament_2.txt', 'tournament_3.txt', 'tournament_4.txt', 'tournament_5.txt', 'tournament_6.txt', 'tournament_7.txt']))
    global d
    d = get_tournaments_dict(tournaments)
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")
    global root
    root = ctk.CTk()
    root.title("PageRank")
    root.iconbitmap('images/graphimage.ico')
    root.resizable(True, True)
    start_screen()
    root.mainloop()

if __name__ == '__main__':
    main()
