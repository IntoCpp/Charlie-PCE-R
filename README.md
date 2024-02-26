# Paranoia Character Creator - 'perfect edition' (2023)

## Introduction

This web service is based on a script I use to generate characters with random characteristics for the RPG game PARANOIA. All the online generators I found was for older version of Paranoia. The main goal of this project was to publish a web service as fast as possible while I had no knowledge on how to do such things. In my free time. So yeah, things are little rough on the edges, and is very basic.

As of this writing you can find the online service at: https://charlie-r-pce.azurewebsites.net/

Some delays may occur due to Azure 'free' services, the page can take a minute or two to show up.

**PLEASE** visit [Mongoose Publishing - Paranoia page](https://www.mongoosepublishing.com/collections/paranoia) for any information about the game. You will not learn much about the game here. Paranoia is an underated RPG that did not get published enough in the last 25+ years. Please support them to get things going :)


## Character generation - how it's done

It is based on 'The Core Book' (TCB), (Mongoose Publishing/2023) description of how to create characters (Pages 20–25). Obviously, it replaces all human actions in the creation by a random decision from The Friend Computer. So this is great for NPC or first time player to gain a little time by just giving them pre-made characters.

The nomenclature used here (and in Python code) is from the book.

Here is the rundown of the algorithm to give you an idea of what is going on.

1. Generate a name (M or F) and append "-R-" and a random sector.
2. Random a Service Group: The 'Purpose' is also added.
3. Random a Treason Button.
4. Random a Violence Button.
5. Generate the productivity profile (skills and stats). This follows the rules, but without the human interactions. So:
   - Each -5 to +5 is distributed randomly to stats, except for guns (always +2). The ones left are kept at zero.
   - Skills are then calculated from the statistics. I.e: the sum of their stats. Note that **stats** are adjusted later based on the characters Service Group and Secret Society. **Warning:** The **skills** are not recalculated after those **stats** change, since there is no mention that it should be done in TCB. I.e., the skills are only calculated once, after the statistical distribution, and never later.
6. Random a Secret Society: The purpose of the Secret Society is added.
7. Random a Mutant Power: The purpose and warning (bad effect) of the mutation are added.

All of that is then printed on the screen. A set of data exists in French for the "FRA" option. Translation done mostly using 'DeepL Translate' that I can recommend.

## More options and customization
The things described here could be added in this service with a pull request. Or on your PC if you just clone the repo and use the 'paranoia.py' scripts from the command line. 

(This following is from my original Python doc)

A great fun of the game is how it keeps things simple, fast, and let you do all sorts of crazy stuff. And that includes coming up with your own mutant powers, buttons and secret society. The book often says,  "suggested list of...". Mongoos Publishing is comming out with more of them soon I read.

I made sure to place all those in a dedicated file that follows the YAML format, which is easy to read, modify and has a simple structure. The code simply looks for the main item name and iterate thru them to select one.

Just open it and add your own ideas. I do recommend googling "YML validator" and paste the entire file in there when you are done. Structural errors in the file are not fun to fix by calling the script.

> [!WARNING] do not change the keys used in code. "Purpose", "Warning" for example or all the skills and stats name ("Brain", "Bluff", etc.) In doubt, search the code and if it is used don't change the name.

The options you can easily change are:
- Secret Societies
- Service Groups
- Mutant Powers
- Treason Buttons
- Violence Buttons
- Names M: for a male
- Names F: for a female

### Customizing the language

You will find two files here:
- paranoia_data_ENG.yml with English description.
- paranoia_data_FRA.yml with French description.

You can copy one and create your own version in another own language. Just use the 3 characters in the "--language" parameter to use it.


# paranoia.py details

Follows under here the original script I did to create characters for my games. 
### How to use it (Security Level: Yellow)


# References
As mentioned in the introduction, this project was done as a way to study how easy it was to quickly publish a simple web service on a web page, using the Python script I made to generate the characters for my games (in a private repo, copied in this one).

After a little research I went with Azure ... for no other reason than it is used by various professionals around me. 

The rest of this page contains notes and references I saved on this page while developing.

## So Azure, how was it?
I was pleasantly surprised at the overall ease of use. The only issue I had was to deploy. 

The first deploy pipeline has a delay from 15 minutes to over 45 minutes. This made me believe the problem was me, so I reset and retried several times, just to return later and "Hey! It works. What happened?"Same thing on the second run, but it was still not working after 45 min. I called it quits and next morning it was there, working on the Azure site.

# Developement notes and references
The rest of this file is not very interesting. It contains notes I used for the creation of this project.

# Deploy a Python (Flask) web app to Azure App Service - Sample Application

This is the sample Flask application for the Azure Quickstart [Deploy a Python (Django or Flask) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python). For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:

* Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
* FastAPI [https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).

## First run
From that tutorial, the first local test was done by: 

``` Commad Line
py -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
flask run
```
"Browse to the sample application at http://localhost:5000 in a web browser."

## Production
* I'm using the GitHub project: https://github.com/IntoCpp/Charlie-PCE-R branch: **main**
* In my local folder <code-root>\Code\Charlie-PCE-R
    * To run locally, run from that folder DOS commend-line:
    ``` 
    .venv\scripts\activate
    flask run
    ```
* On Azzure: Charlie-R-PCE 
* With the final page : https://charlie-r-pce.azurewebsites.net/ 

## Workflow: 
* Do the developement on branch **devel**
* Approuved PR goes into the branch **test** and is deployed on the test system.
* If tests passes a PR is made in the main branch. 

Overkill? For this project certainly. But that's part of me learning how to do these things in Azure. 
In reality I code and push to the test branch and havent merged in production as of this writing.

## Test Dev - branch 'devel'
Azure have 'deployment slots' that let you create devel, test, production, (or whatever you name them) deployments. 
But that is a paying service. 
And since I'm still under the 30 day evaluation, I simple created a second project with the dployment pointing to the test branch instead of the main. I will most probably have deleteed it by the time anyone reads this.
* On Azzure: Charlie-R-PCE branch test
* With the final page : https://charlie-r-test.azurewebsites.net/  


