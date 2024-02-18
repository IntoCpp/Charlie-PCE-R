import random
from itertools import islice

class Productivity:
    def __init__(self):
        # First item is the 'stats', the others are the skills
        # look function set_stats where the stats are hard-coded.
        self.brains = {"Brains": 0, "Alpha Complex": 0, "Bureaucracy": 0, "Psychology": 0, "Science": 0 }
        self.chutzpah = {"Chutzpah": 0, "Bluff": 0, "Charm": 0, "Intimidate": 0, "Stealth": 0 }
        self.mechanics = {"Mechanics": 0, "Demolitions": 0, "Engineer": 0, "Operate": 0, "Program": 0 }
        self.violence = {"Violence": 0, "Athletics": 0, "Guns": 2, "Melee": 0, "Throw": 0 }

    def generate_random_productivity(self):
        # Generate a random array of stats
        random_stats = self.generate_random_array()
        
        # Fill skills with a set of random skill values (1 to 5 or -1 to -5)
        self.set_skils(random_stats)
        
        # Once the skills set we can calculate the skill stats (brains, chutzpah, mechanics, violence)
        self.set_stats()

    def generate_random_array(self):
        
        # First we randomize the order of the stats 1-16
        random_numbers = random.sample(range(15), 15) # array of 15 unique random numbers

        # then we fill an array with the +/- stats using the random positions.
        random_stats = [0] * 15 # array of 15 numbers all set to 0
        random_stats[random_numbers[0]] = 1
        random_stats[random_numbers[1]] = -1
        random_stats[random_numbers[2]] = 2
        random_stats[random_numbers[3]] = -2
        random_stats[random_numbers[4]] = 3
        random_stats[random_numbers[5]] = -3
        random_stats[random_numbers[6]] = 4
        random_stats[random_numbers[7]] = -4
        random_stats[random_numbers[8]] = 5
        random_stats[random_numbers[9]] = -5

        # Now 'stats' is an array of 15 numbers, where 10 of them is a stat from 1 to 5 or -1 to -5 
        # placed at random in the array. The others stauy at zero.

        return random_stats

    def set_skils(self, random_stats):
        # Fill the each stats with a set of random stats
        i = 0
        for key in islice(self.brains, 1, None): # set the 4 'brains' stats
            self.brains[key] = random_stats[i]
            i = i+1
        for key in islice(self.chutzpah, 1, None): # set the 4 'chutzpah' stats
            self.chutzpah[key] = random_stats[i]
            i = i+1
        for key in islice(self.mechanics, 1, None):# set the 4 'mechanics' stats
            self.mechanics[key] = random_stats[i]
            i = i+1

        for key in islice(self.violence, 1, None): # set the 4 'violence' stats
            if key != "Guns": # Skip Guns that must stay at 2.
                self.violence[key] = random_stats[i]
                i = i+1 

    def set_stats(self):            
        # Set the Brains, Chutzpah, Mechanics and Violence stats by counting the number of items >0 in each category
        count = 0
        for key in self.brains:
            if self.brains[key] > 0:
                count += 1
        self.brains["Brains"] = count

        count = 0
        for key in self.chutzpah:
            if self.chutzpah[key] > 0:
                count += 1
        self.chutzpah["Chutzpah"] = count

        count = 0
        for key in self.mechanics:
            if self.mechanics[key] > 0:
                count += 1
        self.mechanics["Mechanics"] = count

        count = 0
        for key in self.violence:
            if self.violence[key] > 0:
                count += 1
        self.violence["Violence"] = count

    def adjust_skill(self, skill, value):
        # Adjust the skill by the given value, make sure it stays in the [-5:5] range
        if skill in self.brains:
            self.brains[skill] = max(min(self.brains[skill] + value, 5), -5)
        elif skill in self.chutzpah:
            self.chutzpah[skill] = max(min(self.chutzpah[skill] + value, 5), -5)
        elif skill in self.mechanics:
            self.mechanics[skill] = max(min(self.mechanics[skill] + value, 5), -5)
        elif skill in self.violence:
            self.violence[skill] = max(min(self.violence[skill] + value, 5), -5)
        else:
            raise ValueError("Invalid skill: " + skill)
        
    def get_profile(self):
        # Print the character's attributes
        profile = "\t"
        profile += str(self.brains) + "\n\t"
        profile += str(self.chutzpah) + "\n\t"
        profile += str(self.mechanics) + "\n\t"
        profile += str(self.violence) + "\n"
        return profile

    def pretty_print(self, language):
        # Print the character's attributes
        ret = ""
        if language == "FRA":
            ret += "- Profil de Productivité -\n"
        else:
            ret += "- Productivity Profile -\n"
        ret = self.get_profile()
        return ret


            
