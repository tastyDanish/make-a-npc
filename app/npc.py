"""
Author: Peter Lansdaal
Date: 2018-11-20
"""
from app import random_weight


_base_stats = {'STR': 10, 'CON': 10, 'DEX': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
_stat_array = [15, 14, 13, 12, 10, 8]

_human_stats = {'STR': 10, 'CON': 10, 'DEX': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
_human_bonus = {'STR': 1}
_human_back = {'Soldier': 10, 'Acolyte': 10, 'Hermit': 10, 'Sage': 10}

_elf_stats = {'STR': 5, 'CON': 5, 'DEX': 20, 'INT': 20, 'WIS': 10, 'CHA': 10}
_elf_bonus = {'DEX': 2, 'INT': 1}
_elf_back = {'Soldier': 10, 'Acolyte': 10, 'Hermit': 10, 'Sage': 10}

_race_stats = {'Elf': _elf_stats, 'Human': _human_stats}
_race_bonus = {'Elf': _elf_bonus, 'Human': _human_bonus}
_race_back = {'Elf': _elf_back, 'Human': _human_back}

class NPC:
    """
    Creates an NPC following the PC building rules
    """
    def __init__(self, name, race):
        self.name = name
        self.race = race
        self.stats = self.generate_stats()
        self.background = self.generate_background()
        self.pc_class = self.generate_class()
        self.skills = self.generate_skills()

    def get_highest_stat(self):
        """
        Gives you a list of the highest stats. Generally this is a single value, but sometimes its two or more!
        :return: the highest stats
        :rtype: list
        """
        highest = 0
        big_stat = []
        for stat, value in self.stats.items():
            if value > highest:
                highest = value
                big_stat = [stat]
            elif value == highest:
                big_stat.append(stat)
        return big_stat

    def get_lowest_stat(self):
        """
        Gives you a list of the lowest stats. Generally this is one, but it could be more!
        :return: the lowest score
        :rtype: list
        """
        lowest = 100
        small_stat = []
        for stat, value in self.stats.items():
            if value < lowest:
                lowest = value
                small_stat = [stat]
            elif value == lowest:
                small_stat.append(stat)
        return small_stat

    def generate_stats(self):
        """
        Generates stats for the character, rolling stats by their weights
        :return: a stat array for the character
        :rtype: dict
        """
        my_stats = {}
        remove_stats = []
        for stat in _stat_array:
            chosen_stat = random_weight.roll_with_weights_removal(_race_stats[self.race], remove_stats)
            my_stats[chosen_stat] = stat
            remove_stats.append(chosen_stat)
        for bonus, value in _race_bonus[self.race].items():
            my_stats[bonus] = my_stats[bonus] + value
        return my_stats

    def generate_background(self):
        return 123

    def generate_class(self):
        return 123

    def generate_skills(self):
        return 123


if __name__ == '__main__':
    my_npc = NPC('Gringle', 'Elf')
    print(my_npc.stats)
    print(my_npc.get_highest_stat())
    print(my_npc.get_lowest_stat())
