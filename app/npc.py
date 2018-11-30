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
_human_class = {'Barbarian': 10, 'Bard': 10,  'Cleric': 10, 'Druid': 10, 'Fighter': 10, 'Monk': 10, 'Paladin': 10,
                'Ranger': 10, 'Rogue': 10, 'Sorcerer': 10, 'Warlock': 10, 'Wizard': 10}

_elf_stats = {'STR': 5, 'CON': 5, 'DEX': 20, 'INT': 20, 'WIS': 10, 'CHA': 10}
_elf_bonus = {'DEX': 2, 'INT': 1}
_elf_back = {'Soldier': 5, 'Acolyte': 10, 'Hermit': 15, 'Sage': 20, 'Criminal': 10, 'Artisan': 10}
_elf_class = {'Barbarian': 5, 'Bard': 5,  'Cleric': 10, 'Druid': 15, 'Fighter': 5, 'Monk': 5, 'Paladin': 10,
                'Ranger': 20, 'Rogue': 15, 'Sorcerer': 10, 'Warlock': 5, 'Wizard': 20}

_race_stats = {'Elf': _elf_stats, 'Human': _human_stats}
_race_bonus = {'Elf': _elf_bonus, 'Human': _human_bonus}
_race_back = {'Elf': _elf_back, 'Human': _human_back}

_stat_backs = {'STR': ['Soldier', 'Acolyte'],
               'DEX': ['Hermit', 'Criminal'],
               'INT': ['Sage', 'Artisan'],
               'WIS': ['Acolyte', 'Sage'],
               'CHA': ['Criminal', 'Artisan'],
               'CON': ['Soldier', 'Hermit']}



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
        """
        Generates a background based on the race and stats of the NPC
        :return: the background
        :rtype: str
        """
        high_stat = self.get_highest_stat()
        low_stat = self.get_lowest_stat()
        back_dict = _race_back[self.race].copy()
        for h_stat in high_stat:
            if h_stat in _stat_backs.keys():
                for back in _stat_backs[h_stat]:
                    back_dict[back] = back_dict[back] + 10

        for l_stat in low_stat:
            if l_stat in _stat_backs.keys():
                for back in _stat_backs[l_stat]:
                    back_dict[back] = back_dict[back] - 10
                    if back_dict[back] < 0:
                        back_dict[back] = 0

        return random_weight.roll_with_weights(back_dict)

    def generate_class(self):


    def generate_skills(self):
        return 123


if __name__ == '__main__':
    my_npc = NPC('Gringle', 'Elf')
    print(my_npc.stats)
    print(my_npc.background)
