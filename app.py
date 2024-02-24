import os

from paranoia import ParanoiaCharacterGenerator

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   lang = request.form.get('language')
   sexu = request.form.get('sex')

   print( "generating characte with params: " + lang + " and " + sexu)
   pcg = ParanoiaCharacterGenerator(language=lang, sex=sexu)
   pcg.generate_character()

   print("Character generated, calling hello page")
   #
   # DEBUG: To see the generated character in the generator:
   # pcg.print_character()

   return render_template(
      'hello.html', 
      name = pcg.name, 
      service = pcg.service_group, 
      service_desc = pcg.service_group_description,
      btn_treason = pcg.button_treason, 
      btn_violence = pcg.button_violence, 

      Brains = pcg.productivity.brains["Brains"],
      Chutzpah = pcg.productivity.chutzpah["Chutzpah"],
      Mechanics = pcg.productivity.mechanics["Mechanics"],
      Violence = pcg.productivity.violence["Violence"], 

      Alpha = pcg.productivity.brains["Alpha Complex"],
      Bluff = pcg.productivity.chutzpah["Bluff"],
      Demolition = pcg.productivity.mechanics["Demolitions"],
      Athletics = pcg.productivity.violence["Athletics"], 

      Bureaucracy = pcg.productivity.brains["Bureaucracy"],
      Charm = pcg.productivity.chutzpah["Charm"],
      Engineer = pcg.productivity.mechanics["Engineer"],
      Guns = pcg.productivity.violence["Guns"],

      Psychology = pcg.productivity.brains["Psychology"],
      Intimidate = pcg.productivity.chutzpah["Intimidate"],
      Operate = pcg.productivity.mechanics["Operate"],
      Melee = pcg.productivity.violence["Melee"],

      Science = pcg.productivity.brains["Science"],
      Stealth = pcg.productivity.chutzpah["Stealth"],
      Program = pcg.productivity.mechanics["Program"],
      Throw = pcg.productivity.violence["Throw"], 

      Secret = pcg.secret_society, 
      Secret_desc = pcg.secret_society_description,
      Mutant = pcg.mutations,
      Mutant_purpose = pcg.mutations_purpose,
      Mutant_warning = pcg.mutations_warning
      )
      


if __name__ == '__main__':
   app.run()
