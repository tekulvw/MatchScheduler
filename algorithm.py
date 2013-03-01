#! /usr/bin/env python

"""
So, I'm in a bit of a situatiuon.

This is completely new territory for me, my first major project, 
and im hoping to be able to use this with as few bugs and as best 
results as possible.

Any issues, questions, complaints, comments should be directed to my email:

tekulvw@aol.com

Otherwise, have fun, be fair, and go teams!
"""

import Queue
import thread
import threading
import random

class Algorithm(threading.Thread):

    running = False
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.differential = 0
        self.average = 0.0
        self.rankmap = {}
        self.rankrangemap = {}
        self.options = {}
        self.teams = []
        self.scores = []
        self.matchschedule = [[[]]]
        self.surrogates = []
        
        
                           # So this'll be a 3D array (mindf*** much?)
    def finish_init(self): #[[(blue alliance is first 2 teams)[0, 1, 2, 3], (number of teams)
        self.differential = self.determine_ranks()
        self.matchschedule = [[[0]*(2*self.options['teams_per_alliance']) for x in xrange(len(self.teams))]*self.options['roundnum']]
        
    def DefaultOptions(self):
        return {
            'threadlimit':5,
            'matchseperation':1,
            'teams_per_alliance':2,
            'number_of_teams':0,
            'roundnum':5,
            'surrogate':0
        }
        
    def LoadStuff(self, options, teamlist, scorelist):
        self.options = options.copy()
        self.teams = list(teamlist)
        self.scores = list(scorelist)
        
    def randomNum(self, stop):
        return random.randint(0, stop)
        
    def status(self):
        return self.surrogates
        
    def determine_ranks(self):
        for score in self.scores:
            self.average+=score #We need to calculate our average
        self.average /= len(self.teams)
        self.average = self.average
        for i in xrange(1, 11): #Determines our 1-10 rank values
            self.rankmap[i] = int(self.average*i/10)
        for i in xrange(len(self.teams)): #Assigns each team a value 1-10
            for item in self.rankrangemap.iteritems():
                if self.scores[i] < item[1]:
                    self.rankmap[self.teams[i]] = item[0]
                elif item[0] == 10:
                    self.rankmap[self.teams[i]] = 10
                else:
                    pass
        print "Initialization is finished"
                    
    def schedule_matches(self):
        self.finish_init()
        self.randint = self.randomNum(len(self.teams))
        if (len(self.teams) % (self.options['teams_per_alliance']*2) != 0): #here we are determining the number of surrogate teams
            self.options['surrogate'] = (self.options['teams_per_alliance']*2) - (len(self.teams) % (self.options['teams_per_alliance']*2))
        if self.options['surrogate'] != 0:
            for i in xrange(self.options['roundnum']): #Fill the surrogate list to have different teams as surrogates per round
                for j in xrange(self.options['surrogate']):
                    if self.teams[self.randint] not in self.surrogates: #checks if surrogate team is already in the surrogate list
                        self.surrogates.append(self.teams[self.randint]) #We dont want one surrogate in more than one round
                    else:
                        while self.teams[self.randint] in self.surrogates: #changes next surrogate to make sure there are no more surrogates
                            self.randint = self.randomNum(len(self.teams))
                            
    def run(self):
        print 'Scheduling Algorithm is starting up.'
        self.running = True

        thread.start_new_thread(self.schedule_matches, ())
        
            
