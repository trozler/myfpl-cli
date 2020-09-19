#!/usr/bin/env python3

def gwRunner(session, get_gw_team, get_data_bootstrap, get_data_entry, get_live_points):

    sp = ' '
    player_list = {"starting": [], "bench": [], "formation": [0, 0, 0, 0]}
    live_points_cache = {}
    player_cache = {}
    speed_gw_points = 0
    print()

    print("Gameweek:", get_data_entry["current_event"])
    print()
    print('{0: >42}'.format("Points"), '{0:>13}'.format(
        '+/-'), '{0: >9}'.format('Chance'))
    print('Name', '{0:>35}'.format('(GW)'), '{0: >9}'.format('Price'), '{0: >6}'.format(
        '(GW)'), '{0: >8}'.format('NextGW'), '{0: >7}'.format("News\n"))

    printGwTeam(session, get_gw_team, get_data_bootstrap,
                get_data_entry, get_live_points, player_list, live_points_cache, player_cache)

    for pl in player_list["starting"]:
        gw_points = live_points_cache[pl["ID"]]['stats']['total_points']
        if pl["multiplier"] == 2:
            gw_points *= 2
        elif pl["multiplier"] == 3:
            gw_points *= 3
        pl["tot_gw_points"] += gw_points
        speed_gw_points += gw_points
        print("%-25s %-9s %-8d %-7.1f %-6.1f %-8d %s" %
              (pl["name"], pl["player_status"], pl["tot_gw_points"], pl["price"], pl["price_change"], pl["next_round"], pl["news"]))

    for pl in player_list["bench"]:
        gw_points = live_points_cache[pl["ID"]]['stats']['total_points']
        pl["tot_gw_points"] += gw_points
        print("%-25s %-9s %-8d %-7.1f %-6.1f %-8d %s" %
              (pl["name"], pl["player_status"], pl["tot_gw_points"], pl["price"], pl["price_change"], pl["next_round"], pl["news"]))

    print("\n\nGameweek points: %d (%d)       \tOverall points: %-7d" %
          (speed_gw_points, get_gw_team["entry_history"]["event_transfers_cost"],
           get_gw_team["entry_history"]["total_points"]))

    print("Gameweek rank:   %-7s\tOverall rank:   %-7s\n" %
          (get_gw_team["entry_history"]["rank"], get_gw_team["entry_history"]["overall_rank"]))

    print("\nH2H Leagues:\n")
    print(sp*40 + "Prev" + sp*7 + "Curr" + sp*7 + "Rank" + sp*7 + "Leader")
    print("League Name" + sp*29 + "Rank" + sp*7 +
          "Rank" + sp*7 + "Diff" + sp*7 + "Points\n")

    for i in range(len(get_data_entry['leagues']['h2h'])):
        league_id = get_data_entry['leagues']['h2h'][i]['id']
        league_name = get_data_entry['leagues']['h2h'][i]['name']
        previous_rank = get_data_entry['leagues']['h2h'][i]['entry_last_rank']
        current_rank = get_data_entry['leagues']['h2h'][i]['entry_rank']
        rank_difference = get_data_entry['leagues']['h2h'][i]['entry_last_rank'] - current_rank

        league_api = 'https://fantasy.premierleague.com/api/leagues-h2h/%s/standings/' % league_id
        get_data_league = session.get(league_api).json()
        if len(get_data_league['standings']['results']) == 0:
            print(
                "Fpl end-point api/leagues-h2h, is not working, please try again later.")
            return

        league_leader = get_data_league['standings']['results'][0]['total']
        point_differential = league_leader - \
            get_data_league['standings']['results'][current_rank - 1]['total']

        print("%-39s %-10d %-10d %-10d %d (%d)" %
              (league_name, previous_rank, current_rank, rank_difference, league_leader, point_differential))

    print("\n\nClassic Leagues:\n")
    print(sp*40 + "Prev" + sp*7 + "Curr" + sp*7 + "Rank" + sp*7 + "Leader")
    print("League Name" + sp*29 + "Rank" + sp*7 +
          "Rank" + sp*7 + "Diff" + sp*7 + "Points\n")

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

        print("%-39s %-10d %-10d %-10d %d (%d)" % (league_name, previous_rank, current_rank,
                                                   rank_difference, league_leader, league_difference))

    print("\n")


def printGwTeam(session, get_gw_team, get_data_bootstrap, get_data_entry, get_live_points, player_list, live_points_cache, player_cache):

    # Key team, value players.
    team_list = {}

    # Use live point to get gw points as well.

    for j in range(len(get_gw_team['picks'])):
        ID = get_gw_team['picks'][j]['element']
        multiplier = get_gw_team['picks'][j]['multiplier']
        vice_captain = get_gw_team['picks'][j]['is_vice_captain']
        team_position = get_gw_team['picks'][j]['position']

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

        if ID in player_cache:
            temp = player_cache[ID].copy()
            temp["player_status"] = player_status
            temp["team_position"] = team_position
            temp["multiplier"] = multiplier

            if player_status == "(Bench)":
                player_list["bench"].append(temp)
            else:
                player_list["starting"].append(temp)
                player_list["formation"][temp["element_type"] - 1] += 1
        else:
            for i in range(len(get_data_bootstrap['elements'])):
                if get_data_bootstrap['elements'][i]['id'] == ID:
                    name = get_data_bootstrap['elements'][i]['web_name']

                    price = get_data_bootstrap['elements'][i]['now_cost'] / 10
                    price_change = get_data_bootstrap['elements'][i]['cost_change_event'] / 10
                    next_round = get_data_bootstrap['elements'][i]['chance_of_playing_next_round']
                    if next_round == None:
                        next_round = 100
                    news = get_data_bootstrap['elements'][i]['news']

                    team = get_data_bootstrap['elements'][i]["team"]
                    if team in team_list:
                        team_list[team].append(ID)
                    else:
                        team_list[team] = [ID]

                    if player_status == "(Bench)":
                        player_list["bench"].append({
                            "name": name,
                            "player_status": player_status,
                            "tot_gw_points": 0,  # Added later.
                            "price": price,
                            "price_change": price_change,
                            "next_round": next_round,
                            "news": news,
                            "team": team,
                            "ID": ID,
                            "element_type": get_data_bootstrap['elements'][i]["element_type"],
                            "team_position": team_position,
                            "multiplier": multiplier
                        })
                        player_cache[ID] = {
                            "name": name,
                            "player_status": None,
                            "tot_gw_points": 0,  # Added later.
                            "price": price,
                            "price_change": price_change,
                            "next_round": next_round,
                            "news": news,
                            "team": team,
                            "ID": ID,
                            "element_type": get_data_bootstrap['elements'][i]["element_type"],
                            "team_position": None,  # Team specific.
                            "multiplier": None  # Team specific
                        }
                    else:
                        player_list["starting"].append({
                            "name": name,
                            "player_status": player_status,
                            "tot_gw_points": 0,  # Added later.
                            "price": price,
                            "price_change": price_change,
                            "next_round": next_round,
                            "news": news,
                            "team": team,
                            "ID": ID,
                            "element_type": get_data_bootstrap['elements'][i]["element_type"],
                            "team_position": team_position,
                            "multiplier": multiplier
                        })
                        player_cache[ID] = {
                            "name": name,
                            "player_status": None,
                            # Added later.
                            "tot_gw_points": 0,
                            "price": price,
                            "price_change": price_change,
                            "next_round": next_round,
                            "news": news,
                            "team": team,
                            "ID": ID,
                            "element_type": get_data_bootstrap['elements'][i]["element_type"],
                            "team_position": None,  # Team specific.
                            "multiplier": None  # Team specific
                        }
                        player_list["formation"][get_data_bootstrap['elements']
                                                 [i]["element_type"] - 1] += 1

                    break

    # Populate live_points_cache here.
    for k in range(len(player_list["bench"])):
        ID = player_list["bench"][k]["ID"]
        if ID not in live_points_cache:
            for i in range(len(get_live_points['elements'])):
                if get_live_points['elements'][i]['id'] == ID:
                    live_points_cache[ID] = get_live_points['elements'][i]
                    break

    for k in range(len(player_list["starting"])):
        ID = player_list["starting"][k]["ID"]
        if ID not in live_points_cache:
            for i in range(len(get_live_points['elements'])):
                if get_live_points['elements'][i]['id'] == ID:
                    live_points_cache[ID] = get_live_points['elements'][i]
                    break

    if not get_data_bootstrap["events"][0]["finished"]:
        getFixtuerData(session, get_data_bootstrap, get_data_entry,
                       player_list, team_list, get_live_points, live_points_cache)

    # testing
    # getFixtuerData(session, get_data_bootstrap, get_data_entry,
    #                player_list, team_list, get_live_points, live_points_cache)
    # testing


def getFixtuerData(session, get_data_bootstrap, get_data_entry, player_list, team_list, get_live_points, live_points_cache) -> int:
    fixture_url = "https://fantasy.premierleague.com/api/fixtures/?event=%s#/" % get_data_entry["current_event"]
    get_gw_fixture = session.get(fixture_url).json()

    # testing
    # get_gw_fixture = None
    # with open('./teststuff/test2.json') as jf:
    #     get_gw_fixture = json.load(jf)
    # testing

    finished = {}
    started = {}
    upcoming = {}

    # Iterate over all fixtuers
    for g in range(len(get_gw_fixture)):
        if get_gw_fixture[g]["finished"] == True:
            finished[get_gw_fixture[g]["team_a"]] = get_gw_fixture[g]
            finished[get_gw_fixture[g]["team_h"]] = get_gw_fixture[g]

        elif get_gw_fixture[g]["started"] == True:
            started[get_gw_fixture[g]["team_a"]] = get_gw_fixture[g]
            started[get_gw_fixture[g]["team_h"]] = get_gw_fixture[g]

        else:
            upcoming[get_gw_fixture[g]["team_a"]] = get_gw_fixture[g]
            upcoming[get_gw_fixture[g]["team_h"]] = get_gw_fixture[g]

        # Possibly add bonus points
        if get_gw_fixture[g]["team_a"] in team_list or get_gw_fixture[g]["team_h"] in team_list:
            # Need add provisional bonus points.
            if get_gw_fixture[g]["started"] == True and get_gw_fixture[g]["finished"] == False:

                bp_players = find_prelim_bonus(get_gw_fixture[g])

                # Now we need to check if any of your players are on bonus, if so increase their points.
                for pl in range(len(player_list["starting"])):
                    if player_list["starting"][pl]["ID"] in bp_players:
                        player_list["starting"][pl]["tot_gw_points"] += bp_players[player_list["starting"][pl]["ID"]]

                for pl in range(len(player_list["bench"])):
                    if player_list["bench"][pl]["ID"] in bp_players:
                        player_list["bench"][pl]["tot_gw_points"] += bp_players[player_list["bench"][pl]["ID"]]

    n_subs_made = 0

    for k in range(len(player_list["starting"])):
        player_info = live_points_cache[player_list["starting"][k]["ID"]]
        if player_list["starting"][k]["team"] not in upcoming and not player_info["stats"]["minutes"] > 0:
            replacement_found = make_sub(
                k, player_list, finished, started, upcoming, live_points_cache)
            if replacement_found:
                n_subs_made += 1
        if n_subs_made == 3:
            break


'''
Edge cases:
* Need to maintain the minimum number of players in each position:
    - golakeeper can only replace goal keeper.
    - If playing 3 at the back, and defender not playing. Only another defender can replace that defender.
    - If playing 1 striker, only striker can replace that striker.
    - If playing 3 midfield, only midfielder can replace that midfielder.
'''


def make_sub(index_of_sub, player_list, finished, started, upcoming, live_points_cache) -> bool:
    player_to_swap = player_list["starting"][index_of_sub]
    n_defenders = player_list["formation"][1]
    n_mids = player_list["formation"][2]
    n_attackers = player_list["formation"][3]

    valid_sub_types = set()
    replacement_found = False  # There may be no replacement.

    # We need to use defender sub.
    if n_defenders == 3 and player_to_swap["element_type"] == 2:
        valid_sub_types.add(2)
    elif n_mids == 3 and player_to_swap["element_type"] == 3:
        valid_sub_types.add(3)  # We need to use mid sub.
    elif n_attackers == 1 and player_to_swap["element_type"] == 4:
        valid_sub_types.add(4)  # We need to use attacker sub.
    elif player_to_swap["element_type"] == 1:
        valid_sub_types.add(1)  # We need to use goalie sub.
    else:  # Any type will do.
        valid_sub_types.update([2, 3, 4])

    for j in range(len(player_list["bench"])):
        # make swap.
        if player_list["bench"][j]["team"] not in upcoming and player_list["bench"][j]["element_type"] in valid_sub_types and live_points_cache[player_list["bench"][j]["ID"]]["stats"]["minutes"] > 0:
            replacement_found = True
            # Change formation
            player_list["formation"][player_list["bench"]
                                     [j]["element_type"] - 1] += 1
            player_list["formation"][player_to_swap["element_type"] - 1] -= 1

            # If captain is benched need to make multiplier 2 fro vice captain.
            if player_to_swap["player_status"] == "(C)":
                for k in range(len(player_list["starting"])):
                    if player_list["starting"][k]["player_status"] == "(VC)":
                        player_list["starting"][k]["player_status"] = "(C)"
                        player_list["starting"][k]["multiplier"] = 2
                        break

            elif player_to_swap["player_status"] == "(TC)":
                for k in range(len(player_list["starting"])):
                    if player_list["starting"][k]["player_status"] == "(VC)":
                        player_list["starting"][k]["player_status"] = "(TC)"
                        player_list["starting"][k]["multiplier"] = 3
                        break

            # Update player statuss
            player_list["bench"][j]["player_status"] = ""
            player_to_swap["player_status"] = "(Bench)"

            # Multiplier
            player_list["bench"][j]["multiplier"] = 1
            player_to_swap["multiplier"] = 0

            player_list["bench"][j]["team_position"], player_to_swap["team_position"] = player_to_swap[
                "team_position"], player_list["bench"][j]["team_position"]

            # Need to swap elements in starting and bench array.
            player_list["bench"][j], player_list["starting"][index_of_sub] = player_list["starting"][index_of_sub], player_list["bench"][j]

            break

    # There may be no replacement in a very bad case.
    if not replacement_found:
        return False
    return True


def find_prelim_bonus(fixture):

    h_i, a_i = 0, 0
    bp_players = {}
    n_players = 3
    record = {"last_bps_score": -1, "last_bonus": -1}

    while n_players > 0 and h_i < len(fixture["stats"][9]["h"]) and a_i < len(fixture["stats"][9]["a"]):
        if fixture["stats"][9]["h"][h_i]["value"] > fixture["stats"][9]["a"][a_i]["value"]:
            if fixture["stats"][9]["h"][h_i]["value"] == record["last_bps_score"]:
                bp_players[fixture
                           ["stats"][9]["h"][h_i]["element"]] = record["last_bonus"]
            else:
                bp_players[fixture["stats"][9]["h"]
                           [h_i]["element"]] = n_players
                record["last_bonus"] = n_players
                record["last_bps_score"] = fixture["stats"][9]["h"][h_i]["value"]

            h_i += 1
            n_players -= 1

        elif fixture["stats"][9]["h"][h_i]["value"] < fixture["stats"][9]["a"][a_i]["value"]:
            if fixture["stats"][9]["a"][a_i]["value"] == record["last_bps_score"]:
                bp_players[fixture
                           ["stats"][9]["a"][a_i]["element"]] = record["last_bonus"]
            else:
                bp_players[fixture
                           ["stats"][9]["a"][a_i]["element"]] = n_players
                record["last_bonus"] = n_players
                record["last_bps_score"] = fixture["stats"][9]["a"][a_i]["value"]

            a_i += 1
            n_players -= 1

        elif fixture["stats"][9]["h"][h_i]["value"] == fixture["stats"][9]["a"][a_i]["value"]:

            bp_players[fixture
                       ["stats"][9]["a"][a_i]["element"]] = n_players
            bp_players[fixture
                       ["stats"][9]["h"][h_i]["element"]] = n_players

            n_players -= 2
            h_i += 1
            a_i += 1

    return bp_players
