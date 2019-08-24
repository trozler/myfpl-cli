import requests, traceback, re, getpass

#Hardcode login (login is equivelent to email) field for future . Never hardcode password.
credentials = {'password':None,
               'login':None,
               'redirect_uri': 'https://fantasy.premierleague.com/a/login',
               'app': 'plfpl-web'
               }

#Set team_id for future use by changing None
team_id = None

#Only ask for validation if team_id, email and password havn't been set
if team_id == None or credentials['password'] == None or credentials['login'] == None:
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

#Bootstrap API
bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
get_data_bootstrap = requests.get(bootstrap_url).json()

#Establish session
session = requests.session()
session.post('https://users.premierleague.com/accounts/login/', data=credentials)

#Team API
team_api = 'https://fantasy.premierleague.com/api/my-team/%s/' % (team_id)
get_data_team = session.get(team_api).json()

#Rank section
entry_api = 'https://fantasy.premierleague.com/api/entry/%s/' % team_id
get_data_entry = session.get(entry_api).json()

#Transfer API
transfer_api = 'https://fantasy.premierleague.com/api/entry/%s/transfers-latest/' % (team_id)
get_transfer = session.get(transfer_api).json()

team = []
status = []
sp = ' '

def get_player_info(transfers:bool):
    
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
        elif position > 11:
            player_status = "(Bench)"
        else:
            player_status = ""

        team.append(player_id)
        status.append(player_status)

    if transfers:
        #replace transferd in players with transferd out
        for i in range(len(get_transfer)):
            player_out = get_transfer[i]['element_out']
            player_in = get_transfer[i]['element_in']
            team[team.index(player_in)] = player_out
        
    print ("\n" + sp*36 + "Points" + sp*11 + "+/-" + sp*4 + "Chance")
    print ("Name" + sp*32 + "(GW)" + sp*5 + "Price" + sp*3 + "(GW)" + sp*3 + "NextGW" + sp*3 + "News\n")

    for i in range(len(team)):
        id = team[i]
        player_status = status[i]
        for i in range(len(get_data_bootstrap['elements'])):
            if get_data_bootstrap['elements'][i]['id'] == id:
                name = get_data_bootstrap['elements'][i]['web_name']
                gw_points = get_data_bootstrap['elements'][i]['event_points']
                if player_status == "(C)":
                    gw_points *= 2
                elif player_status == "(TC)":
                    gw_points *= 3
                price = get_data_bootstrap['elements'][i]['now_cost'] / 10
                price_change = get_data_bootstrap['elements'][i]['cost_change_event'] / 10
                next_round = get_data_bootstrap['elements'][i]['chance_of_playing_next_round']
                if next_round == None:
                    next_round = 100
                news = get_data_bootstrap['elements'][i]['news']

                print("%-25s %-9s %-8d %-7.1f %-6.1f %-8d %s" %
                    (name, player_status, gw_points, price, price_change, next_round, news))

#If length is equal to 0 then no transfers we just enter regular flow
if (len(get_transfer) == 0):
    get_player_info(False)
else:
    get_player_info(True)

print ("\n\nGameweek points: %-7d\tOverall points: %-7d" %
    (get_data_entry["summary_event_points"], get_data_entry["summary_overall_points"]))

print ("Gameweek rank:   %-7s\tOverall rank:   %-7s\n" %
    (get_data_entry["summary_event_rank"], get_data_entry["summary_overall_rank"]))

print ("\nH2H Leagues:\n")
print (sp*40 + "Prev" + sp*7 + "Curr" + sp*7 + "Rank" + sp*8 + "Leader")
print ("League Name" + sp*29 + "Rank" + sp*7 + "Rank" + sp*7 + "Diff\n")

for i in range(len(get_data_entry['leagues']['h2h'])):
    league_id = get_data_entry['leagues']['h2h'][i]['id']
    league_name = get_data_entry['leagues']['h2h'][i]['name']
    previous_rank = get_data_entry['leagues']['h2h'][i]['entry_last_rank']
    current_rank = get_data_entry['leagues']['h2h'][i]['entry_rank']
    rank_difference = get_data_entry['leagues']['h2h'][i]['entry_last_rank'] - current_rank

    league_api = 'https://fantasy.premierleague.com/api/leagues-h2h/%s/standings/' % league_id
    get_data_league = session.get(league_api).json()
    league_leader = get_data_league['standings']['results'][0]['total']
    point_differential = league_leader - get_data_league['standings']['results'][current_rank - 1]['total']

    print ("%-39s %-10d %-10d %-11d %d (%d)" %
        (league_name, previous_rank, current_rank, rank_difference, league_leader, point_differential))

print ("\n\nClassic Leagues:\n")
print (sp*40 + "Prev" + sp*7 + "Curr" + sp*7 + "Rank" + sp*8 + "Leader")
print ("League Name" + sp*29 + "Rank" + sp*7 + "Rank" + sp*7 + "Diff" + sp*8 + "Points\n")

for i in range (len(get_data_entry['leagues']['classic'])):
    league_id = get_data_entry['leagues']['classic'][i]['id']
    league_name = get_data_entry['leagues']['classic'][i]['name']
    previous_rank = get_data_entry['leagues']['classic'][i]['entry_last_rank']
    current_rank = get_data_entry['leagues']['classic'][i]["entry_rank"]
    rank_difference = previous_rank - current_rank

    league_api = 'https://fantasy.premierleague.com/api/leagues-classic/%s/standings/' % league_id
    get_data_league = session.get(league_api).json()

    league_leader = get_data_league['standings']['results'][0]['total']
    league_difference = league_leader - get_data_entry['summary_overall_points']

    print ("%-39s %-10d %-10d %-11d %d (%d)" % (league_name, previous_rank, current_rank,
        rank_difference, league_leader, league_difference))

print ()

