import pandas as pd
import random
import re


class Door:
    def __init__(self, name):
        self.name = name
        self.door_bounty = 0
        self.door_closed = 1
        self.door_player = 0
        self.door_status = name + ': 🕸 🚪 🪑'

    def put_bounty(self):
        self.door_bounty = 1
        self.door_status = self.door_status.replace('🕸', '💎')

    def put_player(self):
        self.door_player = 1
        self.door_status = self.door_status.replace('🪑', '🏃‍♂️')

    def open_door(self):
        self.door_closed = 0
        self.door_status = self.door_status.replace('🚪', '👀')

    def del_player(self):
        self.door_player = 0
        self.door_status = self.door_status.replace('🏃‍♂️', '🚪')

    def __repr__(self):
        return f'{self.door_status}'


class MontyHallShow:
    doors = None
    first_choice = None
    second_choice = None

    def m_get_closed_doors(self):
        return [d for d in self.doors if str(d).count('🚪') == 1]

    def m_put_bounty_behind_a_door(self):
        self.bounty_door = random.choice(self.doors)
        self.bounty_door.put_bounty()

    def m_choose_door(self):
        if not self.first_choice:
            self.first_choice = random.choice(self.m_get_closed_doors())
            self.first_choice.put_player()
        else:
            self.second_choice = random.choice(self.m_get_closed_doors())
            self.second_choice.put_player()
            if self.second_choice != self.first_choice:
                self.first_choice.del_player()

    def m_monty_reveal_door(self):
        random.choice([d for d in self.m_get_closed_doors() if str(d).count('💎') == 0 and str(d).count('🏃‍♂️') == 0]).open_door()

    def m_snapshot1(self):
        self.snapshot1 = '     '.join([str(d) for d in self.doors])

    def m_snapshot2(self):
        self.snapshot2 = '     '.join([str(d) for d in self.doors])

    def m_snapshot3(self):
        self.snapshot3 = '     '.join([str(d) for d in self.doors])


def simulation(repetitions=10, verbose=0):
    games = {}
    for i in range(repetitions):
        # monty hall game game:
        game = MontyHallShow()
        d1, d2, d3 = Door('Door1'), Door('Door2'), Door('Door3')
        game.doors = [d1, d2, d3]
        game.m_put_bounty_behind_a_door()

        # player makes first choice:
        game.m_choose_door()
        game.m_snapshot1()
        # monty reveals a door with no prize behind:
        game.m_monty_reveal_door()
        game.m_snapshot2()
        # player makes second choice:
        game.m_choose_door()
        game.m_snapshot3()

        player_switched = 0 if game.first_choice == game.second_choice else 1
        player_won = 1 if game.second_choice == game.bounty_door else 0

        games[f'game {i}'] = {'Player switched the door': player_switched, 'Times player won': player_won}

        if verbose and i < 10:
            print(fr'''
______________
round {i} starts\____________________________________________________
{game.snapshot1}

monty reveals
{game.snapshot2}

{'player switched' if player_switched else 'player stayed'}
{game.snapshot3}
{'player won' if player_won else 'player lost'}
''')
    print('\n', pd.DataFrame(pd.DataFrame(games).T.groupby(['Player switched the door'])['Times player won'].sum()))


simulation(repetitions=300, verbose=1)
