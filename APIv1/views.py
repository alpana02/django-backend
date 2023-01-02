from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Website,Sentences
import json

from bs4 import BeautifulSoup
import requests
import re
import random
# Create your views here.

@csrf_exempt
def uploadUrl(request): 
    # urlName = json.loads(request.body.decode('utf-8'))['urlName']
    url= json.loads(request.body.decode('utf-8'))['url']
    print(url,"------------>")
    obj = Website(url = url)
    obj.save()
    res = generateSentences(url)

    for r in res : 
        s = Sentences(sentenceText = r, website =  obj)
        s.save()

    sentences = list(Website.objects.get(id = obj.id).sentences_set.all())
    sentences = random.sample(sentences, 7)

    for s in sentences:
        s.selected = True
        s.save()

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
    # for tag in child_elements:
    #     for element in soup.select(tag):
    #         text.append(re.sub('\s+', ' ', element.text.strip()))

    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # desried_divs = []
    # desried_divs = soup.find_all("div", class_="tailwind-article-body")

    # text = []
    # for tag in desried_divs:
    #     text.append((re.sub('\s+'," ",tag.text.strip())))
    # text = text[0].split(".")
    # return text

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
