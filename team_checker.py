import requests, traceback, re, getpass

#Hardcode team-id login (login is equivelent to email) field for future . Never hardcode password.
credentials = {'password':None,
               'login': None,
               'redirect_uri': 'https://fantasy.premierleague.com/a/login',
               'app': 'plfpl-web'
               }

team_id = None

#Only ask for validation if team_id, email and password havn't been set
if team_id == None or credentials['login'] == None:
    while True:
        print ("Enter team ID: ", end = '')
        team_id = input()
        try:
            int(team_id)
        except:
            print("Your game id is an all integer code")
            continue
        
        print ("Email: ", end = '')
        email = input()
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match == None:
            print('Bad email please re-enter')
            continue
        credentials['login'] = email

        print ("Password: ", end = '')
        credentials['password'] = getpass.getpass()
        break

#getpass method stops password echoing in terminal, menaing it remains hidden. 
else:
    print ("Password: ", end = '')
    credentials['password'] = getpass.getpass()

#Bootstrap API
bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
get_data_bootstrap = requests.get(bootstrap_url).json()

#Establish session
session = requests.session()
session.post('https://users.premierleague.com/accounts/login/', data=credentials)

#Team API
team_api = 'https://fantasy.premierleague.com/api/my-team/%s/' % (team_id)
get_data_team = session.get(team_api).json()

team = []
status = []
sp = ' '

for i in range(len(get_data_team['picks'])):
    player_id = get_data_team['picks'][i]['element']
    multiplier = get_data_team['picks'][i]['multiplier']
    vice_captain = get_data_team['picks'][i]['is_vice_captain']
    position = get_data_team['picks'][i]['position']

    if multiplier == 2:
        player_status = "(C)"
    elif multiplier == 3:
        player_status = "(TC)"
    elif vice_captain == True:
        player_status = "(VC)"
    elif multiplier == 0:
        player_status = "(Bench)"
    else:
        player_status = ""

    team.append(player_id)
    status.append(player_status)

print()   
print ("\n" + sp*44 + "+/-" + sp*4 + "Chance")
print ("Name" + sp*32 + "Price" + sp*3 + "(GW)" + sp*3 + "NextGW" + sp*3 + "News\n")

for i in range(len(team)):
    id = team[i]
    player_status = status[i]
    for i in range(len(get_data_bootstrap['elements'])):
        if get_data_bootstrap['elements'][i]['id'] == id:
            name = get_data_bootstrap['elements'][i]['web_name']
            price = get_data_bootstrap['elements'][i]['now_cost'] / 10
            price_change = get_data_bootstrap['elements'][i]['cost_change_event'] / 10
            next_round = get_data_bootstrap['elements'][i]['chance_of_playing_next_round']
            if next_round == None:
                next_round = 100
            news = get_data_bootstrap['elements'][i]['news']

            print("%-25s %-9s %-7.1f %-6.1f %-8d %s" %
                (name, player_status, price, price_change, next_round, news))

print()



