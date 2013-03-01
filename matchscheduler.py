#! /usr/bin/env python

"""
Thank you to motoma for the original idea of layout.
It was SUPER helpful!
"""

# TODO Add functionality for the Add Window
# TODO Make edit button and Window
# TODO Actually work on the algorithm, not just the shiny Tk menu :P

from Tkinter import BooleanVar
from Tkinter import *
from Tkinter import Toplevel
import time
import random

#My import
from algorithm import *

titlestring = "6133 - MatchScheduler"

class MainWindow(Tk): #This is going to be our main window
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "%s" % titlestring)
        
        self.mws = []
        
        self.options = { #Every user input-ed option should be defined here
            'roundnum' : IntVar(),
            'matchseperation' : IntVar(),
            'number_of_teams' : IntVar(),
        }
        
        #Set values for our options here
        self.options['roundnum'] = 5
        self.options['matchseperation'] = 2
        self.options['number_of_teams'] = 28
        
        self.teams = []
        self.scores = []
        
        for i in range(0, self.options.get('number_of_teams')):
            self.teams.append(i+1)
           
        for i in range(0, len(self.teams)): #Both lists MUST be the same size
            self.scores.append(i+2)
            
        self.alliances = [[0] * self.options.get('roundnum') for x in xrange(len(self.teams))] # Generate alliance list filled with blanks
        
        #create our Tk window
        tf = LabelFrame(self, text = 'Team Information', relief = GROOVE, labelanchor = 'nw', width = 550, height = 200)
        tf.grid(row = 0, column = 1)
        tf.grid_propagate(0) #Not sure what this does
        
        #Generate the scrollbar
        scrollbar = Scrollbar(tf, orient=VERTICAL)
        
        #Team Information box
        Label(tf, text = 'Team Number').grid(row = 0, column = 1)
        self.teambox = Listbox(tf, selectmode = SINGLE, yscrollcommand=scrollbar.set)
        self.teambox.grid(row = 1, column = 1)
        for team in self.teams: #Populate the teambox
            self.teambox.insert(END, team)
            
        self.teambox.bind("<MouseWheel>", self.onMouseWheel) # Bind the mouse scrolls to all Listbox's
        self.teambox.bind("<Button-4>", self.onMouseWheel)
        self.teambox.bind("<Button-5>", self.onMouseWheel)
            
        #Pre-Round Score box
        Label(tf, text = 'Pre-Round Score').grid(row = 0, column = 2)
        self.scorebox = Listbox(tf, selectmode = SINGLE, yscrollcommand=scrollbar.set)
        self.scorebox.grid(row = 1, column = 2)
        for score in self.scores: #Populate the scorebox
            self.scorebox.insert(END, score)
            
        self.scorebox.bind("<MouseWheel>", self.onMouseWheel) # Bind the mouse scrolls to all Listbox's
        self.scorebox.bind("<Button-4>", self.onMouseWheel)
        self.scorebox.bind("<Button-5>", self.onMouseWheel)
        
        #Best Alliance members box
        Label(tf, text = 'Best Choice Allies').grid(row = 0, column = 3)
        self.alliancebox = Listbox(tf, selectmode=SINGLE, yscrollcommand=scrollbar.set)
        self.alliancebox.grid(row=1, column=3)
        
        self.alliancebox.bind("<MouseWheel>", self.onMouseWheel) # Bind the mouse scrolls to all Listbox's
        self.alliancebox.bind("<Button-4>", self.onMouseWheel)
        self.alliancebox.bind("<Button-5>", self.onMouseWheel)
        
        for i in xrange(len(self.alliances)): #Fill alliance list
            ret = ""
            for j in xrange(self.options.get('roundnum')):
                randint =  random.randint(0, len(self.teams)-1) #Generate random teams to be paired for alliances
                self.alliances[i][j] = self.teams[randint]
                if j < self.options.get('roundnum')-1:
                    ret += str(self.alliances[i][j])+", "
                elif j == int(self.options.get('roundnum'))-1:
                    ret += str(self.alliances[i][j])
            self.alliancebox.insert(END, ret)
            
        #Assign the scrollbar to teambox
        scrollbar.config(command=self.yview)
        scrollbar.grid(row=1, column=4, sticky=N+S)
        
        #Now that our 'view' window is done, we need to introduce the buttons to be able to add/edit data
        dmf = LabelFrame(self, text = "Data Manipulation", relief = GROOVE, labelanchor = 'nw', width = 550, height = 100)
        dmf.grid(row = 1, column = 1)
        dmf.grid_propagate(0)
        Label(dmf, text = "").grid(row = 2, column = 1)
        Button(dmf, text = "Add", command=self.add).grid(row = 3, column = 1)
        
        #Edit button
        Button(dmf, text = "Edit", command=self.edit).grid(row = 3, column = 2)
        
        #Start button
        Button(dmf, text = "Start", command=self.start).grid(row = 3, column = 3)
        
    def yview(self, *args): #Modify the scrollbar positions of both lists simultaneously
        self.teambox.yview(*args)
        self.scorebox.yview(*args)
        self.alliancebox.yview(*args)
        
    def onMouseWheel(self, event):
        if (event.num == 4 or event.num == 120): #Linux
            delta = -1
        elif (event.num == 5 or event.num == -120):
            delta = 1
        else:                   # Windows & OSX
            delta = event.delta
            
        self.teambox.yview("scroll", delta, "units")
        self.scorebox.yview("scroll", delta, "units")
        self.alliancebox.yview("scroll", delta, "units")
        
        return "break" # So as not to repeat the event
        
    def add(self):
        self.mws.append(AddWindow())
        
    def edit(self):
        if self.teambox.curselection(): #Checks and decides which box to draw data from
            self.mws.append(EditWindow(self.teambox.curselection()[0], self.teams, self.alliances, self.scores))
        elif self.scorebox.curselection():
            self.mws.append(EditWindow(self.scorebox.curselection()[0], self.teams, self.alliances, self.scores))
        else: return
        
    def start(self):
        self.mws.append(RunWindow(self.options, self.teams, self.scores))
        
    def checkloop(self):
        thread.start_new_thread(self.check, ())

    def check(self):
        while True:
            for mw in self.mws:
                mw.check()
            time.sleep(1)
        
class AddWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title(string = "%s" % titlestring)
        self.options = {
            'teamnum':IntVar(),
            'prescore':IntVar(),
            'label':StringVar(),
        }
        
        # Now to make the GUI for adding a team
        af = LabelFrame(self, text = "Add a new team", relief=GROOVE, labelanchor="nw", width = 400, height = 150)
        af.grid(row = 0, column = 0)
        af.grid_propagate(0)
        Label(af, text = "Team Number:").grid(row=0, column = 1)
        Entry(af, textvariable = self.options['teamnum']).grid(row = 0, column = 2) #Team number input
        
        Label(af, text = "Pre-Round Score:").grid(row = 1, column = 1)
        Entry(af, textvariable = self.options['prescore']).grid(row = 1, column = 2) #Pre round score input
        
        Label(af, text = "", textvar = self.options['label']).grid(row = 2, column = 2)
        
        Button(af, text = "Submit", command = self.submit).grid(row = 3, column = 2)
        
    def submit(self):
        if self.options['teamnum'].get() != 0: # Need to add functionality
            self.destroy()
        else:
            self.options['label'].set("Team Name must not be 0!")
            
class EditWindow(Toplevel):
    def __init__(self, teamnum, teams, alliances, scores):
        Toplevel.__init__(self)
        self.title(string = "%s" % titlestring)
        
        self.teamnum = int(teamnum)
        self.teamnumber = teams[self.teamnum]
        self.score = scores[self.teamnum]
        
        self.elements = { # motoma!
            'teamnumber':IntVar(),
            'prescore':IntVar(),
        }
        
        self.elements['teamnumber'].set(self.teamnumber)
        self.elements['prescore'].set(self.score)
        
        # Starting our editing frame
        ef = LabelFrame(self, text = "Edit Team Information", relief=GROOVE, labelanchor="nw", width = 400, height = 150)
        ef.grid(row = 0, column = 0)
        ef.grid_propagate(0)
        
        Label(ef, text = "Team Number:").grid(row = 0, column = 1)
        Entry(ef, text = "%s" % self.teamnumber, textvar = self.elements['teamnumber']).grid(row = 0, column = 2)
        
        Label(ef, text = "Pre-Round Score:").grid(row = 1, column = 1)
        Entry(ef, text = "%s" % self.score, textvar = self.elements['prescore']).grid(row = 1, column = 2)
        
        Label(ef, text = "").grid(row = 2, column = 1)
        Button(ef, text = "Submit", command=self.submitchanges).grid(row = 3, column = 2)
        
    def submitchanges(self):
        self.destroy()
        
class RunWindow(Toplevel):
    def __init__(self, options, teams, scores):
        Toplevel.__init__(self)
        self.title(string = titlestring)
        self.elements = {
            'surrogates': StringVar(),
        }
        
        self.elements['surrogates'].set('N/A')
       
        self.algo = Algorithm()
        self.algo.start()
        
        self.algoOptions = self.algo.DefaultOptions()
        for key in options.keys():
            self.algoOptions[key] = options[key]
        self.algo.LoadStuff(self.algoOptions, teams, scores)
        
        rw = LabelFrame(self, text = "Current Information", relief=GROOVE, labelanchor="nw", width = 400, height = 150)
        rw.grid(row = 0, column = 0)
        rw.grid_propagate(0)
        
        Label(rw, text = "Surrogate Teams:").grid(row = 1, column = 1)
        Label(rw, text = "N/A", textvar = self.elements['surrogates']).grid(row = 1, column = 2)
        
    def check(self):
        while True:
            try:
                status = self.algo.status()
                if status[0]:
                    self.elements['surrogates'].set(str(status[0]))
                else:
                    pass
                time.sleep(1)
            except:
                pass
        
if __name__ == '__main__':
    try:
        mw = MainWindow()
        mw.checkloop()
        mw.mainloop()
    except Exception, ex:
        print('There was an error: %s.\nQuitting.' % ex)
