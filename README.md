# ЗВІТ ДО КОМП'ЮТЕРНОГО ПРОЕКТУ 
#### p.s модуль знаходиться в файлі mainGUI.py
# БІБЛІОТЕКИ
```import customtkinter as ctk
from tkinter import ttk
import csv
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
```
## •	networkx 
– це бібліотека для створення, обробки й візуалізації графів (мереж)
ЇЇ основні властивості полягають в :
Створенні графів:
1.	Підтримка як неорієнтованих, так і орієнтованих графів
2.	Робота з ваговими графами (кожному ребру можна призначити "вагу")
3.	Створення мультиграфів (декілька ребер між одними й тими ж вершинами
4.	Імпортування графів із файлів (наприклад, .gml, .graphml, .adjlist, .edgelist)

Модифікація графів:
1.	Додавання/видалення вузлів і ребер
G.add_node(1) – додає один вузол
G.add_nodes_from([2, 3, 4, 5]) = додає кілька вузлів
G.remove_node(5) – видаляє вузол
pos = nx.spring_layout(G, k=0.8, iterations=100) – розсташування 
G.add_edge(1, 2) – одне ребро
G.add_edges_from([(2, 3), (3, 4), (4, 5), (5, 1)]) – кілька ребер
G.remove_edge(1, 2) – видаляє ребро

2.	Зміна атрибутів вузлів або ребер (назви, ваги, кольори тощо)
G.add_node(1, color='red', weight=5) – додати атрибут до вузла
G.add_edge(1, 2, weight=3, label='A') – додати атрибут до ребра
3.	Об'єднання, злиття графів або отримання їх підграфів

## •	matplotlib.pyplot 
– бібліотека для створення графіків і візуалізацій
## •	matplotlib.colors 
– модуль для роботи з кольорами, зокрема нормалізації значень для призначення кольорів.
## •	customkinter
 – кастомізована обгортка для tkinter, стандартної бібліотеки для створення GUI (графічних інтерфейсів користувача) у Python. Вона додає сучасний вигляд і стилізацію до інтерфейсу, дозволяючи створювати теми, кастомізовані елементи управління ( кнопки, меню, етикетки та інше)

Використання у коді:
CTk() створює головне вікно програми
CTkLabel, CTkButton, CTkOptionMenu — сучасні аналоги елементів управління tkinter
set_appearance_mode() дозволяє задавати світлу чи темну тему
set_default_color_theme() — налаштування кольорової схеми
## •	ttk 
є частиною стандартної бібліотеки tkinter і надає елементи управління, що підтримують стилізацію.
Використання у коді:
Treeview використовується для створення таблиць (наприклад, для відображення результатів турніру).
Налаштування стилю (ttk.Style()) застосовується до таблиці для коректного відображення тексту.
## •	Csv
використовується для читання та запису даних у форматі CSV. У коді записується таблиця турніру у файл tournament.csv.
## •	PIL
Підключено для роботи з зображеннями. В коді використовується для відкриття зображення графу (Image.open()), яке згодом виводиться у графічному інтерфейсі.

# ВИКОРИСТАНІ ПРИНЦИПИ ДИСКРЕТНОЇ МАТЕМАТИКИ
1) Поняття вершин і ребер
2) Поняття орієнтованого графа (DiGraph)

Використання функцій бібліотеки networkx для роботи з орієнтованими графами, таких як add_edges_from та spring_layout, дозволяє візуалізувати і аналізувати структуру взаємозв'язків між гравцями.
Побудова візуалізації з використанням кольору для позначення властивостей графів (наприклад, рейтингу гравців).

# АЛГОРИТМ PAGERANK

## Мета алгоритму:
Алгоритм PageRank в цьому коді використовується для визначення відносної важливості гравців у турнірі на основі результатів матчів. Ранжування ґрунтується на графовому поданні перемог і поразок між гравцями.

## Основні етапи роботи алгоритму:
1. Зчитування даних турніру:
Дані про турнір представлені у вигляді текстового файлу з турнірною таблицею і результатами кожної гри.
Функція get_tournaments_dict() повертає словник, де ключі це назви турнірів, а значення, це шляхи до файлів з інформацією про турнір.
Функція read_file() повертає кортеж з даними про турнір:
•   Назва турніру.
•   Список гравців так їхніх країн.
•   Список пар переможець/переможений.

2. Перетворення даних у граф:
Дані про матчі представлені як список пар переможець/переможений (`games`).
Використовується функція to_dict() для створення словника, де кожен гравець має два набори:
•	Множина суперників, яких він переміг.
•	Множина суперників, від яких зазнав поразки.

3. Ітеративне обчислення PageRank:
•	Алгоритм реалізовано у функції page_rank(graph).
•	Початковий рейтинг всіх гравців ініціалізується рівним значенням 1/N, де N- кількість гравців
•	Ітеративне обчислення відбувається допоки максимальна абсолютна різниця пейдж ранків між попередньою та даною ітерацією не буде менша або рівна заданому
параметру, в даному випадку 0.01.
•	На кожній ітерації PageRank гравця обчислюється як сума внесків від його суперників, які на попередній ітерації поділили свій поточний рейтинг між усіма переможцями, від яких вони програли.

4. Сортування за рейтингом:
•	Функція sort_by_rank() упорядковує гравців за їхніми остаточними значеннями PageRank.
•	Результати подаються у вигляді словника, де ключ — ім'я гравця, а значення — його позиція у рейтингу.

5. Візуалізація графу:
•	Вузли графу (гравці) забарвлюються на основі їхніх PageRank значень: вищий рейтинг відповідає яскравішим вузлам.
•	Візуалізація здійснюється через бібліотеку networkx із використанням спрямованого графу (DiGraph).


## Застосування результатів:
•	Алгоритм PageRank дозволяє автоматично ранжувати гравців за їхнім впливом у турнірі.

•	Результати виводяться у вигляді таблиці та графу, що робить аналіз зрозумілим і наочним.


# ІМПЛЕМЕНТАЦІЯ АЛГОРИТМУ У КОДІ
## Алгоритм процедури:

1) Видалення старих даних із таблиці.
2) Читання нового файлу даних турніру.
3) Перетворення даних у формат для графа.
4) Обчислення рангів PageRank для гравців.
5) Побудова та збереження графа у вигляді зображення.
6) Оновлення графічного інтерфейсу для відображення нового графа.
7) Експорт результатів у CSV.
8) Вивід результатів у таблицю для користувача.
## Основні етапи алгоритму
1) Зчитування даних турніру із файлу.
Перетворення даних у структуру графа:
Гравці — це вузли графа.
Матчі — це спрямовані ребра між вузлами.
2)Обчислення PageRank для кожного гравця:
3)Алгоритм виконує кілька ітерацій, поки різниця між результатами ітерацій не стане меншою за заданий поріг (PAGE_RANK_DELTA).
4)Сортування гравців за їхніми фінальними рангами.
Візуалізація графа:
5)Вузли графа фарбуються відповідно до їхнього рейтингу.
6)Результати відображаються у графічному інтерфейсі.
Експорт результатів у CSV-файл.

## Основні функції:

```graph_visualize(): Створює графічну візуалізацію результатів турніру
read_file(): Зчитує дані турніру з текстового файлу
page_rank(): Реалізує алгоритм PageRank
sort_by_rank(): Ранжує гравців за оцінками PageRank
to_dict(): Перетворює результати ігор на словник 
```
## Функція read_file читає файл з інформацією про турнір:
1)Назва турніру.
2) Дані про гравців та їх країни.
3) Результати ігор у форматі списку перемог і поразок.

## Як це працює:

1) Зчитує перший рядок файлу як назву турніру.
2) Пропускає зайві рядки, які не містять корисної інформації.
3) Виділяє блок даних про гравців та результати матчів.
4) Перетворює дані у формат, який зручно використовувати для побудови графа:
players: список гравців із зазначенням їхніх країн.
games: список матчів у форматі ("гравець_переможець", "гравець_програвший").
```
tournament_name, players_countries, games = read_file(file_path)
```

## Функція to_dict створює словник, де кожен гравець пов’язаний з:
1) Гравцями, яких він переміг.
2) Гравцями, від яких він програв.

```
dict_games = to_dict(games)
```
## Як це працює:

Для кожного матчу додається зв'язок між переможцем та тим, хто програв.
Створюється словник такого формату:

```
{
    "гравець_А": ({"переміг_Б", "переміг_С"}, {"програв_Д"}),
    "гравець_Б": ({"переміг_Д"}, {"програв_А"}),
    ...
}
```

## Обчислення PageRank
```raw_prs = page_rank(dict_games)
global page_ranks
page_ranks = sort_by_rank(raw_prs)
```

1) page_rank: Обчислює вагу (ранг) кожного гравця на основі взаємозв'язків у графі.
2) sort_by_rank: Сортує гравців за їхнім фінальним рангом.

Як це працює:

Останнє значення кожного гравця у списку рангів береться за основу для сортування.

Створюється новий словник, де кожному гравцю привласнюється його позиція у рейтингу
```
{
    "гравець_С": 1,  # найвищий ранг
    "гравець_Д": 2,
    ...
}
```

## Візуалізація графа
```
graph_visualize(games, page_ranks)
```
Створює зображення графа, де вузли представляють гравців, а ребра – їх взаємодії (хто кого переміг).

## Як це працює:

Побудова графа:
Вузли — це гравці.
Ребра — це результати матчів.
Колір вузлів:
Колір залежить від рангу гравця (більш високий ранг = більш насичений колір).
Розташування вузлів:
Використовується метод spring_layout, який імітує розташування вузлів як у пружній системі.
Збереження графа:
Граф зберігається як зображення PNG.

## Оновлення візуального елемента графа
```
remove_graph()
show_graph()
```
Видаляє попередній граф із вікна і додає новий.

## Експорт результатів у файл

```
with open('tournament.csv', 'w', encoding='utf-8') as file:
    file.write('Country,Name,PR,Raw Data\n')
    for name in page_ranks.keys():
        line = ','.join(map(str, [players_countries[name], name, page_ranks[name], round(raw_prs[name][-1], 3)]))
        file.write(line + '\n')
```
Записує результати в CSV-файл, включаючи:
1) Країну гравця.
2) Ім'я.
3) PageRank


## Додавання даних до таблиці
```
with open('tournament.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Пропускає заголовки
    for row in reader:
        table.insert("", "end", values=row)
```

# РОЗПОДІЛ РОБОТИ
1) Павло Ружило - ініціатор та розробник  алгоритму, допомога з UI процесами
2) Цибрівський Олександр - аналітик з обробки даних, розробник алгоритму
3) Мандрик Софія - робота з візуалізацією графів, написання звіту
4) Довбенчук Олена - робота з UI, розробка презентації
5) Мацелюх Максим - робота з UI

# ВРАЖЕННЯ ВІД ВИКОНАННЯ ПРОЕКТУ/ФІДБЕК:
Павло: 

"So far цей проєкт був найкрутішим з усіх курсів в 1 семестрі! Часом навіть ловив себе на тому, що хотілось робити швидше його, aніж будь-яке інше завдання. Дав змогу ознайомитись одразу з кількома корисними бібліотеками, пізнати новий алгоритм та підтягнути навички роботи в команді з GitHub."

Софія: 

"Проект дав змогу ще раз попрактикувати навички роботи в команді, поєднюючи у собі практику з програмування та дискретної математики одночасно! Робота з новим алгоритмом дуже зацікавила! Дякую за таку перфект можливість нашим викладачам та асистентці, всі поради були справді корисними!"

Олександр:

"Цей проєкт удосконалив наші уміння використовувати систему контролю версій. 
Було дуже цікаво вивчити досить важливий алгоритм і реалізувати його в коді"

Олена:

"Це був справді корисний командний проєкт, який допоміг краще закріпити знання з дискретної математики. Особливо він допоміг краще розібратися з темою графів, також було дуже корисно розробити один з алгоритмів та надати йому практичного застосування. Ще одним важливим аспектом варто зазначити роботу з UI це розширило мої знання на невідомому мені раніше полі, що потім неодмінно буде корисним, тому добре, що ми навчились використовувати це саме зараз."

Максим:

"Новий досвід - завджи супер! "