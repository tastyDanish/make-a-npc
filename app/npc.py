"""
Author: Peter Lansdaal
Date: 2018-11-20
"""
from app import random_weight


_base_stats = {'STR': 10, 'CON': 10, 'DEX': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
_stat_array = [15, 14, 13, 12, 10, 8]

_human_stats = {'STR': 10, 'CON': 10, 'DEX': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
_elf_stats = {'STR': 5, 'CON': 5, 'DEX': 20, 'INT': 20, 'WIS': 10, 'CHA': 10}
_race_stats = {'Elf': _elf_stats, 'Human': _human_stats}


class NPC:
    """
    Creates an NPC following the PC building rules
    """
    def __init__(self, name, race):
        self.name = name
        self.race = race
        self.stats = generate_stats(self.race)
        self.background = generate_background(self.race, self.stats)
        self.pc_class = generate_class(self.background, self.race, self.stats)


def generate_stats(race):
    """
    Generates stats for the character, rolling stats by their weights
    :param race:
    :type race:
    :return:
    :rtype:
    """
    my_stats = {}
    remove_stats = []
    for stat in _stat_array:
        chosen_stat = random_weight.roll_with_weights_removal(_race_stats[race], remove_stats)
        my_stats[chosen_stat] = stat
        remove_stats.append(chosen_stat)
    return my_stats


def generate_background(race, stats):
    return None


def generate_class(background, race, stats):
    return None


if __name__ == '__main__':
    print(generate_stats('Elf'))