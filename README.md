## myfpl - A command line interface for Fantasy Premier League

![Python][2]![Shell][1]![License][3]

A command line interface that allows users to retrieve information about their fpl teams, leagues and fixtures in single commands.

Currently the core commands are:

**Live leagues**

![live](./promo/live.gif)

- See other people's teams and your league standings way before fpl updates. All standings and teams are based on real time scores, which are adjusted for bonus and substitutions. Output also includes every players captaincy choice and transfer hits. It can be used on leagues of any size, inclduing the overall league.

**Fixture**

![live](./promo/fix.gif)

- Get real time scores from PL fixtures, including goals, assists, cards and bonus.

**Gameweek**

![live](./promo/gw.gif)

- See how your gameweek is going by viewing your real time score, adjusted for bonus and substitutions.

**Team**

![live](./promo/team.gif)

- Team command is intended for users who want to plan for future gameweeks. It will correctly display the team you have selected for next gameweek, transfers made and chips available.
- You will be prompted for your team id, fpl email and password, the first time you use this command, as your current team line up is private. Your email and team id will be cached locally, but never your password. The next time around you will only be promtped for your password. You can always clear the cache by running `myfpl -c`.

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

Using pip simply run:

```
$ pip3 install myfpl
$ myfpl <your args go here>
```

Note:

- Do not use `sudo pip3 install myfpl`, as this will leads to issues with file permissions for `config.json`. And requires you to run `sudo myfpl` for every command.

If you want to clone the project do the following.

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
  - See how your gameweek is going before fpl updates, by viewing your real time score, adjusted for bonus and substitutions.
- -t, --team
  - Plan for future gameweeks by viewing transfers made, chips avialable, currently selected team and more. Since your team line-up is private, your Fpl password and email are required. Your email and team id will be cached locally for future use, but never your password. You can clear the cache with -c command.
- -l, --live
  - Check out your league standings before fpl updates. All standings are based on real time scores, which are adjusted for bonus and substitutions.
- -f, --fixture
  - Get real time scores from PL fixtures.
- -c, --clear
  - Remove your email and team id stored in config.json.
- -h, --help
  - Show help for all commands.

### Contribution

If you spot bugs or have features that you'd really like to see in myfpl, please check out the [contributing page](https://github.com/trozler/myfpl/blob/master/.github/CONTRIBUTING.md).

[1]: https://img.shields.io/badge/-Shell-89e051
[2]: https://img.shields.io/badge/python-3.3+-blue
[3]: https://img.shields.io/badge/license-MIT-orange
