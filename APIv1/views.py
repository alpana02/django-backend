from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Website,Sentences
import json, os
from PyPDF2 import PdfReader, PdfFileWriter
from .utils import *

from bs4 import BeautifulSoup
import requests
import re
import random
# Create your views here.

@csrf_exempt
def uploadUrl(request): 
    # urlName = json.loads(request.body.decode('utf-8'))['urlName']
    url= json.loads(request.body.decode('utf-8'))['url']
    if(len(Website.objects.filter(url = url))==0):
        obj = Website(url = url)
        obj.save()
        res, fileName = generateSentences(url)
        obj.textFilePath = fileName
        obj.save()
        for r in res : 
            s = Sentences(sentenceText = r, website =  obj)
            s.save()

        summaryFileName = getProcessedSummary(res,fileName)
        obj.summaryFilePath = summaryFileName
        obj.save()

        # sentences = list(Website.objects.get(id = obj.id).sentences_set.all())
        # sentences = random.sample(sentences, 7)
        sentences = readSummaryFile(obj.summaryFilePath)

        for s in list(Website.objects.get(id = obj.id).sentences_set.all()):
            if s.sentenceText in sentences:
                s.selected = True
                s.save()
    else:
        obj = Website.objects.get(url = url)

    return JsonResponse({'objectId' : obj.id})


@csrf_exempt
def uploadPdf(request): 
    # urlName = json.loads(request.body.decode('utf-8'))['urlName']
    # url= json.loads(request.body.decode('utf-8'))['url']
    # pdf= json.loads(request.body.decode('utf-8'))['file']
    pdf = request.FILES['file']
    obj = Website(pdf = pdf)
    obj.save()
    # print(request.FILES['file'] ,"________________________________________")
    if(len(Website.objects.filter(pdf = pdf))==0):
        # print(obj.pdf.url,"+++++++++++++++++++++++++")
        res = generateSentencesPdf(obj.pdf.url)
        # res = ["jdshjsdk","sdhfkjdsh"]
        for r in res : 
            s = Sentences(sentenceText = r, website =  obj)
            s.save()

        sentences = list(Website.objects.get(id = obj.id).sentences_set.all())
        sentences = random.sample(sentences, 7)


        for s in sentences:
            s.selected = True
            s.save()
    else:
        obj = Website.objects.get(pdf = pdf)

    return JsonResponse({'objectId' : obj.id})

def getAllSentences(request,websiteId):
    print(request)
    print("asuchi",websiteId)
    # sentences = Website.objects.get(id = websiteId).sentences_set.all()
    # items = list(Website.objects.get(id = websiteId).sentences_set.all())
    # random_items = random.sample(items, 3)
    # random_item = random.choice(items)

    # sentences = list(Website.objects.get(id = websiteId).sentences_set.all())
    # sentences = random.sample(sentences, 13)
    sentences = Website.objects.get(id = websiteId).sentences_set.all()
    d = []
    for s in sentences:
        d.append( {
            'sentenceText' : s.sentenceText,
            'selected' : s.selected,
            'sentenceId' : s.id
        })
    return JsonResponse(d, safe=False)

child_elements = ['h1','h2','h3','h4','h5','p']
def generateSentences (url):
    text = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    current_sibling = soup.find('h2', text='Prepared Remarks:')
    text = []
    while (current_sibling.next_sibling != soup.find('h2', text='Questions and Answers:')):
        if current_sibling.name == "p":
            text.append(current_sibling.next_sibling.text.strip())
        current_sibling = current_sibling.next_sibling

    res = []
    for s in text:
        res+=(s.split(". "))

    test_list = [i for i in res if i]
    fileName = generatetextfile(test_list,url)
    return (test_list, fileName)


def generateSentencesPdf (url):
    # print(url,"-----------------------")
    # url.replace("/","\\")
#     url = url.replace("/","\\")
#     print(url,"++++++++++++++++++++++++++")
#     x = "media\\uploadedPdf\\Undertakingbystudents_v50m5Fb.pdf"
    url = os.path.join(os.getcwd(), 'django-backend' ,url[1:])
    os.system('pwd')
    os.system('ls ./django-backend/APIv1/uploadedPdf')
    pdf = PdfReader(url)
    text = []
    for page_num in range(len(pdf.pages)):
        pageObj = pdf.pages[page_num]
        text.append(pageObj.extract_text())
    res = []
    for s in text:
        if(s=='\n'):
            continue
        else:
            res+=(s.split(". "))

    test_list = [s.replace('\n', '') for s in res]
    return (test_list)

def updateSelectedSentence(request,sentenceId):
    sentence = Sentences.objects.get(id = sentenceId)
    sentence.selected = not(sentence.selected)
    sentence.save()

    return JsonResponse({"success" : True})


def summary(request,websiteId):

    sentences = Website.objects.get(id = websiteId).sentences_set.all()
    print(sentences)
    d = []
    filteredSentence = []
    for s in sentences:        
        if(s.selected):
            filteredSentence.append({'sentenceText' : s.sentenceText,
            'selected' : s.selected,
            'sentenceId' : s.id})
            d += [s.sentenceText]

    d = '.'.join(d)
    return JsonResponse({"paragraph" : d, "sentence" : filteredSentence})


#name
#wesbiteurl
#setences
