
from collections import OrderedDict
from .gameweek import printGwTeam, find_prelim_bonus


# Globals
league_map = OrderedDict()
player_map = OrderedDict()
sp = ' '


def liveRunner(session, get_data_entry, get_data_bootstrap, get_live_points, get_gw_fixture):
    global league_map, player_map
    print("\nClassic Leagues:\n")
    print('{0: >54}'.format('Prev'), '{0:>10}'.format('Curr'),
          '{0: >13}'.format('Rank'), '{0: >16}'.format('Leader'))
    print("League Name", '{0:>42}'.format('Rank'), '{0: >10}'.format(
        'Rank'), '{0: >13}'.format('Diff'), '{0: >17}'.format("Points\n"))

    for i in range(len(get_data_entry['leagues']['classic'])):
        league_id = get_data_entry['leagues']['classic'][i]['id']
        league_name = get_data_entry['leagues']['classic'][i]['name']
        previous_rank = get_data_entry['leagues']['classic'][i]['entry_last_rank']
        current_rank = get_data_entry['leagues']['classic'][i]["entry_rank"]
        rank_difference = previous_rank - current_rank

        league_api = 'https://fantasy.premierleague.com/api/leagues-classic/%s/standings/' % league_id
        get_data_league = session.get(league_api).json()

        if len(get_data_league['standings']['results']) == 0:
            print(
                "Fpl end-point api/leagues-classic, is not working, please try again later.")
            return

        league_leader = get_data_league['standings']['results'][0]['total']
        league_difference = league_leader - \
            get_data_entry['summary_overall_points']

        # Create league hashmap. Value is a tuple of name and league id.
        league_map[i] = (league_name, league_id)

        print("(%d) %-45s %-10d %-13d %-14d %d (%d)" % (i, league_name, previous_rank, current_rank,
                                                        rank_difference, league_leader, league_difference))

    # Get all fixtures that have started and get prelim bonus for each match.
    started = []
    prelim_bonus = {}  # FInd all prelim bonus and add to a map.

    for g in range(len(get_gw_fixture)):
        if get_gw_fixture[g]["finished"] == False and get_gw_fixture[g]["started"] == True:
            started.append(get_gw_fixture[g])
            bonus_points = find_prelim_bonus(started[g])
            for k, v in bonus_points.items():
                prelim_bonus[k] = v

    while True:
        print(
            "\nEnter the ID (left of name) of the league you want live standings for or q to exit:")
        try:
            ID = input()
            if ID == 'q':
                break
            ID = int(ID)
            if ID not in league_map:
                continue
            else:
                process_league(ID, session, get_data_entry,
                               get_data_bootstrap, get_live_points, prelim_bonus)
        except:
            continue

    print()


def process_league(ID, session, get_data_entry, get_data_bootstrap, get_live_points, prelim_bonus):
    global league_map, player_map
    # Orderd dict for sorting efficiency
    user_map = OrderedDict()
    page_num = 1
    limit_page = 4

    league_api = 'https://fantasy.premierleague.com/api/leagues-classic/%s/standings/?page_new_entries=1&page_standings=%s&phase=1' % (
        league_map[ID][1], page_num)
    get_data_league = session.get(league_api).json()
    gameweek = get_data_entry["current_event"]

    while True:
        for i in range(len(get_data_league["standings"]["results"])):
            team_id = get_data_league["standings"]["results"][i]["entry"]
            # User id
            user_id = (get_data_league["standings"]["results"][i]["entry_name"] +
                       ' - ' + get_data_league["standings"]["results"][i]["player_name"])
            # gw_Team API
            gw_team_api = 'https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/' % (
                team_id, gameweek)
            get_gw_team = session.get(gw_team_api).json()
            # get old gw points - costly try and find improvement in future
            if gameweek > 1:
                gw_team_old_api = 'https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/' % (
                    team_id, gameweek - 1)
                get_gw_old_team = session.get(gw_team_old_api).json()
                gw_old_points = get_gw_old_team["entry_history"]["total_points"]
            else:
                gw_old_points = 0

            speed_gw_points = 0
            # Captain points(already doubled), Name, triple (boolean)
            captain_id_name = [None, None, False]

            for pl in range(len(get_gw_team['picks'])):
                id = get_gw_team['picks'][pl]['element']
                multi = get_gw_team['picks'][pl]['multiplier']

                if multi > 0 and id in player_map:
                    gw_points = player_map[id][0]
                    if id in prelim_bonus:
                        gw_points += prelim_bonus[id]

                    if multi == 2:
                        # Mark as captain
                        gw_points *= 2
                        captain_id_name[0], captain_id_name[1] = gw_points, player_map[id][1]
                    elif multi == 3:
                        # Mark as Tripple captain
                        gw_points *= 3
                        captain_id_name[0], captain_id_name[1], captain_id_name[2] = gw_points, player_map[id][1], True

                    speed_gw_points += gw_points

                elif multi > 0:
                    for j in range(len(get_data_bootstrap['elements'])):
                        if get_data_bootstrap['elements'][j]['id'] == id:
                            # Need to iterate over live points.
                            gw_points = get_data_bootstrap['elements'][j]['total_points']
                            if id in prelim_bonus:
                                gw_points += prelim_bonus[id]
                            # Issue is here, cannot do get_live_points
                            player_map[id] = (
                                gw_points, get_data_bootstrap['elements'][j]['web_name'])
                            if multi == 2:
                                # Mark as captain
                                gw_points *= 2
                                captain_id_name[0], captain_id_name[1] = gw_points, player_map[id][1]
                            elif multi == 3:
                                # Mark as Triple captain
                                gw_points *= 3
                                captain_id_name[0], captain_id_name[1], captain_id_name[2] = gw_points, player_map[id][1], True

                            speed_gw_points += gw_points
                            break

                # Captain didn't play, was substituted and Vice didn't play.
                elif get_gw_team['picks'][pl]['is_captain'] and captain_id_name[0] == None:
                    if id in player_map:
                        captain_id_name[0], captain_id_name[1] = 0, player_map[id][1]
                    # Player is not in player map. Need to find in bootstrap.
                    else:
                        for j in range(len(get_data_bootstrap['elements'])):
                            if get_data_bootstrap['elements'][j]['id'] == id:
                                player_map[id] = (
                                    0, get_data_bootstrap['elements'][j]['web_name'])
                                break
                        captain_id_name[0], captain_id_name[1] = 0, player_map[id][1]

            # Have Team name + person name of as key. Value is a tuple:
            # (gw-1 points + gw points - hits, gw points - hits, previous rank, hits, gw team)
            user_map[user_id] = (speed_gw_points + gw_old_points - get_gw_team["entry_history"]["event_transfers_cost"], speed_gw_points - get_gw_team["entry_history"]["event_transfers_cost"],
                                 get_data_league["standings"]["results"][i]["rank"],
                                 -get_gw_team["entry_history"]["event_transfers_cost"],
                                 captain_id_name, get_gw_team)

        # Only print first 200 entries. Then ask if want to keep going
        if page_num == limit_page or len(get_data_league['standings']['results']) == 0:
            # Ask if keep going, as there exsits a next page.
            if len(get_data_league['standings']['results']) != 0 and page_num == limit_page:
                print(
                    "\nEnter 'go' to see output or enter anything else to process another 200 players:")
                try:
                    temp = input()
                    if temp == 'go':
                        break
                    else:
                        page_num += 1
                        limit_page += 4
                        league_api = 'https://fantasy.premierleague.com/api/leagues-classic/%s/standings/?page_new_entries=1&page_standings=%s&phase=1' % (
                            league_map[ID][1], page_num)
                        get_data_league = session.get(league_api).json()

                except:
                    page_num += 1
                    limit_page += 4
                    league_api = 'https://fantasy.premierleague.com/api/leagues-classic/%s/standings/?page_new_entries=1&page_standings=%s&phase=1' % (
                        league_map[ID][1], page_num)
                    get_data_league = session.get(league_api).json()

            else:
                break

        else:
            page_num += 1
            league_api = 'https://fantasy.premierleague.com/api/leagues-classic/%s/standings/?page_new_entries=1&page_standings=%s&phase=1' % (
                league_map[ID][1], page_num)
            get_data_league = session.get(league_api).json()

    # Perform sorting: Use selection sort as stable and exploit psudo orderd property of league table. Faster than python nlogn library quicksort.
    user_list = list(user_map.items())
    for k in range(1, len(user_list)):
        key = user_list[k]
        w = k - 1
        while w >= 0 and key[1][0] > user_list[w][1][0]:
            user_list[w + 1] = user_list[w]
            w -= 1
        user_list[w + 1] = key

    print()
    print('{0: >49}'.format('Curr'), '{0:>9}'.format('Prev'),
          '{0: >9}'.format('Rank'), '{0: >43}'.format('Net'))
    print('{0: <41}'.format('Name'), '{0:>7}'.format('Rank'), '{0: >9}'.format('Rank'), '{0: >9}'.format(
        'Diff'), '{0: >11}'.format('Captain'), '{0: >24}'.format('Hits'), '{0: >10}'.format("Points\n"))

    for i in range(len(user_list)):
        print("%-44s %-9d %-9d %-8d %-27s %-7d %d (%d)" % (user_list[i][0], i + 1, user_list[i][1][2], user_list[i][1][2] - (i + 1), ((user_list[i][1][4][1] + ' ('+str(
            user_list[i][1][4][0]) + ')' + '(TC)') if user_list[i][1][4][2] else user_list[i][1][4][1] + ' ('+str(user_list[i][1][4][0]) + ')'), user_list[i][1][3], user_list[i][1][0], user_list[i][1][1]))

    live_points_cache = {}
    while True:
        print("\nView a players team by entering their current rank:")
        try:
            ID = int(input())
            if 1 <= ID <= len(user_list):
                player_list = {"starting": [],
                               "bench": [], "formation": [0, 0, 0, 0]}
                get_gw_team = user_list[ID - 1][1][5]
                speed_gw_points = 0
                print("\n" + user_list[ID - 1][0])
                print("Gameweek:", get_data_entry["current_event"])
                print()
                print('{0: >42}'.format("Points"), '{0:>13}'.format(
                    '+/-'), '{0: >9}'.format('Chance'))
                print('Name', '{0:>35}'.format('(GW)'), '{0: >9}'.format('Price'), '{0: >6}'.format(
                    '(GW)'), '{0: >8}'.format('NextGW'), '{0: >7}'.format("News\n"))

                printGwTeam(session, get_gw_team,
                            get_data_bootstrap, get_data_entry, get_live_points, player_list, live_points_cache)

                for pl in player_list["starting"]:
                    gw_points = live_points_cache[pl["ID"]
                                                  ]['stats']['total_points']
                    if pl["multiplier"] == 2:
                        gw_points *= 2
                    elif pl["multiplier"] == 3:
                        gw_points *= 3
                    pl["tot_gw_points"] += gw_points
                    speed_gw_points += gw_points
                    print("%-25s %-9s %-8d %-7.1f %-6.1f %-8d %s" %
                          (pl["name"], pl["player_status"], pl["tot_gw_points"], pl["price"], pl["price_change"], pl["next_round"], pl["news"]))

                for pl in player_list["bench"]:
                    gw_points = live_points_cache[pl["ID"]
                                                  ]['stats']['total_points']
                    pl["tot_gw_points"] += gw_points
                    print("%-25s %-9s %-8d %-7.1f %-6.1f %-8d %s" %
                          (pl["name"], pl["player_status"], pl["tot_gw_points"], pl["price"], pl["price_change"], pl["next_round"], pl["news"]))

                print("\n\nGameweek points: %d (%d)       \tOverall points: %-7d" %
                      (speed_gw_points, get_gw_team["entry_history"]["event_transfers_cost"],
                       get_gw_team["entry_history"]["total_points"]))

                print("Gameweek rank:   %-7s\tOverall rank:   %-7s\n" %
                      (get_gw_team["entry_history"]["rank"], get_gw_team["entry_history"]["overall_rank"]))

        except:
            break
