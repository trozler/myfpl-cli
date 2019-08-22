import requests
import traceback
import re


#FPL ID
#663372

#Overall fpl api
#https://fantasy.premierleague.com/api/entry/663372/
#Team api
#https://fantasy.premierleague.com/api/my-team/663372/


#Set password and login (login is equivelent to email) fileds for easy future use 
credentials = {'password':'Drogba1997',
               'login':'tony.rosler246@gmail.com',
               'redirect_uri': 'https://fantasy.premierleague.com/a/login',
               'app': 'plfpl-web'
               }

#Set team_id for future use by changing None
team_id = 663372

#Only ask for validation if team_id, email and password havn't been set
if team_id == None or credentials['password'] == None or credentials['password'] == None:
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
        password = input()
        credentials['password'] = password

        break


bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
get_data_bootstrap = requests.get(bootstrap_url).json()

#gweek_url = 'https://fantasy.premierleague.com/api/entry/%s/' % (team_id)
#gweek = requests.get(gweek_url).json()
#gameweek = gweek['current_event']

#Establish session
session = requests.session()
session.post('https://users.premierleague.com/accounts/login/', data=credentials)

#Get team information using session object
team_api = 'https://fantasy.premierleague.com/api/my-team/%s/' % (team_id)
get_data_team = session.get(team_api).json()


team = []
status = []


#Querry transfers and see if zero. If not zero then replace teh transferd in player with teh old player/ 

transfer_api = 'https://fantasy.premierleague.com/api/entry/%s/transfers-latest/' % (team_id)
get_transfer = session.get(transfer_api).json()


#If length is equal to 0 then 
if (len(get_transfer) == 0):
    







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

sp = ' '
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

print ("\n\nGameweek points: %-7d\tOverall points: %-7d" %
    (get_data_team['entry_history']['points'], get_data_team['entry_history']['total_points']))

print ("Gameweek rank:   %-7d\tOverall rank:   %-7d\n" %
    (get_data_team['entry_history']['rank'], get_data_team['entry_history']['overall_rank']))


#Rank section
#https://fantasy.premierleague.com/api/entry/663372

entry_api = 'https://fantasy.premierleague.com/api/entry/%s' % team_id
get_data_entry = get_data_team = requests.get(entry_api).json()

#print(get_data_entry)

print ("\nH2H Leagues:\n")
print (sp*40 + "Prev" + sp*7 + "Curr" + sp*7 + "Rank" + sp*8 + "Leader")
print ("League Name" + sp*29 + "Rank" + sp*7 + "Rank" + sp*7 + "Diff" + sp*8 + "Points\n")

for i in range(len(get_data_entry['leagues']['h2h'])):
    league_id = get_data_entry['leagues']['h2h'][i]['id']
    league_name = get_data_entry['leagues']['h2h'][i]['name']
    previous_rank = get_data_entry['leagues']['h2h'][i]['entry_last_rank']


    #Needs to be chnaged currently no ['entry_movement'] field.
    #There seems to be an actual 'rank' filed so none of this is necessary
    
    #if get_data_entry['leagues']['h2h'][i]['entry_movement'] == "up":
        #current_rank = previous_rank - get_data_entry['leagues']['h2h'][i]['entry_change']
    #elif get_data_entry['leagues']['h2h'][i]['entry_movement'] == "down":
        #current_rank = previous_rank + get_data_entry['leagues']['h2h'][i]['entry_change']
    #else:
        #current_rank = previous_rank
    #rank_difference = previous_rank - current_rank

    

    league_api = 'https://fantasy.premierleague.com/api/leagues-h2h-standings/%s' % league_id
    get_data_league = get_data_team = requests.get(league_api).json()

    league_leader = get_data_league['standings']['results'][0]['points_total']

    print ("%-39s %-10d %-10d %-11d %d" %
        (league_name, previous_rank, current_rank, rank_difference, league_leader))

print ("\n\nClassic Leagues:\n")
print (sp*40 + "Prev" + sp*7 + "Curr" + sp*7 + "Rank" + sp*8 + "Leader")
print ("League Name" + sp*29 + "Rank" + sp*7 + "Rank" + sp*7 + "Diff" + sp*8 + "Points\n")

for i in range (len(get_data_entry['leagues']['classic'])):
    league_id = get_data_entry['leagues']['classic'][i]['id']
    league_name = get_data_entry['leagues']['classic'][i]['name']
    previous_rank = get_data_entry['leagues']['classic'][i]['entry_last_rank']
    if get_data_entry['leagues']['classic'][i]['entry_movement'] == "up":
        current_rank = previous_rank - get_data_entry['leagues']['classic'][i]['entry_change']
    elif get_data_entry['leagues']['classic'][i]['entry_movement'] == "down":
        current_rank = previous_rank + get_data_entry['leagues']['classic'][i]['entry_change']
    else:
        current_rank = previous_rank
    rank_difference = previous_rank - current_rank

    league_api = 'https://fantasy.premierleague.com/api/leagues-classic-standings/%s' % league_id
    get_data_league = get_data_team = requests.get(league_api).json()

    league_leader = get_data_league['standings']['results'][0]['total']
    league_difference = get_data_entry['entry']['summary_overall_points'] - league_leader

    print ("%-39s %-10d %-10d %-11d %d (%d)" % (league_name, previous_rank, current_rank,
        rank_difference, league_leader, league_difference))

print ()

