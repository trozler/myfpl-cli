## Fantasy Premier League Live - Command Line Scripts

Three python scripts that allow fpl users to retrieve information about their teams and leagues, whilst skipping the laborious web log in flow in a single command.

- Live leagues script aims to fill the gap caused by FPL being slow to update leagues during gameweeks. It provides real time league positions (net of transfers) and changes in rank, before fpl officially updates tables at the end of the gameday. Also includes every players captaincy choice and transfer hits.

- Gw script is intened for users intrested in following thier team's progress during a gameweek. The gw script will correctly displays real time points (net of transfers), price changes, classic and h2h league ranks.

- Team script is intended for users who want to plan for future gameweeks. Team script will correctly display the team you have selected for next gameweek, transfers made and chips available.

## How to install

```
$ cd ~
$ git clone https://github.com/trozler/fantasyPremierLeagueLive.git
```

If you have Bash, run the commands below to create aliases in your `~/.bash_profile`, allowing you to easily invoke gameweek(fplgw), team(fplteam) and live leagues (fpllive), in a single command.

`~/.bashrc` should also work.

```
echo -e '\nalias fplgw="python3 ~/fantasyPremierLeagueLive/src/gameweek_checker.py"' >> ~/.bash_profile
echo -e '\nalias fplteam="python3 ~/fantasyPremierLeagueLive/src/team_checker.py"' >> ~/.bash_profile
echo -e '\nalias fpllive="python3 ~/fantasyPremierLeagueLive/src/live_leagues.py"' >> ~/.bash_profile
```

### Usage note

Users are required to know their **unique fpl entry id**. The id can be retreived on the fpl site by clicking "my team", "view gameweek history" and looking at url.
Example: https://fantasy.premierleague.com/entry/{team-id}/history

It is also highly recommended that users hardcode their emails and team ID's, at the beginning each of the 3 scripts. This will speed up the login process significantly. However, do not hardcode your password.

`'login': 'youremail@mail.com', team_id = xxxxxx`

## Dependencies

- python3.
- [requests module](https://pypi.org/project/requests/)
