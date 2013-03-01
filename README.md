MatchScheduler
==============
-
My attempt at improving FIRST's current system of Match Selection
-
==============

As of now, the Scheduler only has a semi-functional GUI, and a 
randomized alliance selection that is completely randomized.

Currently I am working on the algorithm to derive team alliances using 
my own ranking system of 1-10. These ranks are determined by finding the 
difference in "pre-score" from the average, where "pre-score" is 
simply the allies first round score minus their opponents first round score.
Hopefully this integrates a bit more fairness into the random equation of 
alliances.

-
Usage
-

**Linux**

Simply mark matchscheduler.py as executable and run. Python 2.X is needed, 
download from http://python.org/download/

-

**Windows**

I'll be providing a converted .exe in a couple of days, for now, download
 Python 2.X at the above link and run `C:\Python2X\python.exe matchscheduler.py`
 from Command Line
