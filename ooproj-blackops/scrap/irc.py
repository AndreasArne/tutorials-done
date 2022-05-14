#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file contains classes:
* IrcLogParser
* Message
For parisng an irc log
"""

import re

class User():
    """
    Represents an Irc user
    """

    def __init__(self, nick, role, online):
        """
        Constructor
        """
        self.nick = nick
        self.role = role
        self.online = online
        self.messages = []

    def printInfo(self):
        print("{}{} is online: {}\n\
        {}".format(self.role, self.nick, self.online, "\n\t".join([str(x) for x in self.messages])))

class LoginQuitEvent():
    """
    Class for login and quit events
    """

    def __init__(self, date, time, nick, operator, action):
        """
        Constructor. takes:
        * date, of event
        * time, of event
        """
        self.date = date
        self.time = time
        self.nick = nick
        self.operator = operator
        self.action = action

    def __str__(self):
        """
        Return all info
        """
        return "{} {} {} {} {}".format(self.date, self.time, self.nick, self.operator, self.action)

class Message():
    """
    Class for messages
    """

    def __init__(self, date, time, nick, message):
        """
        Constructor
        """
        self.date = date
        self.time = time
        self.nick = nick
        self.message = message

    def __str__(self):
        """
        Return all info
        """
        return "{} {} {} {}".format(self.date, self.time, self.nick, self.message)

class IrcLogParcer():
    """
    Irc log parser
    """
    LOGIN_QUIT = "^(\d\d:\d\d) -!- (.*) \[(.*\.(\w+(.com|.se|.net|.org))|(.*))\] has (joined|quit|left)"
    DATE = "^--- (Log|Day) .*ed [A-z]{3} ([A-z]{3}) (\d\d) (..:..:.. )?(\d\d\d\d)"
    MESSAGE = "^(\d\d:\d\d)\s<(.)([\w-]*)> (.*)$"
    IGNORE = "..... -!- (mode|.* now known as)|--- Log closed|..... -!- Irssi.*|..:.. <.*>$|.+  \* "

    def __init__(self):
        """
        Constructor
        """
        self.file = "ircLog.txt"
        # self.file = "test.txt"
        self.users = []
        self.date = ""
        self.events = []
        self.messages = []

    def parseLoginQuit(self, matchObj):
        """
        Check if line is login or quit. Creates appropriate object
        """
        event = LoginQuitEvent(self.date, matchObj.group(1), matchObj.group(2), matchObj.group(4), matchObj.group(7))
        self.events.append(event)
        self.loginOutUser(event.nick, True if event.action == "joined" else False)
        # print(matchObj.group())
        # print(event)

    def parseMessage(self, matchObj):
        """
        Check if line is message and create appropriate object
        """
        message = Message(self.date, matchObj.group(1), matchObj.group(3), matchObj.group(4))
        self.messages.append(message)
        return message

    def logMessageToUser(self, message, role):
        """
        Add message to user.
        """
        user = self.checkUser(message.nick, role)
        user.messages.append(message)


    def loginOutUser(self, nick, online, role=""):
        """
        try to login or logout user
        """
        self.checkUser(nick, role).online = online


    def checkUser(self, nick, role):
        """
        Check if user exist, otherwise add to list
        """
        user = self.getUser(nick)
        if not user:
            user = self.createUser(nick, role)

        return user

    def createUser(self, nick, role, online=True):
        """
        create user and append to list
        """
        user = User(nick, role, True)
        self.users.append(user)
        return user

    def getUser(self, user):
        """
        Return user if exist. compare with string
        """
        for cuser in self.users:
            if cuser.nick == user:
                return cuser
        return False


    def parseFile(self):
        """
        Parse file
        """
        with open(self.file) as inp:
            for line in inp:

                #Message
                matchObj = re.match(self.MESSAGE, line)
                if matchObj:
                    self.logMessageToUser(self.parseMessage(matchObj), matchObj.group(2))
                    #print(matchObj.group())
                    continue

                #Login/out
                matchObj = re.match(self.LOGIN_QUIT, line)
                if matchObj:
                    self.parseLoginQuit(matchObj)
                    continue

                #ignore mode|known as|Log closed|me messages
                matchObj = re.match(self.IGNORE, line)
                if matchObj:
                    continue

                #New date
                matchObj = re.match(self.DATE, line)
                if matchObj:
                    self.date = matchObj.group(3) + matchObj.group(2) + matchObj.group(5)
                    # print(self.date)
                    continue


                print("UNMATCHED: " + line)

if __name__ == "__main__":
    parser = IrcLogParcer()
    parser.parseFile()
    for x in parser.users:
        x.printInfo()
