
from productivity import Productivity

import os
import string
import random
import json
import codecs
import argparse

# This class is used to generate a Paranoia character
class ParanoiaCharacterGenerator:
    # String used for the data file name, we insert the selected language string in the middle.
    data_file_prefix = "paranoia_data_"
    data_file_extension = ".json"

    # English/French words I swap based on the language parameter. Search for them it's pretty obvious.
    # This should be adjusted (or removed) if more languages are added. Or added in the data file?
    purpose = "Purpose"
    purpose_fr = "Objectif"
    warning = "Warning"
    warning_fr = "Avertissement"


    # Parameters:
    # language: 'F' for French, 'E' for English
    # sex: 'M' for male, 'F' for female
    def __init__(self, language='ENG', sex='M', seed_name="", debug = False ):
        self.language = language
        self.sex = sex
        self.debug = debug
        self.name = seed_name
        self.service_group = ""
        self.service_group_description = ""
        self.mutations = []
        self.button_treason = ""
        self.button_violence = ""
        self.productivity = Productivity()
        self.secret_society = ""
        self.secret_society_description = ""
        self.output_file = ""

        if self.language == "FRA":
            self.purpose = self.purpose_fr
            self.warning = self.warning_fr


        # Load language specific data file based on received language parameter used in file name
        self.data_file_name = self.data_file_prefix + language + self.data_file_extension

        if not os.path.exists(self.data_file_name):
            print("Error: Data file not found: " + self.data_file_name)
            exit()

        # Read with codecs to handle UTF-8 (french accents in the file)
        with codecs.open(self.data_file_name, 'r', encoding='utf-8') as file:
            self.json_data = json.load(file)

        self.trace("Loaded data file: " + self.data_file_name)

    # Centralize the trace output when the 'debug' parameter is set
    def trace(self, txt):
        if self.debug:
            print(txt)

    # Used to centralize the console output, useful to output to file and console at the same time
    def console(self, txt):
        if self.output_file != "":
            with codecs.open(self.output_file, 'a', encoding='utf-8') as file:
                file.write(txt + '\n')
        print(txt)
            
    #
    # MAIN FUNCTION - just acall the other functions one by one to generate the character
    #
    def generate_character(self):
        # Generate a complete character with all attributes
        # The 'steps' are based on The Core Book 'build a character' instructions.

        self.trace( "# Step-A" )
        self.generate_name()
        self.generate_service_group()
        self.generate_button_treason()
        self.generate_button_violence()

        self.trace( "# Step-B" )
        self.generate_productivity_profile()

        self.trace( "# Step-C" )
        self.generate_secret_society() # Also applies the modifiers to the productivity profile
        self.generate_mutant_power()
        
        # Step-D
        # 8 Moxies, 200XP, Wound, Flags, Red laser pistol, Red reflect armour.

    # Generate a random name for the character. 
    # Will use a seed name if one was given, otherwise will generate a random name from list in the JSON file.
    # The security level R is added and then the sector (3 random letters).
    def generate_name(self):
        # Generate a random name for the character

        # Skip random name selection if user already set a predefined name
        if self.name is None or self.name == "":
            name_key = "Names M"
            if self.sex is "F":
                name_key = "Names F"

            name_list = self.json_data[name_key]
            self.name = str(random.choice(name_list))
            
        # Add security level
        self.name += "-"
        self.name += "R" # Alwasy RED for now
        self.name += "-"
        
        # Add the sector
        self.name += self.generate_sector()
        ze_this = "Name: " + self.name
        self.trace( "Name: " + self.name)

    # Generate a random sector composed of 3 random upper case characters
    def generate_sector(self):
        zetree = random.choices(string.ascii_uppercase, k=3)
        return ''.join(zetree)

    # Select a 'service group' at random from the dictionary in the JSON data file.
    def generate_service_group(self):
        # Read the "Secret Society" data from the JSON file
        service_group_data = self.json_data["Service Groups"]

        # Generate a random secret society for the character
        self.service_group = random.choice(list(service_group_data.keys()))
        self.trace( "Service Group: " + self.service_group)

        # Retrieve the "Purpose" element from the retrieved key
        self.service_group_description = service_group_data[self.service_group]["Purpose"]
        self.trace(" - " + self.purpose + ": " + self.service_group_description)

        # Get the keys and data following the "Purpose" key
        for key, value in service_group_data[self.service_group].items():
            if key != "Purpose":
                self.trace(" - Adjusting " + key + ": " + str(value))
                self.productivity.adjust_skill(key, value)

    # Print the service group information to the console
    def print_service_group(self):
        self.console( "Service Group: " + self.service_group)
        self.console(" - " + self.purpose + ": " + self.service_group_description)


    # select a 'treason button' at random from the dictionary in the JSON file.
    def generate_button_treason(self):
        treason_buttons = self.json_data["Treason Buttons"]
        self.button_treason = random.choice(list(treason_buttons))
        self.trace( "Treason Button: " + self.button_treason)

    # select a 'violence button' at random from the dictionary.
    def generate_button_violence(self):
        violence_buttons = self.json_data["Violence Buttons"]
        self.button_violence = random.choice(violence_buttons)
        self.trace( "Violence Button: " + self.button_violence)


    # Generate the characters stats (Productivity Profile)
    def generate_productivity_profile(self):
        # Generate a random number of skill points for the character
        self.productivity.generate_random_productivity()
        if self.debug:
            self.trace( "Productivity: " )
            self.productivity.pretty_print(self.language)

    # Generate the 'Secret Society' at random from the dictionary in the JSON file.
    def generate_secret_society(self):
        # Read the "Secret Society" data from the JSON file
        secret_society_data = self.json_data["Secret Societies"]
        
        # Generate a random secret society for the character
        self.secret_society = random.choice(list(secret_society_data.keys()))
        self.trace( "Secret Society: " + self.secret_society)

        # Retrieve the "Purpose" element from the retrieved key
        self.secret_society_description = secret_society_data[self.secret_society]["Purpose"]
        self.trace(" - Purpose: " + self.secret_society_description)

        # Get the keys and data following the "Purpose" key
        for key, value in secret_society_data[self.secret_society].items():
            if key != "Purpose":
                self.trace(" - Adjusting " + key + ": " + str(value))
                self.productivity.adjust_skill(key, value)

    def print_secret_society(self):
        if self.language == "FRA":
            self.console( "Société Secrète: " + self.secret_society)
        else:
            self.console( "Secret Society: " + self.secret_society)

        self.console(" - " + self.purpose + ": " + self.secret_society_description)                


    # Select a 'Mutation' at random from the data file.
    def generate_mutant_power(self):
        # load mutant powers JSON data:
        mutant_power_data = self.json_data["Mutant Powers"]

        self.mutations = self.mutant_power_data = random.choice(list(mutant_power_data.keys()))
        self.mutations_purpose = mutant_power_data[self.mutations]["Purpose"]
        self.mutations_warning = mutant_power_data[self.mutations]["Warning"]

        self.trace(self.mutations + ": " + self.mutations_purpose + " - " + self.mutations_warning)

    def print_mutations(self):
        self.console( "Mutation: " + self.mutations)
        self.console( " - " + self.purpose + ": " + self.mutations_purpose)
        self.console( " - " + self.warning + ": " + self.mutations_warning)

    def print_character(self):
        # Print the character's attributes
        if self.language == "FRA":
            self.console(' -- Générateur de personnage pour PARANOIA "The Perfect Edition" (2023) --')
        else:
            self.console(' -- Character generator for PARANOIA "The Perfect Edition" (2023) --')
        self.console("Name: " + self.name)

        self.print_service_group()
        self.console("")
        
        if self.language == "FRA":
            self.console("Bouton de Trahison: " + self.button_treason)
            self.console("Bouton de Violence: " + self.button_violence)
            self.console("Profil de productivité:")
        else:
            self.console("Treason Button: " + self.button_treason)
            self.console("Violence Button: " + self.button_violence)
            self.console("Productivity Profile:")
        
        self.console( self.productivity.pretty_print(self.language) )

        if self.language == "FRA":
            self.console( "\nVous avez: 8 Moxies, 200XP, un pistolet laser rouge et une armure réfléchissante rouge.")
            self.console(" --- Côté caché ---")
        else:
            self.console( "\nYou also have: 8 Moxies, 200XP, a red laser pistol and a red reflect armour.")
            self.console("\n --- Naughty Side ---")

        
        self.print_secret_society()
        self.console("")
        self.print_mutations()

        self.console("-----------------------------------------------------\n" )


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Paranoia Character Generator")

    # Add arguments
    parser.add_argument("-s", "--sex", choices=["M", "F"], default="M", help="Specify the character sex (for name selection) (default: M)")
    parser.add_argument("-l", "--language", default="ENG", help="Specify the language (default: ENG)")
    parser.add_argument("-n", "--name", default="", help="(Optional) Specify the character name. Sector and Security color is added automatically.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode for additional trace information")
# Option removed for online web service.    
#    parser.add_argument("-f", "--file", help="Specify a file name to save/append the console output to.", default="")
    parser.add_argument("-b", "--number", type=int, default=1, help="Specify the number of characters to generate (default: 1)")

    # Parse the command line arguments
    args = parser.parse_args()
    
    for _ in range(args.number):
        generator = ParanoiaCharacterGenerator(args.language, args.sex, args.name)
        generator.debug = args.debug
        #generator.output_file = args.file
        generator.generate_character()
        generator.print_character()



if __name__ == "__main__":
    main()
