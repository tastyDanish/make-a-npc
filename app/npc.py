"""
Author: Peter Lansdaal
Date: 2018-11-20
"""
from app import random_weight


_base_stats = {'STR': 10, 'CON': 10, 'DEX': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
_stat_array = [15, 14, 13, 12, 10, 8]

_human_stats = {'STR': 10, 'CON': 10, 'DEX': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
_human_back = {'Soldier': 10, 'Acolyte': 10, 'Hermit': 10, 'Sage': 10, 'Criminal': 10, 'Artisan': 10}
_human_class = {'Barbarian': 5, 'Bard': 5,  'Cleric': 5, 'Druid': 5, 'Fighter': 5, 'Monk': 5, 'Paladin': 5,
                'Ranger': 5, 'Rogue': 5, 'Sorcerer': 5, 'Warlock': 5, 'Wizard': 5}

_elf_stats = {'STR': 5, 'CON': 5, 'DEX': 10, 'INT': 10, 'WIS': 5, 'CHA': 5}
_elf_bonus = {'DEX': 2, 'INT': 1}
_elf_back = {'Soldier': 5, 'Acolyte': 5, 'Hermit': 10, 'Sage': 10, 'Criminal': 5, 'Artisan': 10}
_elf_class = {'Barbarian': 5, 'Bard': 5,  'Cleric': 5, 'Druid': 10, 'Fighter': 5, 'Monk': 5, 'Paladin': 5,
              'Ranger': 5, 'Rogue': 10, 'Sorcerer': 5, 'Warlock': 5, 'Wizard': 10}

_race_stats = {'Elf': _elf_stats, 'Human': _human_stats}
_race_bonus = {'Elf': _elf_bonus}
_race_back = {'Elf': _elf_back, 'Human': _human_back}
_race_class = {'Elf': _elf_class, 'Human': _human_class}

_stat_backs = {'STR': ['Soldier', 'Acolyte'],
               'DEX': ['Hermit', 'Criminal'],
               'INT': ['Sage', 'Artisan'],
               'WIS': ['Acolyte', 'Sage'],
               'CHA': ['Criminal', 'Artisan'],
               'CON': ['Soldier', 'Hermit']}

_stat_class = {'STR': ['Fighter', 'Paladin', 'Barbarian'],
               'DEX': ['Rogue', 'Ranger', 'Monk', 'Fighter'],
               'INT': ['Wizard'],
               'WIS': ['Cleric', 'Druid', 'Monk', 'Ranger'],
               'CHA': ['Warlock', 'Sorcerer', 'Bard', 'Paladin'],
               'CON': []}

_back_class = {'Soldier': ['Fighter', 'Barbarian'],
               'Acolyte': ['Cleric', 'Paladin', 'Monk'],
               'Hermit': ['Ranger', 'Ranger', 'Druid', 'Monk'],
               'Sage': ['Wizard'],
               'Criminal': ['Rogue', 'Warlock', 'Bard'],
               'Artisan': ['Bard']}


class NPC:
    """
    Creates an NPC following the PC building rules
    """
    def __init__(self, name, race, background=None, pc_class=None, top_stat=None):
        self.name = name
        self.race = race
        self.stats = self.generate_stats(top_stat)
        self.background = self.generate_background(background)
        self.pc_class = self.generate_class(pc_class)
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

    def generate_stats(self, top_stat=None):
        """
        Generates stats for the character, rolling stats by their weights
        :return: a stat array for the character
        :rtype: dict
        """
        my_stats = {}
        remove_stats = []
        for i, stat in enumerate(_stat_array):
            if i == 0 and top_stat is not None:
                chosen_stat = top_stat
            else:
                chosen_stat = random_weight.roll_with_weights_removal(_race_stats[self.race], remove_stats)
            my_stats[chosen_stat] = stat
            remove_stats.append(chosen_stat)
        if self.race == 'Human':
            first_high = 0
            first_stat = None
            second_high = 0
            second_stat = None
            for key, val in my_stats.items():
                if val % 2 == 1 and val > first_high:
                    first_high = val
                    first_stat = key
                elif val % 2 == 1 and val > second_high:
                    second_high = val
                    second_stat = key
            my_stats[first_stat] = my_stats[first_stat] + 1
            my_stats[second_stat] = my_stats[second_stat] + 1
        else:
            for bonus, value in _race_bonus[self.race].items():
                my_stats[bonus] = my_stats[bonus] + value
        return my_stats

    def generate_background(self, background=None):
        """
        Generates a background based on the race and stats of the NPC
        :return: the background
        :rtype: str
        """
        if background is not None:
            return background
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

    def generate_class(self, pc_class=None):
        """
        Generates the class of the NPC by building on the original weights
        :return:
        :rtype:
        """
        if pc_class is not None:
            return pc_class
        high_stat = self.get_highest_stat()
        low_stat = self.get_lowest_stat()
        class_dict = _race_class[self.race].copy()
        for h_stat in high_stat:
            if h_stat in _stat_class.keys():
                for pc_class in _stat_class[h_stat]:
                    class_dict[pc_class] = class_dict[pc_class] + 20

        for l_stat in low_stat:
            if l_stat in _stat_backs.keys():
                for pc_class in _stat_class[l_stat]:
                    class_dict[pc_class] = class_dict[pc_class] - 10
                    if class_dict[pc_class] < 0:
                        class_dict[pc_class] = 0

        for pc_class in _back_class[self.background]:
            class_dict[pc_class] = class_dict[pc_class] + 5
        print(class_dict)
        return random_weight.roll_with_weights(class_dict)

    def generate_skills(self):
        return 123


if __name__ == '__main__':
    my_npc = NPC('Gringle', 'Elf', pc_class='Wizard', top_stat='INT')
    print(my_npc.stats)
    print(my_npc.background)
    print(my_npc.pc_class)
