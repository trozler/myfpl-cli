#!/usr/bin/env python3

import requests
import getpass
import argparse
import sys
import json
import os
import pkg_resources

from myfpl.live import liveRunner
from myfpl.gameweek import gwRunner
from myfpl.team import teamRunner
from myfpl.fixtures import fixtureRunner

team_id = None

config_path = pkg_resources.resource_filename(
    "myfpl", os.path.join(".config", "config.json"))


def addCli():
    parser = argparse.ArgumentParser(
        description="The myfpl cli allows you to retrieve information about your fpl team.", prog="myfpl",
        epilog="\n"
    )
    parser.add_argument("-g", "--gameweek", action="store_true", dest="gameweek",
                        help="See how your gameweek is going by viewing your real time score, adjusted for bonus and substitutions.")
    parser.add_argument("-t",
                        "--team", action="store_true", dest="team", help="Plan for future gameweeks by viewing transfers made, chips avialable, currently selected team and more.")
    parser.add_argument("-l",
                        "--live", action="store_true", dest="live", help="See other people's teams and your league standings before fpl updates. All standings and teams are based on real time scores, which are adjusted for bonus and substitutions. Output also includes every players captaincy choice and transfer hits. It can be used on leagues of any size, inclduing the overall league.")

    parser.add_argument("-c",
                        "--clear", action="store_true", dest="clear", help="Remove your email and team id stored in config.json.")

    parser.add_argument("-f",
                        "--fixtures", action="store_true", dest="fix", help="Get real time scores from PL fixtures.")

    if len(sys.argv) <= 1:
        parser.print_help()
        print()
        sys.exit(1)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        print()
        sys.exit(1)

    return args


def handleTeamId():
    global team_id
    flag = False
    with open(config_path, 'r+') as jf:
        config_data = json.load(jf)

        if config_data["team_id"] == "":  # Enter your team id
            flag = True

            while True:
                print("Enter team ID: ", end='')
                temp = input()
                try:
                    temp = int(temp)
                    if temp <= 0:
                        print("please enter a valid team id.")
                        continue
                    team_id = temp
                    config_data["team_id"] = team_id
                    break
                except:
                    print("please enter a valid team id.")

        else:
            team_id = int(config_data["team_id"])

        if flag:
            jf.seek(0, 0)
            json.dump(config_data, jf, ensure_ascii=False, indent=4)

    return flag


def handleLogin(credentials):
    global team_id
    flag = False
    with open(config_path, 'r+') as jf:
        config_data = json.load(jf)

        if config_data["team_id"] == "":  # Enter your team id
            flag = True

            while True:
                print("Enter team ID: ", end='')
                temp = input()
                try:
                    temp = int(temp)
                    if temp <= 0:
                        print("please enter a valid team id.")
                        continue
                    team_id = temp
                    config_data["team_id"] = team_id
                    break
                except:
                    print("please enter a valid team id.")

        else:
            team_id = int(config_data["team_id"])

        if config_data["email"] == "":  # Handle email
            flag = True

            while True:
                print("Enter email: ", end='')
                email = input()

                credentials['login'] = email
                config_data["email"] = email
                break

        else:
            credentials['login'] = config_data["email"]

        if flag:
            jf.seek(0, 0)
            json.dump(config_data, jf, ensure_ascii=False, indent=4)

    credentials['password'] = getpass.getpass()

    return flag


def clearConfig():
    with open(config_path, 'w') as jf:
        config_data = {
            "email": "",
            "team_id": ""
        }
        json.dump(config_data, jf, ensure_ascii=False, indent=4)


def main():
    global team_id

    credentials = {'password': None,
                   'login': None,
                   'redirect_uri': 'https://fantasy.premierleague.com/a/login',
                   'app': 'plfpl-web'
                   }

    args = addCli()
    session = requests.session()

    # Api fetched for all scripts.
    bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    get_data_bootstrap = session.get(bootstrap_url).json()

    # Shoudl not ask for password.
    if args.gameweek:

        handleTeamId()

        entry_api = 'https://fantasy.premierleague.com/api/entry/%s/' % team_id
        get_data_entry = session.get(entry_api).json()

        # Positive integer provided is too large clear data.
        if len(get_data_entry) == 1:
            print("Bad team id, please try again.")
            clearConfig()
            sys.exit(1)

        if get_data_entry["current_event"] == None:
            print(
                "Fpl api/entry is not available currently, please try again when season returns.")
            sys.exit(1)

        # gw_Team API will always work no login needed.
        gw_team_api = 'https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/' % (
            team_id, get_data_entry["current_event"])
        get_gw_team = session.get(gw_team_api).json()

        live_points_url = "https://fantasy.premierleague.com/api/event/%s/live/#/" % get_data_entry["current_event"]
        get_live_points = session.get(live_points_url).json()

        # testing
        # get_live_points = None
        # with open(config_path) as jf:
        #     get_live_points = json.load(jf)
        # testing

        gwRunner(session, get_gw_team, get_data_bootstrap,
                 get_data_entry, get_live_points)

    # Should not ask for password.
    elif args.live:

        handleTeamId()
        entry_api = 'https://fantasy.premierleague.com/api/entry/%s/' % team_id
        get_data_entry = session.get(entry_api).json()

        if len(get_data_entry) == 1:
            print("Bad team id, please try again.")
            clearConfig()
            sys.exit(1)

        if get_data_entry["current_event"] == None:
            print(
                "Premier League not in season, please come when season returns.")
            sys.exit(1)

        live_points_url = "https://fantasy.premierleague.com/api/event/%s/live/#/" % get_data_entry["current_event"]
        get_live_points = session.get(live_points_url).json()

        fixture_url = "https://fantasy.premierleague.com/api/fixtures/?event=%s#/" % get_data_entry["current_event"]
        get_gw_fixture = session.get(fixture_url).json()

        liveRunner(session, get_data_entry,
                   get_data_bootstrap, get_live_points, get_gw_fixture)

    # Password needed
    elif args.team:
        curr_gw = None
        for k in range(len(get_data_bootstrap["events"])):
            if get_data_bootstrap["events"][k]["is_current"] == True:
                curr_gw = k + 1

        # Handle errors
        if (curr_gw) == None:
            print("Premier League not in season, please come when season returns.")
            sys.exit(1)

        handleLogin(credentials)

        session.post('https://users.premierleague.com/accounts/login/',
                     data=credentials)
        credentials['login'] = None
        credentials['password'] = None
        team_api = 'https://fantasy.premierleague.com/api/my-team/%s/' % (
            team_id)

        get_data_team = session.get(team_api).json()

        if len(get_data_team) == 1:  # If bad passowrd, emial or team_id. Always 200 response,
            print("Wrong login information, please try again.")
            clearConfig()
            sys.exit(1)

        teamRunner(session, team_id, get_data_team,
                   get_data_bootstrap, curr_gw)

    elif args.fix:
        curr_gw = None
        for k in range(len(get_data_bootstrap["events"])):
            if get_data_bootstrap["events"][k]["is_current"] == True:
                curr_gw = k + 1

        # Handle errors
        if (curr_gw) == None:
            print("Premier League not in season, please come back when season returns.")
            sys.exit(1)

        fixture_url = "https://fantasy.premierleague.com/api/fixtures/?event=%s#/" % curr_gw
        get_gw_fixture = session.get(fixture_url).json()

        # testing
        # get_gw_fixture = None
        # with open(config_path) as jf:
        #     get_gw_fixture = json.load(jf)
        # testing

        if not get_gw_fixture:
            print("No fixtures currently available, please try again later.")
        else:
            fixtureRunner(session, get_gw_fixture, get_data_bootstrap, curr_gw)

    if args.clear:
        clearConfig()


if __name__ == "__main__":
    main()
