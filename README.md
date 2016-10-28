# JerryBot

A Python Facebook chat bot written in Python.  Uses a forked [fbchat](https://pypi.python.org/pypi/fbchat/) module with applied patches to get group chat working.

Written for Python2.7 in Python3

##Installation

1. Clone Repo
2. Run
`git submodule init`
to initialize the submodule repo
3. Run
`git submodule update`
to update the repo and pull the data.
4. Update credentials.py with relevant account information

##Usage

`python JerryBot.py`

##Modules

Currently provided modules:
 * Flip (Flip a coin)
 * Roll (Roll an n sided die, default six)
 
Planned Modules:
 * 5cMenu Module
 * Reminders
 * Linkme/define
