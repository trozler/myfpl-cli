## myfpl - A command line interface for Fantasy Premier League

![Python][2]![https://requests.readthedocs.io/en/master/][4]![Shell][1]![License][3]

A command line interface that allow fpl users to retrieve information about their teams and leagues, whilst skipping the laborious web log in flow in a single command.

Currently the core commands are:

**Live leagues**

```
$ myfpl --live

or if no alias created (see below)

$ python3 ~/myfpl/myfpl -l
```

- This command fills the gap caused by FPL being slow to update leagues during gameweeks. It provides real time league positions (net of transfers) and changes in rank, before fpl officially updates tables at the end of the gameday. Also includes every players captaincy choice and transfer hits. It can be used on leagues of any size, inclduing the overall league.
  The accurcay of the real time points, should be the same as websites such as /livefpl.net and /fplgameweek.com.

**Gameweek**

```
$ myfpl -g
```

- Gw script is intened for users intrested in following thier team's progress during a gameweek. The gw script will correctly displays real time points (net of transfers), price changes, classic and h2h league ranks.

**Team**

```
$ myfpl --team
```

- Team script is intended for users who want to plan for future gameweeks. Team script will correctly display the team you have selected for next gameweek, transfers made and chips available.

#### Note

Information about all commands can always be found by running:

```
$ myfpl --help
```

### Prerequesits

You have python3 installed.

- If you don't have python3, you can use this guide [this](https://realpython.com/installing-python/#how-to-install-python-on-macos) guide.
- If your not sure if you do, you can run the following on the command line:

```
$ python3 --version
Python 3.8.1
```

Any version of python 3 will work.

### How to install

```
$ cd ~
$ git clone https://github.com/trozler/myfpl.git
$ cd myfpl
$ pip3 install -r requirements.txt
```

For ease of use it is highly recommended that you create an alias for the package.

- If you know you are using a bash shell do:

```
echo -e '\nalias myfpl="python3 -m ~/myfpl/myfpl"' >> ~/.bash_profile
```

- Otherwise this will work:

```
echo -e '\nalias myfpl="python3 -m ~/myfpl/myfpl"' >> ~/.profile
```

### Usage

Users are required to know their **unique fpl entry id**. The id can be retreived on the fpl site by clicking "points"and looking at url.

Example: https://fantasy.premierleague.com/entry/{team-id}/history

[1]: https://img.shields.io/badge/Shell-Bash-89e051
[2]: https://img.shields.io/badge/python-3.3+-blue
[3]: https://img.shields.io/badge/license-MIT-orange
[4]: https://img.shields.io/badge/python-requests-%23da86c5
