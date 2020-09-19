#!/usr/bin/env python3

import sys
from myfpl.gameweek import find_prelim_bonus
from datetime import datetime, timezone

global_cnt = 0
print_delta = 0


def fixtureRunner(session, get_gw_fixture, get_data_bootstrap, curr_gw):
    print("\nGameweek:", curr_gw)
    print()

    team_list = {}  # Key is team id and val is number.

    for k in range(len(get_data_bootstrap["teams"])):
        team_list[get_data_bootstrap["teams"][k]
                  ["id"]] = get_data_bootstrap["teams"][k]["name"]

    finished = []
    started = []
    upcoming = []
    player_cache = {}

    for g in range(len(get_gw_fixture)):
        if get_gw_fixture[g]["finished_provisional"] == True:
            finished.append(get_gw_fixture[g])

        elif get_gw_fixture[g]["started"] == True:
            started.append(get_gw_fixture[g])

        else:  # Upcoming
            upcoming.append(get_gw_fixture[g])

    if finished:
        print_finished(finished, team_list, get_data_bootstrap, player_cache)
        print()

    if started:
        print_started(session, started, team_list, get_data_bootstrap,
                      player_cache, curr_gw)
        print()

    if upcoming:
        print_upcoming(upcoming, team_list, get_data_bootstrap)
        print()


def findNames(home_list, away_list, get_data_bootstrap, player_cache):
    point_scorers = {"home": [], "away": []}

    for k in range(len(home_list)):
        ID = home_list[k]["element"]
        if ID not in player_cache:
            for j in range(len(get_data_bootstrap['elements'])):
                if get_data_bootstrap['elements'][j]['id'] == ID:
                    player_cache[ID] = {
                        "name": get_data_bootstrap['elements'][j]["web_name"],
                        "team_id": get_data_bootstrap['elements'][j]["team"]
                    }
                    point_scorers["home"].append({
                        "id": ID,
                        "n_points": home_list[k]["value"],
                        "name": player_cache[ID]["name"],
                        "team_id": player_cache[ID]["team_id"]
                    })
                    break
        else:
            point_scorers["home"].append({
                "id": ID,
                "n_points": home_list[k]["value"],
                "name": player_cache[ID]["name"],
                "team_id": player_cache[ID]["team_id"]
            })

    for k in range(len(away_list)):
        ID = away_list[k]["element"]
        if ID not in player_cache:
            for j in range(len(get_data_bootstrap['elements'])):
                if get_data_bootstrap['elements'][j]['id'] == ID:
                    player_cache[ID] = {
                        "name": get_data_bootstrap['elements'][j]["web_name"],
                        "team_id": get_data_bootstrap['elements'][j]["team"]
                    }
                    point_scorers["away"].append({
                        "id": ID,
                        "n_points": away_list[k]["value"],
                        "name": player_cache[ID]["name"],
                        "team_id": player_cache[ID]["team_id"]
                    })
                    break
        else:
            point_scorers["away"].append({
                "id": ID,
                "n_points": away_list[k]["value"],
                "name": player_cache[ID]["name"],
                "team_id": player_cache[ID]["team_id"]
            })
    return point_scorers


def print_upcoming(upcoming, team_list, get_data_bootstrap):
    global global_cnt
    print("\nUpcoming:")
    for g in range(len(upcoming)):
        print('\n\n{:<5} {:>17}'.format(
            str(g + global_cnt + 1) + ".", team_list[upcoming[g]["team_h"]]), end="")
        print('{:<12} {} '.format("", "vs"), end="")

        # https://stackoverflow.com/questions/45448083/convert-time-from-utc-to-gmt-with-python
        # https://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python
        # datetime.strptime("2020-09-12T11:30:00Z", "%Y-%m-%dT%H:%M:%SZ").strftime("%a %d %b %Y, %H:%M GMT.")
        display_time = None
        if sys.version_info.minor < 6:
            display_time = datetime.strptime(
                upcoming[g]["kickoff_time"], "%Y-%m-%dT%H:%M:%SZ").strftime("%a %d %b %Y, %H:%M GMT.")
        else:
            display_time = datetime.strptime(upcoming[g]["kickoff_time"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc).astimezone().strftime("%a %d %b %Y, %H:%M %Z.")

        print('{:<14} {:18} {}'.format(
            "", team_list[upcoming[g]["team_a"]], display_time))

    global_cnt += 1


def find_time(session, fixture, get_data_bootstrap, player_cache, curr_gw):
    kickoff_time = datetime.strptime(
        fixture["kickoff_time"], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.utcnow()
    elapsedTime = now - kickoff_time
    game_time = divmod(elapsedTime.total_seconds(), 60)

    if game_time[0] < 15:  # May in extreme case have no bps points.
        return int(game_time[0])
    else:  # Need to get max time spent on pitch of 3 players.
        live_points_url = "https://fantasy.premierleague.com/api/event/%s/live/#/" % curr_gw
        get_live_points = session.get(live_points_url).json()

        markers = [fixture["stats"][9]["a"][0], fixture["stats"]
                   [9]["h"][0], fixture["stats"][9]["h"][1]]

        time = 0

        for pl in markers:
            ID = pl["element"]
            for i in range(len(get_live_points['elements'])):
                if get_live_points['elements'][i]['id'] == ID:
                    if get_live_points['elements'][i]["stats"]["minutes"] > time:
                        time = get_live_points['elements'][i]["stats"]["minutes"]
                    break
        return time


def print_started(session, started, team_list, get_data_bootstrap, player_cache, curr_gw):
    global global_cnt
    print("\nStarted:")
    for g in range(len(started)):

        # Get the playing time of keeper and 3 defenders, then take mode as gametime.
        display_time = find_time(
            session, started[g], get_data_bootstrap, player_cache, curr_gw)
        # display_time = started[g]["minutes"]

        print('\n\n{:<5} {:>17}'.format(
            str(g + global_cnt + 1) + ".", team_list[started[g]["team_h"]]), end="")
        print('{:<12} {} - {}'.format("",
                                      started[g]["team_h_score"], started[g]["team_a_score"]), end="")
        print('{:<12} {:18} ({} mins)'.format(
            "", team_list[started[g]["team_a"]], display_time))

        for k in [0, 2, 1, 4, 5, 6, 9]:

            h_i, a_i = 0, 0
            h_points = len(started[g]["stats"][k]["h"])
            a_points = len(started[g]["stats"][k]["a"])

            point_scorers = None

            if h_points > 0 or a_points > 0:  # Only print if some points were scored.
                if k == 0:
                    print('{:<36}{}'.format("", "Goals"))
                elif k == 2:
                    print('{:<36}{}'.format("", "Own goals"))
                elif k == 1:
                    print('{:<36}{}'.format("", "Assists"))
                elif k == 4:
                    print('{:<36}{}'.format("", "Penalties missed"))
                elif k == 5:
                    print('{:<36}{}'.format("", "Yellow cards"))
                elif k == 6:
                    print('{:<36}{}'.format("", "Red cards"))
                elif k == 9:
                    print('{:<36}{}'.format("", "Prelim bonus"))

                if k == 9:

                    bonus_points = find_prelim_bonus(started[g])
                    # find_prelim_bonus returns data in wrong format, need to find team and name of player. Before printing.
                    temp_all = [{"value": v, "element": k}
                                for k, v in bonus_points.items()]
                    home_team_id = started[g]["team_h"]
                    away_team_id = started[g]["team_a"]

                    point_scorers = {"home": [], "away": []}

                    for k in range(len(temp_all)):
                        ID = temp_all[k]["element"]
                        if ID in player_cache:
                            team_id = player_cache[ID]["team_id"]
                            if team_id == home_team_id:
                                point_scorers["home"].append({
                                    "id": ID,
                                    "n_points": temp_all[k]["value"],
                                    "name": player_cache[ID]["name"],
                                    "team_id": player_cache[ID]["team_id"]
                                })
                            elif team_id == away_team_id:
                                point_scorers["away"].append({
                                    "id": ID,
                                    "n_points": temp_all[k]["value"],
                                    "name": player_cache[ID]["name"],
                                    "team_id": player_cache[ID]["team_id"]
                                })
                            else:
                                print(
                                    "Error, player ID doesnt belong to any of the teams.")
                                sys.exit(1)
                        else:
                            for j in range(len(get_data_bootstrap['elements'])):
                                if get_data_bootstrap['elements'][j]['id'] == ID:
                                    player_cache[ID] = {
                                        "name": get_data_bootstrap['elements'][j]["web_name"],
                                        "team_id": get_data_bootstrap['elements'][j]["team"]
                                    }

                                    team_id = player_cache[ID]["team_id"]

                                    if team_id == home_team_id:
                                        point_scorers["home"].append({
                                            "id": ID,
                                            "n_points": temp_all[k]["value"],
                                            "name": player_cache[ID]["name"],
                                            "team_id": player_cache[ID]["team_id"]
                                        })

                                    elif team_id == away_team_id:
                                        point_scorers["away"].append({
                                            "id": ID,
                                            "n_points": temp_all[k]["value"],
                                            "name": player_cache[ID]["name"],
                                            "team_id": player_cache[ID]["team_id"]
                                        })

                                    break

                    h_points = len(point_scorers["home"])
                    a_points = len(point_scorers["away"])
                else:
                    point_scorers = findNames(started[g]["stats"][k]["h"],
                                              started[g]["stats"][k]["a"], get_data_bootstrap, player_cache)

                while h_i < h_points or a_i < a_points:
                    away_yes = False
                    home_yes = False

                    if h_i < h_points:
                        home_yes = True
                        print('{:>21} {}'.format(
                            point_scorers["home"][h_i]["name"], point_scorers["home"][h_i]["n_points"]), end='')
                        h_i += 1

                    if a_i < a_points:
                        if home_yes:  # Just printed a home player need alignment for away.
                            print('{:<31}{} {}'.format("",
                                                       point_scorers["away"][a_i]["name"], point_scorers["away"][a_i]["n_points"]))
                            away_yes = True
                            a_i += 1
                        else:  # Nothing was printed need more alignmemt.
                            print('{:<54}{} {}'.format("",
                                                       point_scorers["away"][a_i]["name"], point_scorers["away"][a_i]["n_points"]))
                            away_yes = True
                            a_i += 1

                    if not away_yes and home_yes:  # Only printed home and not away, need new line.
                        print()

    global_cnt += len(started)


def print_finished(finished, team_list, get_data_bootstrap, player_cache):
    global global_cnt
    print("Finished:")
    for g in range(len(finished)):
        print('\n\n{:<5} {:>17}'.format(
            str(g + 1) + ".", team_list[finished[g]["team_h"]]), end="")
        print('{:<12} {} - {}'.format("",
                                      finished[g]["team_h_score"], finished[g]["team_a_score"]), end="")
        print('{:<12} {}'.format("", team_list[finished[g]["team_a"]]))

        for k in [0, 2, 1, 4, 5, 6, 9]:

            # Goals, assites then own goals.
            h_i, a_i = 0, 0
            h_points = len(finished[g]["stats"][k]["h"])
            a_points = len(finished[g]["stats"][k]["a"])

            if h_points > 0 or a_points > 0:  # Only print if some points were scored.
                if k == 0:
                    print('{:<36}{}'.format("", "Goals"))
                elif k == 2:
                    print('{:<36}{}'.format("", "Own goals"))
                elif k == 1:
                    print('{:<36}{}'.format("", "Assists"))
                elif k == 4:
                    print('{:<36}{}'.format("", "Penalties missed"))
                elif k == 5:
                    print('{:<36}{}'.format("", "Yellow cards"))
                elif k == 6:
                    print('{:<36}{}'.format("", "Red cards"))
                elif k == 9:
                    print('{:<36}{}'.format("", "Bonus"))

                if k == 9:

                    if finished[g]["finished"] == False:

                        bonus_points = find_prelim_bonus(finished[g])
                        # find_prelim_bonus returns data in wrong format, need to find team and name of player. Before printing.
                        temp_all = [{"value": v, "element": k}
                                    for k, v in bonus_points.items()]
                        home_team_id = finished[g]["team_h"]
                        away_team_id = finished[g]["team_a"]

                        point_scorers = {"home": [], "away": []}

                        for k in range(len(temp_all)):
                            ID = temp_all[k]["element"]
                            if ID in player_cache:
                                team_id = player_cache[ID]["team_id"]
                                if team_id == home_team_id:
                                    point_scorers["home"].append({
                                        "id": ID,
                                        "n_points": temp_all[k]["value"],
                                        "name": player_cache[ID]["name"],
                                        "team_id": player_cache[ID]["team_id"]
                                    })
                                elif team_id == away_team_id:
                                    point_scorers["away"].append({
                                        "id": ID,
                                        "n_points": temp_all[k]["value"],
                                        "name": player_cache[ID]["name"],
                                        "team_id": player_cache[ID]["team_id"]
                                    })
                                else:
                                    print(
                                        "Error, player ID doesnt belong to any of the teams.")
                                    sys.exit(1)
                            else:
                                for j in range(len(get_data_bootstrap['elements'])):
                                    if get_data_bootstrap['elements'][j]['id'] == ID:
                                        player_cache[ID] = {
                                            "name": get_data_bootstrap['elements'][j]["web_name"],
                                            "team_id": get_data_bootstrap['elements'][j]["team"]
                                        }

                                        team_id = player_cache[ID]["team_id"]

                                        if team_id == home_team_id:
                                            point_scorers["home"].append({
                                                "id": ID,
                                                "n_points": temp_all[k]["value"],
                                                "name": player_cache[ID]["name"],
                                                "team_id": player_cache[ID]["team_id"]
                                            })

                                        elif team_id == away_team_id:
                                            point_scorers["away"].append({
                                                "id": ID,
                                                "n_points": temp_all[k]["value"],
                                                "name": player_cache[ID]["name"],
                                                "team_id": player_cache[ID]["team_id"]
                                            })
                                        else:
                                            print(
                                                "Error, player ID doesnt belong to any of the teams.")
                                            sys.exit(1)
                                        break

                        h_points = len(point_scorers["home"])
                        a_points = len(point_scorers["away"])
                    else:  # Can use official bonus, no need for computation.
                        point_scorers = findNames(finished[g]["stats"][k - 1]["h"],
                                                  finished[g]["stats"][k - 1]["a"], get_data_bootstrap, player_cache)
                        h_points = len(point_scorers["home"])
                        a_points = len(point_scorers["away"])

                else:
                    point_scorers = findNames(finished[g]["stats"][k]["h"],
                                              finished[g]["stats"][k]["a"], get_data_bootstrap, player_cache)

                while h_i < h_points or a_i < a_points:
                    away_yes = False
                    home_yes = False

                    if h_i < h_points:
                        home_yes = True
                        print('{:>21} {}'.format(
                            point_scorers["home"][h_i]["name"], point_scorers["home"][h_i]["n_points"]), end='')
                        h_i += 1

                    if a_i < a_points:
                        if home_yes:  # Just printed a home player need alignment for away.
                            print('{:<31}{} {}'.format("",
                                                       point_scorers["away"][a_i]["name"], point_scorers["away"][a_i]["n_points"]))
                            away_yes = True
                            a_i += 1
                        else:  # Nothing was printed need more alignmemt.
                            print('{:<54}{} {}'.format("",
                                                       point_scorers["away"][a_i]["name"], point_scorers["away"][a_i]["n_points"]))
                            away_yes = True
                            a_i += 1

                    if not away_yes and home_yes:  # Only printed home and not away, need new line.
                        print()

    global_cnt += len(finished)
