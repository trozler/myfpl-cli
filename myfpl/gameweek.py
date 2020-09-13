
import sys


def gwRunner(session, get_gw_team, get_data_bootstrap, get_data_entry):

    sp = ' '
    print()
    printGwTeam(session, get_gw_team, get_data_bootstrap, get_data_entry)

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


def printGwTeam(session, get_gw_team, get_data_bootstrap, get_data_entry):
    speed_gw_points = 0
    player_list = {"starting": [], "bench": []}
    # Key team, value players.
    team_list = {}

    print("Gameweek:", get_data_entry["current_event"])
    print()
    print('{0: >42}'.format("Points"), '{0:>13}'.format(
        '+/-'), '{0: >9}'.format('Chance'))
    print('Name', '{0:>35}'.format('(GW)'), '{0: >9}'.format('Price'), '{0: >6}'.format(
        '(GW)'), '{0: >8}'.format('NextGW'), '{0: >7}'.format("News\n"))

    for j in range(len(get_gw_team['picks'])):
        ID = get_gw_team['picks'][j]['element']
        multiplier = get_gw_team['picks'][j]['multiplier']
        vice_captain = get_gw_team['picks'][j]['is_vice_captain']
        position = get_gw_team['picks'][j]['position']

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

        for i in range(len(get_data_bootstrap['elements'])):
            if get_data_bootstrap['elements'][i]['id'] == ID:
                name = get_data_bootstrap['elements'][i]['web_name']
                gw_points = get_data_bootstrap['elements'][i]['event_points']
                if multiplier == 2:
                    gw_points *= 2
                elif multiplier == 3:
                    gw_points *= 3
                price = get_data_bootstrap['elements'][i]['now_cost'] / 10
                price_change = get_data_bootstrap['elements'][i]['cost_change_event'] / 10
                next_round = get_data_bootstrap['elements'][i]['chance_of_playing_next_round']
                if next_round == None:
                    next_round = 100
                news = get_data_bootstrap['elements'][i]['news']

                if multiplier > 0:
                    speed_gw_points += gw_points

                team = get_data_bootstrap['elements'][i]["team"]
                if team in team_list:
                    team_list[team].append(ID)
                else:
                    team_list[team] = [ID]

                if player_status == "(Bench)":
                    player_list["bench"].append({
                        "name": name,
                        "player_status": player_status,
                        "gw_points": gw_points,
                        "price": price,
                        "price_change": price_change,
                        "next_round": next_round,
                        "news": news,
                        "team": team,
                        "ID": ID
                    })
                else:
                    player_list["starting"].append({
                        "name": name,
                        "player_status": player_status,
                        "gw_points": gw_points,
                        "price": price,
                        "price_change": price_change,
                        "next_round": next_round,
                        "news": news,
                        "team": team,
                        "ID": ID
                    })

                # print("%-25s %-9s %-8d %-7.1f %-6.1f %-8d %s" %
                #       (name, player_status, gw_points, price, price_change, next_round, news))

                break

    speed_gw_points = getFixtuerData(session, get_data_bootstrap,
                                     get_data_entry, player_list, team_list, speed_gw_points)

    print("\n\nGameweek points: %d (%d)       \tOverall points: %-7d" %
          (speed_gw_points, get_gw_team["entry_history"]["event_transfers_cost"],
           get_gw_team["entry_history"]["total_points"]))

    print("Gameweek rank:   %-7s\tOverall rank:   %-7s\n" %
          (get_gw_team["entry_history"]["rank"], get_gw_team["entry_history"]["overall_rank"]))


# TODO; Include provisional bounus for all players.
# TODO: Include players on bench if they are playing and a game has started and starting player is not playing.

'''
teams_needed:
* Array of teams for our players.

'''


def getFixtuerData(session, get_data_bootstrap, get_data_entry, player_list, team_list, speed_gw_points) -> int:
    fixture_url = "https://fantasy.premierleague.com/api/fixtures/?event=%s#/" % get_data_entry["current_event"]
    get_gw_fixture = session.get(fixture_url).json()

    # Iterate over players, for each player check:
    # 1. Is he playing
    # 2. Add prelim bonus points.

    # Need to check if a player which we have starting is actually on bench:
    # Bootstrap contains minutes a player has played.
    # Q: When does the bootsrap minute Api update.
    # IDEA: Maybe https://fantasy.premierleague.com/api/event/1/live/#/ updates.

    # Iterate over all fixtuers
    for g in range(len(get_gw_fixture)):
        # Possibly add bonus points
        if get_gw_fixture[g]["team_a"] in team_list or get_gw_fixture[g]["team_h"] in team_list:
            # Need add provisional bonus points.
            if get_gw_fixture[g]["started"] == True and get_gw_fixture[g]["finished_provisional"] == True and get_gw_fixture[g]["finished"] == False:
                speed_gw_points = addBonus(get_gw_fixture, player_list, g)

    return speed_gw_points


# Returns list of top 3 players that will receive bonus.
def addBonus(get_gw_fixture, player_list, g) -> list:
    if len(get_gw_fixture[g]["stats"]) > 0:
        h_i, a_i = 0, 0
        bp_players = {}
        n_players = 3

        while n_players > 0 and h_i < len(get_gw_fixture[g]["stats"][9]["h"]) and a_i < len(get_gw_fixture[g]["stats"][9]["a"]):
            if get_gw_fixture[g]["stats"][9]["h"][h_i]["value"] > get_gw_fixture[g]["stats"][9]["a"][a_i]["value"]:

                bp_players[get_gw_fixture[g]
                           ["stats"][9]["h"][h_i]["element"]] = n_players
                h_i += 1
                n_players -= 1
            elif get_gw_fixture[g]["stats"][9]["h"][h_i]["value"] < get_gw_fixture[g]["stats"][9]["a"][a_i]["value"]:

                bp_players[get_gw_fixture[g]
                           ["stats"][9]["a"][a_i]["element"]] = n_players

                a_i += 1
                n_players -= 1
            elif get_gw_fixture[g]["stats"][9]["h"][h_i]["value"] == get_gw_fixture[g]["stats"][9]["a"][a_i]["value"]:

                bp_players[get_gw_fixture[g]
                           ["stats"][9]["a"][a_i]["element"]] = n_players
                bp_players[get_gw_fixture[g]
                           ["stats"][9]["h"][h_i]["element"]] = n_players

                n_players -= 2
                h_i += 1
                a_i += 1

        # Now we need to check if any of your players are on bonus, if so increase their points.
        for pl in range(player_list["starting"]):
            if player_list["starting"][pl]["ID"] in bp_players:
                player_list["starting"][pl]["gw_points"] += bp_players[player_list["starting"][pl]["ID"]]
                speed_gw_points += bp_players[player_list["starting"][pl]["ID"]]

        for pl in range(player_list["bench"]):
            if player_list["bench"][pl]["ID"] in bp_players:
                player_list["bench"][pl]["gw_points"] += bp_players[player_list["bench"][pl]["ID"]]

    else:
        print(
            "Error api/fixtures has not updated game stats yet. Please try again later.")
        sys.exit(1)

    return speed_gw_points
