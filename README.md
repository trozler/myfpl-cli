## myfpl - A command line interface for Fantasy Premier League

![Python][2]![Shell][1]![License][3]

A command line interface that allows users to retrieve information about their fpl teams, leagues and fixtures in single commands.

Currently the core commands are:

**Live leagues**

![live](./promo/live.gif)

- Check out other people's teams and your league standings way before fpl updates. All standings and teams are based on real time scores, which are adjusted for preliminary bonus and substitutions. Also includes every players captaincy choice and transfer hits. It can be used on leagues of any size, inclduing the overall league.

**Fixture**

![live](./promo/fix.gif)

- Get real time scores from PL fixtures, including goals, assits, cards and bonus.

**Gameweek**

![live](./promo/gw.gif)

- See how your gameweek is going by viewing your real time score, adjusted for preliminary bonus and substitutions.

**Team**

![live](./promo/team.gif)

- Team command is intended for users who want to plan for future gameweeks. It will correctly display the team you have selected for next gameweek, transfers made and chips available.

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

### How to install

Using pip it is very easy, simply run the following:

```
$ pip3 install myfpl
$ myfpl <your args go here>
```

If you want to clone using git instead of pip, here's how you do it.

```
$ cd ~
$ git clone https://github.com/trozler/myfpl.git
$ cd myfpl
$ pip3 install -r requirements.txt
$ python -m myfpl <args>
```

### Usage

Users are required to know their **unique fpl entry id**. The id can be retreived on the fpl site by clicking "points"and looking at url.

Example: https://fantasy.premierleague.com/entry/{team-id}/history

## Configuration options

- -g, --gameweek
  - See how your gameweek is going before fpl updates, by viewing your real time score, adjusted for preliminary bonus and substitutions.
- -t, --team
  - Plan for future gameweeks by viewing transfers made, chips avialable, currently selected team and more.
- -l, --live
  - Check out your league standings before fpl updates. All standings are based on real time scores, which are adjusted for preliminary bonus and substitutions.
- -f, --fixture
  - Get real time scores from PL fixtures.
- -c, --clear
  - Remove your email and team id stored in config.json.
- -h, --help
  - Show help for all commands.

[1]: https://img.shields.io/badge/-Shell-89e051
[2]: https://img.shields.io/badge/python-3.3+-blue
[3]: https://img.shields.io/badge/license-MIT-orange
