from otree.api import *
import random
from django.http import JsonResponse


class C(BaseConstants):
    NAME_IN_URL = 'mazes'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    maze1 = models.IntegerField(label="First Maze")
    maze2 = models.IntegerField(label="Second Maze")
    maze3 = models.IntegerField(label="Third Maze")
    type_of_learning1 = models.StringField(label="First Type of Learning")
    type_of_learning2 = models.StringField(label="Second Type of Learning")
    type_of_learning3 = models.StringField(label="Third Type of Learning")
    timestamp_start = models.FloatField()
    timestamp_end = models.FloatField()
    gave_up = models.BooleanField(initial=False)

    # current position
    pos_row = models.IntegerField(initial=0)
    pos_col = models.IntegerField(initial=4)


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.vars['maze_order'] = random.sample([1, 2, 3], k=3)
            p.participant.vars['learning_type'] = random.sample([1, 2, 3], k=3)

def load_maze(maze_number):
    maze1 = [
        ['#', '#', '#', '#', 'S', '#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', ' ', '#', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#'],
        ['#', '#', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#', '#'],
        ['#', ' ', ' ', '#', '#', '#', '#', '#', '#', ' ', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', 'E', '#', '#', '#', '#']
    ]

    maze2 = [
        ['#', '#', '#', '#', 'S', '#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', '#', '#', ' ', '#', ' ', '#', '#', ' ', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', '#'],
        ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', '#', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', '#', '#', ' ', '#', ' ', '#', '#'],
        ['#', '#', '#', '#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'E', '#']
    ]

    maze3 = [
        ['#', '#', '#', '#', 'S', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', '#', '#'],
        ['#', ' ', '#', '#', ' ', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', ' ', '#', '#', ' ', '#', ' ', ' ', ' ', '#', '#', '#'],
        ['#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#'],
        ['#', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#'],
        ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', '#', 'E', '#', '#', '#', '#', '#', '#', '#', '#']
    ]

    mazes = [maze1, maze2, maze3]

    return mazes[maze_number - 1]

def load_type_of_learning(learning_num):
    types_of_learning = ['No Cue', 'Auditory', 'Visual']
    return types_of_learning[learning_num - 1]

def print_maze(maze):
    s = [[str(e) for e in row] for row in maze]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))

# PAGES
class Maze(Page):
    form_model = 'player'
    form_fields = ['timestamp_start', 'timestamp_end', 'gave_up']

    @staticmethod
    def live_method(player, data):
        """
        data = {
            'move': 'up'/'down'/'left'/'right'
        }
        """
        maze = load_maze(player.participant.vars['maze_order'][player.round_number - 1])
        printable_maze = maze
        r, c = player.pos_row, player.pos_col
        move = data['move']
        print(move)
        print(player.id_in_group)
        printable_maze[r][c] = '@'

        dr = dc = 0
        if move == 'up': dr = -1
        elif move == 'down': dr = 1
        elif move == 'left': dc = -1
        elif move == 'right': dc = 1

        new_r = r + dr
        new_c = c + dc

        # check bounds
        if not (0 <= new_r < len(maze)) or not (0 <= new_c < len(maze[0])):
            return {player.id_in_group: {'status': 'wall'}}

        cell = maze[new_r][new_c]

        if cell == '#':
            print_maze(printable_maze)
            return {player.id_in_group: {'status': 'wall'}}
        else:
            # valid move
            printable_maze[player.pos_row][player.pos_col] = ' '
            if player.pos_row == 0 and player.pos_col == 4:
                printable_maze[player.pos_row][player.pos_col] = 'S'
            player.pos_row = new_r
            player.pos_col = new_c
            printable_maze[player.pos_row][player.pos_col] = '@'
            print_maze(printable_maze)
            if cell == 'E':
                return {player.id_in_group: {'status': 'finished'}}
            return {player.id_in_group: {'status': 'moved'}}

    @staticmethod
    def vars_for_template(player):
        maze_number = player.participant.vars['maze_order'][player.round_number - 1]
        maze = load_maze(maze_number)
        type_of_learning = load_type_of_learning(player.participant.vars['learning_type'][player.round_number - 1])
        if player.round_number == 1:
            player.maze1 = maze_number
            player.type_of_learning1 = type_of_learning
        elif player.round_number == 2:
            player.maze2 = maze_number
            player.type_of_learning2 = type_of_learning
        elif player.round_number == 3:
            player.maze3 = maze_number
            player.type_of_learning3 = type_of_learning

        return dict(type_of_learning=type_of_learning)
    

page_sequence = [Maze]
