# ChallengeBot

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

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

This will create a migration. If a change was detected, a python source will be save and a migration_name will be given (xyzt) where x, y, z, t are digits. For now, let's assume a new change has the migration_name 0017

```
python manage.py sqlmigrate web 0017
```

To create the sql queries for a migration. But in order to apply the changes, type

```
python manage.py migrate web
```

### Back-end

During testing, the dispatcher will set all jobs from the database to *Registered* and it will start to evaluate all of them in order. (In its current form)

```
python run.py
```

## Writing your game in the back-end

Most of the complicated stuff for basic games are already implemented (how a turn works, adding players, communicating with them etc.)
Depeding on which type of game you need to implement, you will use either AbstractGame or PhasingGame as super class. 
If using a PhasingGame, each phase of the game must be specified and associated with an integer starting from one, self.phase should be changed when necessary to switch to a different phase.

### When to use PhasingGame?

When a game has different phases which require player interaction and have different behaviour.
Example: Battleships has two game phases. In one, the player puts the ships, in the other, they to shoot the enemy ship.

### Logging

Log relevant data which can be used later by a the front-end to show all the data in a pretty way. Do not show the commands sent by user, filter them and show only what they did.

### Declaring winners or losers

Each AbstractPlayer comes with its status. If the status of the player is changed anytime during the game from *Status.PLAYING* to anything else, the player will leave the game and that will be logged. *Status.WINNER, Status.DRAW, Status.LOSER* will ask the player to leave nicely, while all other will result in a *kick*. It is recommended you only change the status of a player in the check function (see implementation for super class used to see what already exists, usually only turns, phases, checks, starts and finished should be implemented). 
When receiving None as a command, the player **must be kicked** with Status.TIMEOUT_EXCEEDED


## Coding style and coding-related

* Use as much jquery as you can, avoid javascript
* OOP and inheritance of already implemented generic stuff is *mandatory* in back-end. If something needs to be implemented, it must added in such a matter that it is similar to real life situations (even a dice has a class)
* on front-end there should be just function calls with a few exceptions
* all forms should be sent through ajax and be validated *only* on server-side (WIP)
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

### Restrictions

* **Do not code on master branch unless it is crucial and have approval**
* *Do not change models or forms classes unless discussed and approved with @Cronologium*. This is a main problem for git pulling (because of migrations) and it should be avoided at all costs or worked with very rarely and at a time.
* *Do not change urls in the urls.py file unless discussed and approved with @Cronologium*. For security reasons and not messing up the work of others, you should avoid changing this kind of basic stuff.

Such undiscussed/unapproved changes will not be taken into consideration.

### Warnings

* **Adding perma-redirects (302) to links will most likely result in losing rights to access the repo.**
* **Any intentional security back-door introduces in the website will result in automatically losing rights**

