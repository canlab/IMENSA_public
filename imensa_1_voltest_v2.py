# === IMENSA PROJECT === 
# Erase BIOPAC part from 'imensa_1_voltest.py'. Used 4/12~

""" 
0. General SETUP 
"""
# === 0a. Import Libraries ===
from __future__ import absolute_import, division
from multiprocessing import dummy
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, sqrt, deg2rad, rad2deg, eye, average, std, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import pandas as pd
import random as rd
from builtins import str, range
import os  # handy system and path functions
import sys  # to get file system encoding
import collections
try:    from collections import OrderedDict
except ImportError:    OrderedDict=dict
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock, prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard


# === 0b. Constants and Togglers ===
debug = 0
autorespond = 0


__author__ = "Byeol Kim"
__version__ = "0.2"
__computer__ = "neurofeedback PC"
__email__ = "byeol.kim.gr@dartmouth.edu"



# === 0c. Autoresponding setup ===
class simKeys:
    ''' an object to simulate key presses
    keyList: a list of keys to watch / name: randomly selected from keyList
    rtRange: [min RT, max RT] where min and max RT are sepecified in ms '''
    def __init__(self, keyList, rtRange):
        self.name=np.random.choice(keyList)
        self.rt = np.random.choice(np.linspace(rtRange[0], rtRange[1])/1000)
thisSimKey=simKeys(keyList=['space'], rtRange=[200,1000])


    
# === 1b. Experimental Dialog Boxes and expInfo ===
expName = 'voltest'
expInfo = {'subject number': '0', 'visit': '1', 'condition': 'p'}
if not debug:
    dlg = gui.DlgFromDict(title="IMENSA study volume practice", dictionary=expInfo, sortKeys=False) 
    if not dlg.OK: 
        core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a timestamp '2021_Dec_27_1947'
expInfo['expName'] = expName


# === 0e. Window setup ===
""" DBIC uses a Panasonic DW750 Projector with a native resolution of 1920x1200 (16:10), but it is configured at 1920x1080 (16:9) at DBIC. Configure a black window with a 16:9 aspect ratio during development (1280x720) and production (1920x1080)"""
if debug == 1:
    win = visual.Window(size=[1280, 720], fullscr=False, 
    # win = visual.Window(size=[1920, 1080], fullscr=False, 
    ### fullscr = False for testing, True for running participants
    screen=0,   # Change this to the appropriate display 
    winType='pyglet', allowGUI=True, allowStencil=True,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True, units='height')
else:
    win = visual.Window(size=[1920, 1080], fullscr=True, 
    screen=4,   # Change this to the appropriate fMRI projector 
    winType='pyglet', allowGUI=True, allowStencil=True,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True, units='height')
frameTolerance = 0.001  # how close to onset before 'same' frame



""" 
1. Experimental Parameters (differ from experiments)
"""

# === 1c. Directory setup ===
_thisDir = os.path.dirname(os.path.abspath(__file__)) 
os.chdir(_thisDir)
main_dir = _thisDir
stimuli_dir = 'C:\\Users\\Dartmouth\\Documents\\imensa\\stimuli'
sub_dir = os.path.join(main_dir, 'scan_data', 'sub%03d' % (int(expInfo['subject number'])), 'sess%01d_%s' % (int(expInfo['visit']), expInfo['condition']))
if not os.path.exists(sub_dir):
    os.makedirs(sub_dir)
psypy_filename = sub_dir + os.sep + u'imensa_sub%03d_sess%01d_volume_test' % (int(expInfo['subject number']), int(expInfo['visit']))

# === 1d. ExperimentHandler ===
### ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='', extraInfo=expInfo, 
    runtimeInfo=None, savePickle=True, saveWideText=True, dataFileName=psypy_filename)


# === 1e. Log for detail verbose info ===
endExpNow = False   # flag for 'escape' or other condition => quit the exp

""" 
2. Stimuli preparation
"""


# === 2a. Movie ===
### make elements and OrderedDict of movie directories
if expInfo['condition'] == 'p':
    condition = 'pos'
if expInfo['condition'] == 'n':
    condition = 'neg'
movie_by_run = []
movie_dict = []
num_stim = 3

movie_dict = [OrderedDict([('file', os.path.join(stimuli_dir,'voltest_1.mp4'))]),
            OrderedDict([('file', os.path.join(stimuli_dir,'voltest_2.mp4'))])] 

# === 2b. Rating parameters ===
stim_size = .5
ratingScaleHeight=.05
rating_pos_y = -0.2
slider_half_size = 0.4
TIME_INTERVAL = 0.005   # Speed at which slider ratings udpate

### cue and rating bar
cue_type = ['warm', 'joyful', 'inspired', 'sad', 'disgusted', 'ashamed', 'horrified']
cum_num = len(cue_type)
cue_list = []
IntensityAnchors = []
for cue_i in range(cum_num):
    cue_list.append(os.path.join(stimuli_dir, "cue", (cue_type[cue_i]+'.png')))
    tmp = visual.ImageStim(win, image=cue_list[cue_i], name='intensityAnchors', 
        size=[np.array([4, 9/4])*stim_size], texRes=512, interpolate=True)
    IntensityAnchors.append(tmp)

volumeAnchors = visual.ImageStim(win, image=os.path.join(stimuli_dir, "cue", "volume.png"), name='intensityAnchors',
        size=[np.array([4, 9/4])*stim_size], texRes=512, interpolate=True)
Rating = visual.Rect(win, height=ratingScaleHeight, fillColor='orange', lineColor='black')
Rating_bar = visual.Rect(win, height=ratingScaleHeight, width=slider_half_size*2, pos=[0, rating_pos_y], fillColor='white', lineColor='black')
IntensityMouse = event.Mouse(win=win)


# === 2c. Instructional TextStim ===
begin_msg = 'We will start a rating practice and volume testing after watching short video clips. You will be watching two documentary video clips and will be asked to respond 7 questions regarding to the previous clip within 6 seconds each. \nIt is important that you watch all the way through and you do not move your head. \nRelax, and please wait for the experimenter to press [Space].'
wait_trigger_msg = 'Please wait. The scan will begin shortly.\nPlease do not move your head. \n Experimenter press [s] to continue.'
in_between_run_msg = 'Please wait for the scanner to stop. \n Remember to please not move your head. \n Experimenter press [e] when stop.'
end_msg = 'Thank you for your participation.\nPlease wait for the experimenter.'

Begin = visual.TextStim(win, name='Begin', text=begin_msg, font='Arial', 
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, color='white', colorSpace='rgb', 
    opacity=1, languageStyle='LTR', depth=0.0, anchorHoriz='center')
wait_trigger_stim_1 = visual.TextStim(win, text=wait_trigger_msg, height=.05, color='white')
wait_trigger_stim_2 = visual.TextStim(win, text=wait_trigger_msg, height=.05, color=[0.1, 0.1, 0.1])
in_between_run_stim = visual.TextStim(win, text=in_between_run_msg, height=0.05)
end_stim = visual.TextStim(win, text=end_msg, height=0.05)


# === 2d. Keyboard and Clocks ===
defaultKeyboard = keyboard.Keyboard()   # to check for escape
Begin_resp = keyboard.Keyboard()

### ticktock
globalClock = core.Clock()              # to track the time since experiment started
routineTimer = core.CountdownTimer()    # to track time remaining of each (non-slip) routine
IntroductionClock = core.Clock()
MovieClock = core.Clock()
RatingClock = core.Clock()
RestingStateClock = core.Clock()
dummy_scan = 5
ratingTime = 6              # Rating Time limit in seconds


"""
3. Start Experimental Loops
    runLoop (prepare the movie order for the run)
    trialLoop (prepare the movie for each trial)
"""

### ------Prepare to start Routine "Introduction"-------
continueRoutine = True
Begin_resp.keys = []
Begin_resp.rt = []
_Begin_resp_allKeys = []
win.mouseVisible = False                        # Turn the mouse cursor off

IntroductionComponents = [Begin, Begin_resp]
for thisComponent in IntroductionComponents:    
    thisComponent.tStartRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

### reset timers
dur = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
IntroductionClock.reset(-_timeToFirstFrame)     # t0 is time of first possible flip
Begin.tStart = globalClock.getTime()

### -------Run Routine "Introduction"-------
while continueRoutine:
    dur = IntroductionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=IntroductionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    
    # *Begin* updates
    if Begin.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Begin.tStartRefresh = tThisFlipGlobal   # on global time
        win.timeOnFlip(Begin, 'tStartRefresh')  # time at next scr refresh
        Begin.setAutoDraw(True)
    
    # *Begin_resp* updates
    waitOnFlip = False
    if Begin_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Begin_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Begin_resp, 'tStartRefresh') # time at next scr refresh
        Begin_resp.status = STARTED  # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(print, "Starting Introduction")
        win.callOnFlip(Begin_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if Begin_resp.status == STARTED and not waitOnFlip:
        theseKeys = Begin_resp.getKeys(keyList=['space'], waitRelease=False)
        _Begin_resp_allKeys.extend(theseKeys)
        if len(_Begin_resp_allKeys):
            Begin_resp.keys = _Begin_resp_allKeys[-1].name  # just the last key pressed
            Begin_resp.rt = _Begin_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # Autoresponder
    if dur >= thisSimKey.rt and autorespond == 1:
        _Begin_resp_allKeys.extend([thisSimKey])  

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:     # a component has requested a forced-end of Routine
        break
    continueRoutine = False     # will revert to True if at least one component still running
    for thisComponent in IntroductionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break       # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

### -------Ending Routine "Introduction"-------
Begin.tStop = globalClock.getTime()
for thisComponent in IntroductionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Begin.start', Begin.tStart)
thisExp.addData('Begin.stop', Begin.tStop)
thisExp.addData('Begin.duration', dur)
# check responses
if Begin_resp.keys in ['', [], None]:   # No response was made
    Begin_resp.keys = None
thisExp.addData('BeginTask.keys',Begin_resp.keys)
if Begin_resp.keys != None:             # we had a response
    thisExp.addData('BeginTask.rt', Begin_resp.rt)
thisExp.nextEntry()

"""
4a. Run Loop Starts, waiting trigger from scanner
"""

wait_trigger_stim_1.draw()          # Automatically draw every frame
win.flip()
bids_data = []  # Start a new BIDS data collection array for each run
run_starttime = globalClock.getTime()

if not autorespond:
    event.waitKeys(keyList = 's')   # experimenter start key
    win.fillColor = 'black'
    win.flip()
    run_starttime = globalClock.getTime()
    core.wait(dummy_scan)                 # Wait 6 TRs, Dummy Scans


# set up handler to look after randomisation of conditions etc
run_starttime = globalClock.getTime()
trialLoop = data.TrialHandler(nReps=1, method='sequential', 
    trialList=movie_dict,
    extraInfo=expInfo, originPath=-1, seed=None, name='trialLoop')
thisExp.addLoop(trialLoop)          # add the loop to the experiment
trialLoop_2 = []


for thisTrialLoop in trialLoop:
    """
    4b. Movie Trial Loop Starts
    """      
    # ================================ MOVIE START ==================================
    # ------Prepare to start Routine "Movie"-------
    continueRoutine = True
    movie = visual.MovieStim3(filename=movie_dict[trialLoop.thisTrialN]['file'],
        win=win, name='movie', noAudio=False, depth=-1.0)
    # movie = loaded_movie
    movie_duration = movie.duration
    if debug:
        movie_duration = 4
    frameN = -1

    MovieComponents = [movie]
    for thisComponent in MovieComponents:
        thisComponent.tStartRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # reset timers
    dur = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    MovieClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    routineTimer.reset()
    routineTimer.add(movie_duration)
    movie.tStart = globalClock.getTime()
    onset = movie.tStart - run_starttime 
    

    # -------Run Routine "Movie"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        dur = MovieClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=MovieClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # *movie* updates
        if movie.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie.frameNStart = frameN  # exact frame index
            movie.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
            movie.setAutoDraw(True)  # start movie, movie.status is changed to STARTED 
            
            if tThisFlipGlobal > movie.tStartRefresh + movie_duration-frameTolerance:
            #     # keep track of stop time/frame for later
                movie.frameNStop = frameN  # exact frame index
                movie.setAutoDraw(False)
        if movie.status == FINISHED:  # force-end the routine
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in MovieComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "Movie"-------
    movie.tStop = globalClock.getTime()
    for thisComponent in MovieComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trialLoop.addData('movie.start', movie.tStart)
    trialLoop.addData('movie.stop', movie.tStop)
    trialLoop.addData('movie.duration', dur)
    movie.stop()
    # thisExp.nextEntry()
    # ================================ MOVIE END ==================================

    rating_part_start = globalClock.getTime()
    trialLoop_2 = data.TrialHandler(nReps=1, method='random', trialList=cue_type, extraInfo=expInfo, originPath=-1, seed=None, name='trialLoop_2')
    thisExp.addLoop(trialLoop_2)          # add the loop to the experiment
    

    for thisTrialLoop_2 in trialLoop_2: 
        """
        4c. Rating Trial Loop Starts
        """      
        # ============================== RATING START ==================================
        # ------Prepare to start Routine "Rating"-------
        continueRoutine = True
        IntensityMouse = event.Mouse(win=win, visible=False) # Re-initialize IntensityMouse
        Rating.startpoint = np.random.choice(101,1)[0] 
        IntensityMouse.setPos((Rating.startpoint/100*2*slider_half_size - slider_half_size,0))
        Rating.width = slider_half_size
        Rating.pos = [-slider_half_size/2, rating_pos_y]
        timeAtLastInterval = 0
        mouseX = 0
        oldMouseX = 0
        timeout = 0

        RatingComponents = [IntensityMouse, Rating, Rating_bar, IntensityAnchors[trialLoop_2.thisIndex]]
        for thisComponent in RatingComponents:
            thisComponent.tStart = None
            thisComponent.tStartRsefresh = None
            thisComponent.tStopRefresh = None                
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")  # very small, 0.00053
        RatingClock.reset(-_timeToFirstFrame)          # set clock as 0.00053
        Rating.tStart = globalClock.getTime()

        # -------Run Routine "Rating"-------
        while continueRoutine:
            timeNow = globalClock.getTime()
            if (timeNow - timeAtLastInterval) > TIME_INTERVAL:
                mouseRel=IntensityMouse.getRel()
                mouseX=oldMouseX + mouseRel[0]
            Rating.pos = ((-slider_half_size + mouseX)/2, rating_pos_y)
            Rating.width = abs((mouseX+slider_half_size))
            if mouseX > slider_half_size:
                mouseX = slider_half_size
            if mouseX < -slider_half_size:
                mouseX = -slider_half_size
            timeAtLastInterval = timeNow
            oldMouseX=mouseX
            sliderValue = (mouseX + slider_half_size) / (slider_half_size*2) * 100

            # get current time
            t = RatingClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=RatingClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            # IntensityAnchors[trialLoop_2.thisIndex].setAutoDraw(True)
            # Rating_bar.setAutoDraw(True)

            # *IntensityAnchors* updates
            if IntensityAnchors[trialLoop_2.thisIndex].status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                IntensityAnchors[trialLoop_2.thisIndex].tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(IntensityAnchors[trialLoop_2.thisIndex], 'tStartRefresh')  # time at next scr refresh
                IntensityAnchors[trialLoop_2.thisIndex].setAutoDraw(True)
            if IntensityAnchors[trialLoop_2.thisIndex].status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > IntensityAnchors[trialLoop_2.thisIndex].tStartRefresh + ratingTime-frameTolerance:
                    # keep track of stop time/frame for later
                    win.timeOnFlip(IntensityAnchors[trialLoop_2.thisIndex], 'tStopRefresh')  # time at next scr refresh
                    IntensityAnchors[trialLoop_2.thisIndex].setAutoDraw(False)
                    timeout = 1


            # *IntensityMouse* updates
            if IntensityMouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                IntensityMouse.tStart = t  # local t and not account for scr refresh
                IntensityMouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(IntensityMouse, 'tStartRefresh')  # time at next scr refresh
                IntensityMouse.status = STARTED
                prevButtonState = IntensityMouse.getPressed()  # if button is down already this ISN'T a new click
            if IntensityMouse.status == STARTED:  # only update if started and not finished!
                if tThisFlipGlobal > IntensityMouse.tStartRefresh + ratingTime-frameTolerance:
                    # keep track of stop time/frame for later
                    IntensityMouse.status = FINISHED
                    timeout = 1
                buttons = IntensityMouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # abort routine on response
                        continueRoutine = False
            
            # *Rating_bar* updates
            if Rating_bar.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Rating_bar.tStart = t  # local t and not account for scr refresh
                Rating_bar.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Rating_bar, 'tStartRefresh')  # time at next scr refresh
                Rating_bar.setAutoDraw(True)
            if Rating_bar.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Rating_bar.tStartRefresh + ratingTime-frameTolerance:
                    # keep track of stop time/frame for later
                    win.timeOnFlip(Rating_bar, 'tStopRefresh')  # time at next scr refresh
                    Rating_bar.setAutoDraw(False)
                    timeout = 1


            # *Rating* updates
            if Rating.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Rating.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Rating, 'tStartRefresh')  # time at next scr refresh
                Rating.setAutoDraw(True)
            if Rating.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Rating.tStartRefresh + ratingTime-frameTolerance:
                    win.timeOnFlip(Rating, 'tStopRefresh')  # time at next scr refresh
                    Rating.setAutoDraw(False)
                    timeout = 1


            # Autoresponder
            if t >= thisSimKey.rt and autorespond == 1:
                sliderValue = random.randint(0,100)
                continueRoutine = False

            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RatingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:
                win.flip()

        # -------Ending Routine "Rating"-------
        Rating.tStop = globalClock.getTime()
        for thisComponent in RatingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store data for thisExp (ExperimentHandler)
        thisExp.addData('rating.dimension',cue_type[trialLoop_2.thisIndex])
        thisExp.addData('rating.starting point', Rating.startpoint)
        thisExp.addData('rating.response', sliderValue)
        thisExp.addData('rating.rt', t)
        thisExp.addData('rating.timeout', timeout)
        thisExp.addData('rating.start', Rating.tStart)
        thisExp.addData('rating.stop', Rating.tStop)
        thisExp.nextEntry()
    
        # ============================== RATING END ==================================
    """
    4bc. Trial Loop Ends
    """

    # ============================== Volume RATING START ==================================
    # ------Prepare to start Routine "Rating"-------
    continueRoutine = True
    IntensityMouse = event.Mouse(win=win, visible=False) # Re-initialize IntensityMouse
    Rating.startpoint = np.random.choice(101,1)[0] 
    IntensityMouse.setPos((0,0))
    Rating.width = slider_half_size
    Rating.pos = [-slider_half_size/2, rating_pos_y]
    timeAtLastInterval = 0
    mouseX = 0
    oldMouseX = 0
    timeout = 0

    RatingComponents = [IntensityMouse, Rating, Rating_bar, volumeAnchors]
    for thisComponent in RatingComponents:
        thisComponent.tStart = None
        thisComponent.tStartRsefresh = None
        thisComponent.tStopRefresh = None                
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")  # very small, 0.00053
    RatingClock.reset(-_timeToFirstFrame)          # set clock as 0.00053
    Rating.tStart = globalClock.getTime()

    # -------Run Routine "Rating"-------
    while continueRoutine:
        timeNow = globalClock.getTime()
        if (timeNow - timeAtLastInterval) > TIME_INTERVAL:
            mouseRel=IntensityMouse.getRel()
            mouseX=oldMouseX + mouseRel[0]
        Rating.pos = ((-slider_half_size + mouseX)/2, rating_pos_y)
        Rating.width = abs((mouseX+slider_half_size))
        if mouseX > slider_half_size:
            mouseX = slider_half_size
        if mouseX < -slider_half_size:
            mouseX = -slider_half_size
        timeAtLastInterval = timeNow
        oldMouseX=mouseX
        sliderValue = (mouseX) / (slider_half_size*2) * 100

        # get current time
        t = RatingClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=RatingClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)

        # *IntensityAnchors* updates
        if volumeAnchors.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            volumeAnchors.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(volumeAnchors, 'tStartRefresh')  # time at next scr refresh
            volumeAnchors.setAutoDraw(True)
        if volumeAnchors.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > volumeAnchors.tStartRefresh + ratingTime-frameTolerance:
                # keep track of stop time/frame for later
                win.timeOnFlip(volumeAnchors, 'tStopRefresh')  # time at next scr refresh
                volumeAnchors.setAutoDraw(False)
                timeout = 1


        # *IntensityMouse* updates
        if IntensityMouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            IntensityMouse.tStart = t  # local t and not account for scr refresh
            IntensityMouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(IntensityMouse, 'tStartRefresh')  # time at next scr refresh
            IntensityMouse.status = STARTED
            prevButtonState = IntensityMouse.getPressed()  # if button is down already this ISN'T a new click
        if IntensityMouse.status == STARTED:  # only update if started and not finished!
            if tThisFlipGlobal > IntensityMouse.tStartRefresh + ratingTime-frameTolerance:
                # keep track of stop time/frame for later
                IntensityMouse.status = FINISHED
                timeout = 1
            buttons = IntensityMouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # abort routine on response
                    continueRoutine = False
        
        # *Rating_bar* updates
        if Rating_bar.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Rating_bar.tStart = t  # local t and not account for scr refresh
            Rating_bar.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Rating_bar, 'tStartRefresh')  # time at next scr refresh
            Rating_bar.setAutoDraw(True)
        if Rating_bar.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Rating_bar.tStartRefresh + ratingTime-frameTolerance:
                # keep track of stop time/frame for later
                win.timeOnFlip(Rating_bar, 'tStopRefresh')  # time at next scr refresh
                Rating_bar.setAutoDraw(False)
                timeout = 1


        # *Rating* updates
        if Rating.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Rating.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Rating, 'tStartRefresh')  # time at next scr refresh
            Rating.setAutoDraw(True)
        if Rating.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Rating.tStartRefresh + ratingTime-frameTolerance:
                win.timeOnFlip(Rating, 'tStopRefresh')  # time at next scr refresh
                Rating.setAutoDraw(False)
                timeout = 1

        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RatingComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:
            win.flip()

    # -------Ending Routine "Rating"-------
    Rating.tStop = globalClock.getTime()
    for thisComponent in RatingComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    bids_data.append((sliderValue))

    # ============================== Volume RATING END ==================================
    
    win.fillColor = 'black'
    win.flip()  
    core.wait(5)

    ### End of one run 

### Wait for T1 ends
in_between_run_stim.draw()
win.callOnFlip(print, "Awaiting experimenter to start next run...")
win.flip()

# Autoresponder
if not autorespond:
    event.waitKeys(keyList = 'e')
    scanner_stop = globalClock.getTime()
    thisExp.nextEntry()

"""
4a. Run Loop Ends
"""
### Save Run File
bids_run_filename = sub_dir + os.sep + u'imensa_sub%03d_sess%01d_volume_test.tsv' % (int(expInfo['subject number']), int(expInfo['visit']))
bids_data = pd.DataFrame(bids_data, columns = ['volume adjust'])
bids_data.to_csv(bids_run_filename, sep="\t")



"""
5. Save data into BIDS .TSV, Excel and .CSV formats and Tying up Loose Ends
""" 
end_stim.draw()
win.flip()

# make sure everything is closed down

core.wait(5)
thisExp.abort()  # or data files will save again on exit
win.close()  # close the window
core.quit()

"""
End of Experiment
"""