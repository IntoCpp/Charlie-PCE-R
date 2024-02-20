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

   print("Character generated, vcall hello page with name: " + pcg.name + " and sex: " + pcg.sex)
   return render_template(
      'hello.html', 
      name = pcg.name, 
      service = pcg.service_group, 
      service_desc = pcg.service_group_description,
      btn_treason = pcg.button_treason, 
      btn_violence = pcg.button_violence)


if __name__ == '__main__':
   app.run()
