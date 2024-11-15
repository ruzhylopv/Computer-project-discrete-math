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


def read_file():
    # (['s', 'ds', 'dh ff', 'kjscha'], [('a', 'b'), ('c', 'd')]
    pass

def to_dict():
    pass


d = {
    'A': ({'B', 'C'}, {'C'}),
    'B': ({'D'}, {'A', 'C'}),
    'D': ({'C'}, {'B', 'C'}),
    'C': ({'A', 'B', 'D'}, {'A', 'D'})
}

len(d['A'])
def page_rank(graph: dict) -> dict[str, int]:

    page_ranks = {key: [1/len(graph)] for key in graph}
    # page_ranks = {list(graph.keys())[i]: [] for i in range(len(graph))}

    # for key in page_ranks:
    #     page_ranks[key] = [1/len(graph)]
    
    # for key in graph:
    #     for vertex in graph[key][1]:
    #         page_ranks[key] = page_ranks[vertex]
    return page_ranks

print(page_rank(d))

