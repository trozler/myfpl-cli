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

[1]: https://img.shields.io/badge/Shell-Bash-89e051
[2]: https://img.shields.io/badge/python-3.3+-blue
[3]: https://img.shields.io/badge/license-MIT-orange
[4]: https://img.shields.io/badge/python-requests-%23da86c5

```
The -m option searches sys.path for the module name and runs its content as

When you import a module, what really happens is that you load its contents for later access and use.

The file with the Python code must be located in your current working directory.
The file must be in the Python Module Search Path (PMSP), where Python looks for the modules and packages you import.

sys.path is equal to python path.
Essentially every folder with python code you want to add to the syspath needs an **init**.py file. These **init**.py files can be empty.

```

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
