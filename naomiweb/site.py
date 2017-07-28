from bottle import route, run, template, static_file, error, request, view, redirect
from gevent import monkey; monkey.patch_all()
from time import sleep
import os
import string
import configparser
from naomigame import *
from loadgame import *

PREFS_FILE = "settings.cfg"
prefs = configparser.ConfigParser()

loadingjob = job(1, 1)

def build_games_list():
    games = []
    games_directory = prefs['Games']['directory'] or 'games'

    print("Looking for NAOMI games...")

    if os.path.isdir(games_directory):
        for filename in os.listdir(games_directory):
            filename = games_directory + '/' + filename
            print(filename)
            if(is_naomi_game(filename)):
                game = NAOMIGame(filename)
                games.append(game)

        return games

    else:
        return None

@route('/')
def index():
    some_games = build_games_list()
    region = prefs['Games']['region'].lower() or 'japan'
    
    if some_games != None:
        return template('index', games=some_games, region=region)
    else:
        return template('index')


@route('/load/<hashid:int>')
def load(hashid):
    global loadingjob
    
    if loadingjob is not None and not loadingjob.finished():
        return "Error: A game is currently being loaded! Try again later"
        
    some_games = build_games_list()
    selected_game = None
    for game in some_games:
        if game.__hash__() == hashid:
            selected_game = game
            break
            
    if (selected_game is None):
    	return "Unable to find" + str(hashid) + '!'
    	
    loadingjob = job(selected_game, prefs)
    loadingjob.start()
    # does not work with safari
    yield "Loading: " + selected_game.name['japan'] + \
          '<br>0---------------------------100%<br>'
    while not loadingjob.finished(): # to be tested without arcade cabinet (fake job)
        yield '...'
        sleep(1)
                
    #yield "<br><p>BACK TO GAMES LIST<p>"
    yield "<br><a href=\"/\">BACK TO GAMES LIST</a>"
    #redirect('/') does not work due to previous yield
    
@route('/config', method='GET')
def config():
    network_ip = prefs['Network']['ip'] or '192.168.0.10'
    network_subnet = prefs['Network']['subnet'] or '255.255.255.0'
    games_directory = prefs['Games']['directory'] or 'games'
    games_region = prefs['Games']['region'].lower() or 'japan'

    return template('config', network_ip=network_ip, network_subnet=network_subnet, games_directory=games_directory, games_region=games_region)

@route('/config', method='POST')
def do_config():
    network_ip = request.forms.get('network_ip')
    network_subnet = request.forms.get('network_subnet')
    games_directory = request.forms.get('games_directory')
    games_region = request.forms.get('selRegion')

    prefs['Network']['ip'] = network_ip
    prefs['Network']['subnet'] = network_subnet
    prefs['Games']['directory'] = games_directory
    prefs['Games']['region'] = games_region
    with open(PREFS_FILE, 'w') as prefs_file:
        prefs.write(prefs_file)

    return template('config', network_ip=network_ip, network_subnet=network_subnet, games_directory=games_directory, games_region=games_region, did_config=True)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, 'static')

@error(404)
def error404(error):
    return '<p>Error: 404</p>'

prefs_file = open(PREFS_FILE, 'r')
prefs.read_file(prefs_file)
prefs_file.close()

run(host='0.0.0.0', port=8000, debug=True)
