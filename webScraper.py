from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import platform
import sys
import requests
import calendar
import time
import xlwt
import os

def clear():
    btnRun['highlightbackground'] = 'blue'
    root.after(200, reset_color)
    root.destroy()

def PlayedThisWeek(tt):
    t = int(calendar.timegm(time.gmtime())-int(tt))
    t = t/(60*60*24)
    return t < 7.2

def reset_color():
    setPlayers['highlightbackground'] = 'white'
    btnRun['highlightbackground'] = 'white'

def saveChanges():
    setPlayers['highlightbackground'] = 'blue'
    root.after(200, reset_color)


    input = PlayerFile.get("1.0",'end-1c')
    f= open("players.txt","w+")
    f.write(input)
    f.close()

#setting up GUI


root = tk.Tk()
btn_text = tk.StringVar()
btn_text.set("Run")
headless = tk.IntVar()
#player List
PlayerFile = tk.Text(root, width=45, height= 20)

with open("players.txt", 'r') as f:
    PlayerFile.insert(tk.END, f.read())


label = tk.Label(root, text = "The Players")
#buttons
setPlayers = tk.Button(root, text="Save Changes", command=saveChanges)
btnRun = tk.Button(root, textvariable=btn_text, command=clear)
headOrLess = tk.Checkbutton(root, text="Run Headless?", variable=headless)

label.pack()
PlayerFile.pack(fill="none", expand=True)
setPlayers.config(bg = 'lightgrey')
#EditPlayers.pack()
setPlayers.pack()
headOrLess.pack()
btnRun.pack()

root.geometry("550x400+200+150")
root.mainloop()

#get player names

if (getattr(sys,'frozen', False)):
    path = sys._MEIPASS + "/players/players.txt"
    file = open(path,"r")
    names = file.readlines()
    file.close()
else:
    file = open("players.txt","r")
    names = file.readlines()
    file.close()

global readyToRun
readyToRun = "no"
#setting up globals
totalRuns = len(names)
runs = 1
#time
global firstTS
firstTS = 0
global secondTS
#result
global firstwinOrLoss
firstwinOrLoss = ''
global secondwinOrLoss
#KDA
global firstKDA
firstKDA = 0
global secondKDA
#KDratio
global firstKDratio
firstKDratio = 0
global secondKDratio
#MVP
global firstMVP
firstMVP = ""
global secondMVP
#champion
global firstChamp
firstChamp = ""
global secondChamp
#game time
global firstGameTime
firstGameTime = 0
global secondGameTime
#CSperMin
global firstCS
firstCS = 0
global secondCS
#kill participation
global firstKPA
firstKPA = ""
global secondKPA
#multiKill
global firstMultiKill
firstMultiKill = ""
global secondMultiKill
#control wards
global firstCW
firstCW = 0
global secondCW

global points
points = 0;

#setting up workbook
wb = xlwt.Workbook()
sheet = wb.add_sheet("sheet1")#formatting sheet
for i in range(0, 17):
    sheet.col(i).width = 256*30

global row
row = 0


chrome_options = Options()
if(headless.get() == 1):
    chrome_options.add_argument("--headless")
#chrome_options.add_extension('')

while(len(names) > 0): #getting all our players and running for each one

    runs = runs + 1
    gameList =[]
    mark = 0;
    currentPlayer = names.pop(0).strip()
    print("There are " + str(len(names)+1) + "/" + str(totalRuns) + " players left. On - " + currentPlayer)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://na.op.gg/summoner/userName='+ currentPlayer)


    #updating the page
    lastUpdated = browser.find_element_by_xpath("//*[@class = 'LastUpdate']")

    if(lastUpdated.text.find("minute") >= 0 or lastUpdated.text.find("second") >= 0):
        time.sleep(.01)
    else:
        print("here we are...waiting")
        browser.find_element_by_xpath("//*[@class='Buttons']//*[@class='Button SemiRound Blue']").click()
        #WebDriverWait(browser, 30000).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@class='Buttons']//*[@class='Button SemiRound Blue']")))
        time.sleep(6)
        print("Done waiting!")
    #loading all the matchers
    runs = 0 # cap at 3 "loadmore"s
    while(len(browser.find_elements_by_xpath("//*[@class='GameMoreButton Box']")) > 0 and runs < 3):
        loadMore = browser.find_element_by_xpath("//*[@class='GameMoreButton Box']")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        loadMore.click()
        #print("loading...")
        browser.implicitly_wait(6)
        time.sleep(5)
        runs = runs +1


    page = BeautifulSoup(browser.page_source,'lxml')

    #print("current time: " + str(calendar.timegm(time.gmtime())- (4*60*60)))
    #print("New Player is : " + currentPlayer)
    #print()





    for gameItem in page.find_all('div', class_=('GameItemWrap')):
        x = 0
        game = gameItem.find('div', class_=('GameStats'))
        gameSettings = gameItem.find('div', class_=('GameSettingInfo'))
        stats = gameItem.find('div', class_='Stats')
        gameKDA = gameItem.find('div', class_='KDA')
        multiKill = gameKDA.find_all('div', class_='MultiKill')
        MVP = gameKDA.find_all('div', class_='Badge')
        wards = gameItem.find_all('span', class_='wards vision')


        kills = int(gameKDA.find('span', class_="Kill").text)
        deaths = int(gameKDA.find('span', class_="Death").text)
        assists = int(gameKDA.find('span', class_="Assist").text)


        #print(stats.text.strip())
        stats = stats.text.strip()
        TotalCS = stats[stats.find('(')-4:stats.find('(')-1].strip()
        CSPerMin = stats[stats.find("(")+1:stats.find(")")]
        if(float(CSPerMin) == 0):
            CSPerMin = int(CSPerMin) +1
        gametime = round(int(TotalCS) / float(CSPerMin),2)
#       print(TotalCS + " (CS)")
#       print(CSPerMin + " (CS Per Min)")
#       print(str(gametime) + "mins")

        KPA = stats[stats.find("P")+7: stats.find("%")]
#      print(KPA + "%")
#       print()


        #print(gameItem.find_element_by_xpath("//*[@class='ChampionName'] //a/@href"))
        #print(gameSettings.find_element_by_xpath("//a[contains(@href,'/champion/')]"))
        champion = gameSettings.find('div', class_=('ChampionName'))
        #print(champion.text)
        tmp = game.find('div', class_=('GameType')).text
        #print ( "game Type " + (game.text))

        if(tmp.strip() == "Ranked Solo"):
            # print (tmp.strip())
            # print (game.find('div', class_=('TimeStamp')).text)
            winOrLoss = game.find('div', class_=('GameResult')).text.strip()
            # print (winOrLoss)


            TS =  game.find('div', class_=('TimeStamp'))
            TS = str(TS)
            TS = TS[TS.find('data-datetime="')+len('data-datetime="'):TS.find('data-interval')-2]
            # print(TS)
            #print(TS.getAttribute("data-datetime"))




            #kills   = k.pop(0).text
            #deaths  = d.pop(0).text
            #assists = a.pop(0).text



            #storing game data only for the first two games of the week
            # remove this when The class is removed
            if(PlayedThisWeek(TS) and winOrLoss != "Remake"):#EPOC time
                secondTS = firstTS
                firstTS = TS

                secondwinOrLoss = firstwinOrLoss
                firstwinOrLoss = winOrLoss

                secondKDA = firstKDA
                firstKDA= (str(kills) + "/"  +str(deaths) + "/" + str(assists))

                secondKDratio = firstKDratio
                firstKDratio = (int(kills)+int(assists))/float(deaths) if int(deaths) > 0 else int(kills)+int(assists)



                secondChamp = firstChamp
                firstChamp = champion.text.strip()

                if(len(MVP) > 0):
                    secondMVP = firstMVP
                    firstMVP = MVP[0].text
                else:
                    secondMVP = firstMVP
                    firstMVP = "---"

                if(len(multiKill) > 0):
                    secondMultiKill = firstMultiKill
                    firstMultiKill = multiKill[0].text
                else:
                    secondMultiKill = firstMultiKill
                    firstMultiKill = "None"
                    #not currently printed
                secondCS = firstCS
                firstCS = CSPerMin

                secondKPA = firstKPA
                firstKPA = KPA

                secondGameTime = firstGameTime
                firstGameTime = gametime
                if(len(wards) > 0):
                    secondCW = firstCW
                    firstCW = wards[0].text


    #end for

    browser.close()

    if(str(firstwinOrLoss) != str(secondwinOrLoss)):
        score = ("1,1")
        points = 5;
    elif(str(firstwinOrLoss) == "Victory"):
        score = ("2,0")
        points = 10;
    else:
        score = ("0,2")
        points = 0
    print(currentPlayer + "\'s first two games were: " + score)
    #print(firstTS)
    print(firstwinOrLoss)
    print(firstKDA)
    print()
    #print(secondTS)
    print(secondwinOrLoss)
    print(secondKDA)
    print()

    #standard points
    if(firstKDratio > 4):
        points += 1
    if (secondKDratio > 4):
        points += 1

    if(int(firstKPA) > 55):
        points += 1
    if(int(secondKPA) > 55):
        points += 1

    if(firstMVP == "MVP" or firstMVP == "ACE"):
        points += 1
    if(secondMVP  == "MVP" or secondMVP == "ACE"):
        points += 1

    if(float(firstCS) > 6.5):
        points += 1
    if(float(secondCS) > 6.5):
        points += 1
    #Bonus points
    if(firstMultiKill == "Penta Kill"):
        points += 2
    if(secondMultiKill == "Penta Kill"):
        points += 2

    if(int(firstKPA) == 100):
        points += 2
    if(int(secondKPA) == 100):
        points += 2

    if(float(firstCS) >= 11):
        points += 2
    if(float(secondCS) >= 11):
        points += 2

    if(int(firstKDA[0:firstKDA.find('/')]) >= 20):
        points +=2
    if(int(secondKDA[0:secondKDA.find('/')]) >= 20):
        points +=2

    if(int(firstKDA[firstKDA.rfind('/')+1:]) >= 40):
        points +=2
    if(int(secondKDA[secondKDA.rfind('/')+1:]) >= 40):
        points +=2

    style = xlwt.easyxf('align: horiz center; borders: left thin, right thin, top thin, bottom thin;')
    sheet.write(row,0, currentPlayer, style)
    sheet.write(row,1, score, style)
    sheet.write(row, 2, points, style)
#champion and KDA
    sheet.write(row,3, firstKDA + " as " + firstChamp, style)
    sheet.write(row,10, secondKDA + " as " + secondChamp, style)
#mvp
    sheet.write(row,4, firstMVP , style)
    sheet.write(row,11, secondMVP , style)
#multi-kills
    sheet.write(row,5, firstMultiKill , style)
    sheet.write(row,12, secondMultiKill , style)
#KPA
    sheet.write(row,6, "KPA: " + firstKPA + "%", style)
    sheet.write(row,13, "KPA: " + secondKPA + "%", style)
#CS
    sheet.write(row,7, "CS per Min: "  + firstCS, style)
    sheet.write(row,14, "CS per Min: "  + secondCS, style)
#control wards
    sheet.write(row,8, "Control wards "  + firstCW, style)
    sheet.write(row,15, "Control wards " + secondCW, style)
#gameTime
    sheet.write(row,9, "Game Time:" + str(firstGameTime), style)
    sheet.write(row,16, "Game Time:" +  str(secondGameTime), style)


    row = row+1


#end while

wb.save("WebScraperResults.xls")
if(platform.system() == "Windows"):
    os.system("webScraperResults.xls")
else:
    os.system("open webScraperResults.xls")
browser.quit()
print("Program complete")
