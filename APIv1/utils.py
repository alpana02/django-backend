import datetime
import os

def generatetextfile(test_list, url):
    now = datetime.datetime.now()
    if(not(os.path.exists("generatedTextFiles"))):
        os.mkdir("generatedTextFiles")
    fileName = str(now).replace(":",".").replace(" ","_")+".txt"
    with open("generatedTextFiles/"+fileName,"w") as file:
        for sentence in test_list:
            file.write(sentence+'.\n')

    return fileName

def getProcessedSummary(test_list, fileName):
    summaryFileName = "output_"+fileName 
    if(not(os.path.exists("processedTextFiles"))):
        os.mkdir("processedTextFiles")
    with open("processedTextFiles/"+summaryFileName,"w") as file:
        for sentence in test_list:
            file.write(sentence+'.\n')

    return summaryFileName

def readSummaryFile(fileName):
    res = []
    with open("processedTextFiles/"+fileName,"r") as file:
        text = file.read()
    res+=text.split(".\n")
    return res