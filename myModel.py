import ccm
from ccm.lib.actr import *
import random 
from datetime import datetime
import numpy as np

CONDITIONS = ["Congruent", "Control", "Incongruent"] # the three conditions
TASKS = "WordReading" # Task that is used, options: "ColorNaming" or "WordReading"
t = 5 # the time the agent is allowed to run for 
LATENCIES = [2.61, 2.66, 3.25] # for creating the ColorNaming task
# LATENCIES = [1.95, 2.10, 2.15] # for creating the WordReading task

log=ccm.log()

class MyEnvironment(ccm.Model):
    pass

class MyAgent(ACTR):
    COND = "Control" # choose between "Control", "Congruent", "Incongruent"
    TASK = "WordReading" # choose between "WordReading" and "ColorNaming"
    pr = False # set to true if you wish the process to be printed to the terminal
    
    goal = Buffer()
    rt = Buffer()
    task = Buffer()
    inpt = Buffer()
    outpt = Buffer()
    DMBuffer = Buffer()
    
    DM = Memory(DMBuffer, latency=0.1, threshold=0) # set DM to account for the latencies 
    dm_n = DMNoise(DM, noise=0.0, baseNoise=0.0) # turn on for DM subsymbolic processing
    dm_bl = DMBaseLevel(DM, decay=0.5, limit=None) # turn on for DM subsymbolic processing

    COLORS=['red','green','blue','yellow','purple','brown']

    def init():
        goal.set("start")
        inpt.set("inputWord:None inputColor:None")
        outpt.set("decision:None")
        rt.set('words:0 process:0.0')
        DM.add("memory:None")
    
    # Starting the stimuli of one word 
    # With respect to the condition and task, a word and color is chosen
    def startWord(goal="start"):
        if pr: print "\n\n>>>>>>>> Starting a new word <<<<<<<<\n"
        rt.modify(process=str(float(rt.__getitem__('process'))+0.1))
        getWord = random.choice(COLORS)
        getColor = 'None'
        if COND=="Congruent":
            getColor=getWord
        elif COND=="Incongruent":
            getColor = random.choice(COLORS)
            while getWord==getColor:
                getColor = random.choice(COLORS)
        elif COND=="Control":
            if TASK=="WordReading":
                getColor='None'
            elif TASK=="ColorNaming":
                getColor=COLORS[4]
                getWord='None'
        inpt.modify(inputWord=str(getWord))
        inpt.modify(inputColor=str(getColor))
        if pr: print "Input shown"
        goal.set("input shown")

    # Procedural function to increment the process: look at the color of the word
    def lookAtColor(goal="input shown"):
        if pr: print "I have seen the color"
        rt.modify(process=str(float(rt.__getitem__('process'))+0.2))
        goal.set("color seen")

    # Procedural function to increment the process: read the word
    def readWord(goal="color seen"):
        if pr: print "I have read the word"
        rt.modify(process=str(float(rt.__getitem__('process'))+0.2))
        goal.set("word read")

    # Procedural function to increment the process: remember the task
    def task(goal="word read"):
        if pr: print "I have understood the task"
        rt.modify(process=str(float(rt.__getitem__('process'))+0.2))
        DM.request("memory:?memory")
        goal.set("task understood")

    # Function to decide the answer. Decision is set to either the input word or input color
    def decideWord(goal="task understood", inpt="inputWord:?inputWord inputColor:?inputColor", DMBuffer="memory:?memory"):
        if pr: print "Deciding on the answer"
        if TASK=="WordReading":
            outpt.modify(decision=str(inputWord))
        elif TASK=="ColorNaming":
            outpt.modify(decision=str(inputColor))
        rt.modify(process=str(float(rt.__getitem__('process'))+0.2))
        goal.set("decided")

    # Function to output the decision and restart the process by calling startWord()
    def output(goal="decided", outpt="decision:?decision", inpt="inputWord:?inputWord inputColor:?inputColor"):
        if pr: print "Output the decision"

        if pr: print "Word shown was: ", inputWord, ". Answer was ", decision
        if TASK=="WordReading" and decision==inputWord:
            if pr: print "Answer correct"
        elif TASK=="ColorNaming" and decision==inputColor:
            if pr: print "Answer correct"
        rt.modify(words=str(int(rt.__getitem__('words'))+1))
        if pr: print "Words Correct: ", rt.__getitem__('words')
        rt.modify(process=0.0)
        goal.set("start")

def computeRT(i, condition):
    MyAgent.COND = CONDITIONS[i] # comment this out if you want the default CONDITION
    MyAgent.DM = Memory(MyAgent.DMBuffer, latency=LATENCIES[i], threshold=0) # comment this out if you want the default latency
    
    # define the agent and environment. Run the environment
    agent = MyAgent()
    Env = MyEnvironment()
    Env.agent = agent
    # ccm.log_everything(Env) # comment this out if you don't want to log the environment
    Env.run(t)

    # calculate reaction times
    rt_perWord = (t/(float(agent.rt.__getitem__('words'))+float(agent.rt.__getitem__('process'))))*1000
    rt_perWord = round(np.random.normal(rt_perWord, 30.0), 2)
    print 'Finished | RT per word: ', rt_perWord 
    return rt_perWord        

def main():
    n_repeat = 30 # times to repeat the experiment for each condition
    random.seed(datetime.now()) # set random seed
    RT = {condition: None for condition in CONDITIONS} # reaction times
    if TASK=="ColorNaming":
        file = open("RTCN.txt", "w")  # open a file for the output data
    else if TASK=="WordReading":
        file = open("RTWR.txt", "w")  # open a file for the output data

    # enumerate over the conditions, running the environment for every condition and computing the reaction times
    for i, condition in enumerate(CONDITIONS):
        RT[condition] = np.array([computeRT(i, condition) for j in range(n_repeat)])
        np.savetxt(file, RT[condition], header=str(n_repeat), delimiter=",", newline = "\n")

    file.close()

main()