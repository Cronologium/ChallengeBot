# ChallengeBot

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

## Prerequisites

*Main*

* [python 2.7](https://www.python.org/download/releases/2.7/) - link is for windows, on linux it comes preinstalled
* [django 1.11.3](https://www.djangoproject.com/download/) - the web framework (if you never worked with django, i recommend [this simple tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) which will give you some basics)
* psutil - should be from pip, but [a common error](https://github.com/StorjOld/dataserv-client/issues/171) may occur

*Minor but not insignificant*

* [django-bootstrap3](https://pypi.python.org/pypi/django-bootstrap3/9.0.0) - gives an easy way to make css pretty 
* [django-codemirror2](https://pypi.python.org/pypi/django-codemirror2/0.2) - adds the awesome code editor in the website
* [django-mathfilters](https://pypi.python.org/pypi) - on pip, not listed on official pypip website. Adds math computations to django

## How to run

### Front-end

The website can run independently, without any dispatcher supporting it. The dispatcher is there to evaluate sources. In order to start the webserver.

```
python manage.py runserver
```

Ocasionally, models in the front-end may change, and the database needs to reflect those changes, or sql errors in django may occur. To fix that:

```
python manage.py makemigrations
```

This will create a migration. If a change was detected, a python source will be save and a migration_name will be given (xyzt) where x, y, z, t are digits. For now, let's assume a new change has the migration_name 0017. You need to take into account which version of the database you are on. Say, if the migration has been done for 0017, you need to apply all versions up until it. If you made just one change, then you only have sqlmigrate that one.

```
python manage.py sqlmigrate web 0016
python manage.py sqlmigrate web 0017
```

To create sql queries pending on the database. But in order to apply the changes, type

```
python manage.py migrate web
```

### Back-end

During testing, the dispatcher will set all jobs from the database to *Registered* and it will start to evaluate all of them in order. (In its current form)

```
python run.py
```

### The dispatcher?

Yes. It looks in the database for registered, un-evaluated jobs and completes them. It has a registry of known games which it can execute.

# Writing your game in the back-end

Most of the complicated stuff for basic games are already implemented (how a turn works, adding players, communicating with them etc.)
Depeding on which type of game you need to implement, you will use either AbstractGame or PhasingGame as super class. 
If using a PhasingGame, each phase of the game must be specified and associated with an integer starting from one, self.phase should be changed when necessary to switch to a different phase.

## When to use PhasingGame?

When a game has different phases which require player interaction and have different behaviour.
Example: Battleships has two game phases. In one, the player puts the ships, in the other, they to shoot the enemy ship.

## Logging

Log relevant data which can be used later by a the front-end to show all the data in a pretty way. Do not show the commands sent by user, filter them and show only what they did.

## Declaring winners or losers

Each AbstractPlayer comes with its status. If the status of the player is changed anytime during the game from *Status.PLAYING* to anything else, the player will leave the game and that will be logged. *Status.WINNER, Status.LOSER* will ask the player to leave nicely, while all other will result in a *kick*. It is recommended you only change the status of a player in the check function (see implementation for super class used to see what already exists, usually only turns, phases, checks, starts and finished should be implemented). 
As of new updates, changing the status should occur **only through special functions in the AbstractGame class**
When receiving None as a command, the player **must be kicked** with Status.TIMEOUT_EXCEEDED. 

## How to test a game?

**Do not use the dispatcher.** Create an executable, conveniently placed .py file which loads the game with a port and test list of players. Create a separate client which directly connects to the server using sockets. See (sources-test folder as a reference)

## The ranking system
Everytime you set a status of a player to WINNER, they will automatically get the best position possible in the ranking. Everytime you set a status of a player to LOSER, they will automatically get the worst position possible in the ranking. There is another tier of *worseness*: disqualification. A player's source can be disqualified, which means it will get the disqualified status and cannot be used again. In this case, all players with loser status will be above the players with disqualified.

### Experience
After the ranking has been determined, each player will be awarded accordingly to their rank in the ranking. If a player is disqualified, they will not enter the ranking, but others will benefit from their loss. The formula for computing xp gain is

```
xp_gain = (xp_win * no_players_below + xp_lost * no_players_above) / (no_players - 1) * (author ? 1.5 : 1.0)
```

Which means the player gets the average of how many players they beat minus how many players beat them. If a player initiates the challenge, they get 150% bonus xp. Be aware as all xp lost will also be multiplied.

There is also a bonus for players which manage to get a source accepted from the first submission: They will automatically start at level **2**

### How to set experience for a level?

1. Figure out possible win-rates for different sources and try to predict the meta of the game.
2. Set win-rates for each level. Try to set as many levels as possible (Recommended for now: 10) (Ex. 1: 33% 2: 50% 3: 66% for a 3-level game)
3. Set the following values:
```
xp_win = xp_reach / wins
xp_lost = - level_win_rate * xp_win
```
Preferabily keep the difference between xp_win and xp_lost
Also, if your game accepts draws (such as X and O) figure out a value which is convenient between xp_lost and xp_win. Increase xp_dsq exponentially after each level. Heavily penalize a disqualification in high level, even with 100% in the last level

Example:
Level 1 (Win-rate 0%):

xp_reach = 60xp

xp_gain = 20xp

xp_lost = 0xp

xp_draw = 10xp

xp_dsq = -10xp


Level 2(Win-rate 25%):

xp_reach = 100xp

xp_gain = 25xp

xp_lost = -7xp

xp_draw = 8xp

xp_dsq = -20xp


...

Level X(Win-rate: 66%):

xp_reach = 1000xp

xp_gain = 40xp

xp_lost = -27xp

xp_draw = 0xp

xp_dsq = -1000xp


This way, for a player to advance a level, they will either have to: 
- have a good enough win-rate the whole level to beat the established one
- know the field and challenge players in order to win (because of the 50% xp bonus)

### Issues with current system

1. Farming low-level players (will be solved by increasing xp gain of low level win and decreasing xp lost of low level and decreasing xp gain of win high level and increasing xp lost of win high level).
2. Continuosly farming same player (a cap on challenging same player will be added soon)
3. The submission bonus is lost if submissions are reeavaluated

## Coding style and coding-related

* Use as much jquery as you can, avoid javascript
* OOP and inheritance of already implemented generic stuff is *mandatory* in back-end. If something needs to be implemented, it must added in such a matter that it is similar to real life situations (even a dice has a class)
* on front-end there should be just function calls with a few exceptions
* all forms should be sent through ajax and be validated *only* on server-side
* write code as generic as possible, *high re-usage is required*
* parts of a function which are related can be spaced out from others (using an empty line)
* if something that already exists can be written more genericaly, create issues to discuss
* releases can be made only from the master branch

### Mentions

* Any change to front-end code will result in an immediate change on the server if it is open (**except for models and form classes**)

### Q & A

**Q:** I changed a coding resource (.js, .css etc.) but the page is still showing the old one. What happened?
**A: It is cached, CTRL+SHIFT+R should fix it**

**Q:** I changed a png or other image file, why does not it show up?
**A: Also cached, but you need to clear browser cache this time**

**Q** What are migrations? 
**A: Whenever you change the models, the corresponding database file needs to be updated. A migration means moving data from a database version to another.**

**Q** My code worked before. Now that i merged with master branch it does not. What's the problem?
**A: Chances are: your database is out of date with the new models. Django tries to find objects according to models.py, not how the database looks. If someone merged to master a change on the models and changed the code which used them, you need to migrate your data to the newest database version (see migrations above)**

### Restrictions

* **Do not code on master branch unless it is crucial and have approval**
* *Do not change models or forms classes unless discussed and approved with @Cronologium*. This is a main problem for git pulling (because of migrations) and it should be avoided at all costs or worked with very rarely and at a time.
* *Do not change urls in the urls.py file unless discussed and approved with @Cronologium*. For security reasons and not messing up the work of others, you should avoid changing this kind of basic stuff.

Such undiscussed/unapproved changes will not be taken into consideration.

### Warnings

* **Adding perma-redirects (302) to links will most likely result in losing rights to access the repo.**
* **Any intentional security back-door introduces in the website will result in automatically losing rights**

