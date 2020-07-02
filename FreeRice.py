#Created By: Matt Govia (Started on: 7/1/20)
#This version cannot use selenium (as it is blocked from the website)
#therefore, we will have it download the html page everytime, (overwriting the previous one to save space)
#we will use pyautogui at start to download html file, open file, get question and answers, close the file, and answer with pyautogui
#
#Plan:
#get current working directory's path (to find html page)
#At start (or once the freericelogo is spotted), click control-s to save
#the html page, move mouse to drop down menu and move slightly left, type in current directory and hit the save button
#if it already exists, click yes to replace  (have as function either do if (py.locate(confirm_save_as) click yes) or if it exists in directory)
#once downloaded (initially), move cursor to rice bowl (to move it out of the way)
#scan for free rice logo at top, and get the position of each buttons from such place
#click on the button based on the answer and then wait for the score to update (this will be done by taking a screenshot
# of the score and while(new screenshot != old screenshot) wait; (add 1.5 seconds after waiting) )
# or better yet wait a couple seconds, ill figure this out later
#ctrl-s to save page again, and do all over again (will have to overwrite (would hit enter, left arrow, enter; after ctrl-s))


'''make sure saving is as Webpage, Complete'''
import pyautogui as py
from bs4 import BeautifulSoup
import os
import time, shutil
import ctypes
import winsound
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

py.FAILSAFE=True
DaQuestion = ''
DaFirstChoice = 0
DaSecondChoice = 0
DaThirdChoice = 0
DaFourthChoice = 0

first_choice_location = ()
second_choice_location = ()
third_choice_location = ()
fourth_choice_location = ()

DaOldQuestion = ''

RefreshButton = r'images/Refresh.PNG'
DoneSaving = r'images/DoneSaving.PNG'
AfterQuestionPic = r'images/RequestsDone.PNG'
RefreshPageButton = r'images/RefreshPage.PNG'
MenuButton = r'images/ThreeLines.PNG'
DifficultyLevelSetting = r'images/DifficultyLevel.PNG'
EasiestSettingGreen = r'images/EasiestGreen.PNG'
EasiestSettingYellow = r'images/EasiestYellow.PNG'
EasiestSettingRed = r'images/EasiestRed.PNG'
RiceBowl = r'images/RiceBowl.PNG'


def main():
    time.sleep(1.5)
    #firstSaveSite()
    
    
    setButtonLocations()
    saveSite()
    count = 0
    bigboicount = 0
    while(True):
        getChoices()
        answerAndPick()     #answers problem and selects based on such choice
        count += 1
        bigboicount += 1
        waitForQuestion()   #wait until next question comes up
        #if(count > 8):
        #    resetDifficulty()
        #    count = 0
        if(bigboicount>50):
            refreshPage()
            time.sleep(.7)
            bigboicount = 0
        saveSite()          #save page once done waiting, and loop around again
    
    

def resetDifficulty():
    menu = py.locateOnScreen(MenuButton,confidence=.8)
    while menu is None:
        time.sleep(.5)
        menu = py.locateOnScreen(MenuButton,confidence=.8)
    py.click(menu)
    time.sleep(.3)
    diff = py.locateOnScreen(DifficultyLevelSetting,confidence=.8)
    py.click(diff)
    time.sleep(.5)

    loc = py.locateCenterOnScreen(EasiestSettingGreen,confidence=.9)
    if(loc is None):
        loc = py.locateCenterOnScreen(EasiestSettingYellow,confidence=.9)
        if(loc is None):
            loc = py.locateCenterOnScreen(EasiestSettingRed,confidence=.9)
    x,y = loc
    
    py.moveTo(x,y-75)
    py.click()
    py.moveTo(x,y+60)
    py.click()
    daloc = py.locateOnScreen(RiceBowl)
    if daloc is None:
        time.sleep(.1)
        py.click()
    time.sleep(1)
    

def waitForQuestion():
    amt = 0
    timeframe = .5
    while(py.locateOnScreen(AfterQuestionPic) is None):
        amt += timeframe
        time.sleep(timeframe)
        if(amt > 10):
            refreshPage()
            break
    time.sleep(1.7)

def refreshPage():
    for _ in range(0,5):
        py.click(py.locateOnScreen(RefreshPageButton))
        time.sleep(1)

def answerAndPick():
    cc = DaQuestion.split(' ')
    num1, operator, num2 = int(cc[0]), cc[1], int(cc[2])
    ans = 0
    if(operator is '+'):
        ans = num1 + num2
    elif(operator is '-'):
        ans = num1 - num2
    elif(operator is '/'):
        ans = num1 / num2
    elif(operator is 'x'):
        ans = num1 * num2
    else:
        print("holy moly what do i do now?")

    if(ans == DaFirstChoice):
        py.moveTo(first_choice_location,duration=.1)
        py.click()
        #maybe later, move mouse over to see number
    elif(ans == DaSecondChoice):
        py.moveTo(second_choice_location,duration=.1)
        py.click()
    elif(ans == DaThirdChoice):
        py.moveTo(third_choice_location,duration=.1)
        py.click()
    elif(ans == DaFourthChoice):
        py.moveTo(fourth_choice_location,duration=.1)
        py.click()
    else:
        print("Something went wrong again idk bro")
    py.moveTo(py.locateOnScreen(RiceBowl, confidence=.75))

def setButtonLocations():
    global first_choice_location, second_choice_location, third_choice_location, fourth_choice_location
    loc = py.locateOnScreen('images//FreeRice.PNG')
    first_choice_location = (loc[0] + 50, loc[1] + 150)
    second_choice_location = (loc[0] + 50, loc[1] + 210)
    third_choice_location = (loc[0] + 50, loc[1] + 275)
    fourth_choice_location = (loc[0] + 50, loc[1] + 330)

def firstSaveSite():
    #later, add to save file as html only
    py.hotkey('ctrl','s')
    while(py.locateOnScreen(RefreshButton) is None):
        time.sleep(.1)
    py.moveTo(py.locateOnScreen(RefreshButton))
    x,y = py.position()
    py.moveTo(x-50, y,.1)
    py.click()
    curr = os.getcwd()  #since we should be in main directory (idk if save will be or not but thats what we're doing)
    for j in curr:
        py.typewrite(j)

    py.press('enter')
    time.sleep(.1)
    py.press('enter')
    time.sleep(.4)
    waitForDownload()
    
def saveSite():
    #will be called before function and after main(cause it has to download)
    #deleteExtraFolder(), fix later
    py.hotkey('ctrl','s')
    while(py.locateOnScreen(RefreshButton) is None):
        time.sleep(.1)
    py.press('enter',1)
    py.press('left',1)
    py.press('enter',1)
    time.sleep(.5)
    waitForDownload()

def waitForDownload():
    while(py.locateOnScreen(DoneSaving,region = (0,675,50,100), confidence=.9) is None):
        while(py.locateOnScreen(DoneSaving,region = (0,675,50,100), confidence=.9) is None):
            time.sleep(.5)
        time.sleep(.1)
    #goes through twice because chance of it flashing (idk if its done by this time or not but better safe than sorry)

    
def deleteExtraFolder():
    #default I did to save the whole website, so some unneeded files are also being downloaded
    #fix later to not download this
    shutil.rmtree(os.getcwd() + 'Freerice_files')


    
def getChoices():
    global DaQuestion, DaFirstChoice,DaSecondChoice,DaThirdChoice,DaFourthChoice
    with open('Freerice.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    game = soup.find('div', class_='game-block')

    #question holds answers and such too
    actual_game = game.find('div',class_='question')
    question = actual_game.find('div', class_='card-title')
    DaQuestion = question.contents[0]

    choice_list = actual_game.find_all('div', class_='card-button')
    DaFirstChoice = int(choice_list[0].contents[0])
    DaSecondChoice = int(choice_list[1].contents[0])
    DaThirdChoice = int(choice_list[2].contents[0])
    DaFourthChoice = int(choice_list[3].contents[0])

    
    
if __name__ == "__main__":
    main()