# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:46:23 2019

@author: Pierre
"""
#############################################################
# Bert_Squad_SEO_Score.py
# Anakeyn Bert Squad Score for SEO Alpha 0.1
# This tool provide a "Bert Score" for first max 30 pages responding to a question in Googe.
#This tool is using  Bert-SQuad created by Kamal Raj. We modified  it to calculate a "Bert-Score"
# regarding severall documents and not a score inside a unique document.
# see original BERT-SQuAD : #https://github.com/kamalkraj/BERT-SQuAD
#############################################################
#Copyright 2019 Pierre Rouarch 
 # License GPL V3
 #############################################################
myKeyword="When Abraham Lincoln died and how?"
from bert import QA
 #from bert import QA
n_best_size = 20
#list of pretrained model
#https://huggingface.co/transformers/pretrained_models.html
#!!!!!  instantiate a BERT model  fine tuned on SQuAD
#Choose your model
#'bert-large-uncased-whole-word-masking-finetuned-squad'
#'bert-large-cased-whole-word-masking-finetuned-squad'
model = QA('bert-large-uncased-whole-word-masking-finetuned-squad', n_best_size) 


#import needed libraries
import pandas as pd
import numpy as np
#pip install google  #to install Google Search by Mario Vilas see
#https://python-googlesearch.readthedocs.io/en/latest/
import googlesearch  #Scrap serps
#to randomize pause
import random
import time  #to calcute page time downlod
from datetime import date      
import sys #for sys variables

import requests #to read urls contents
from bs4 import BeautifulSoup  #to decode html
from bs4.element import Comment

#remove comments and non visible tags
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True




###############################################
#  Search in Google  and scrap Urls 
###############################################

dfScrap = pd.DataFrame(columns=['keyword', 'page', 'position', 'BERT_score', 'source', 'search_date'])
myNum=10
myStart=0
myStop=10 #get by ten
myMaxStart=30  #only 30 pages
myLowPause=5
myHighPause=15
myDate=date.today()
nbTrials = 0
myTLD = "com"   #Google tld   -> we search in google.com
myHl = "en" #in english
#this may be long 
while myStart <  myMaxStart:
    print("PASSAGE NUMBER :"+str(myStart))
    print("Query:"+myKeyword)
    #change user-agent and pause to avoid blocking by Google
    myPause = random.randint(myLowPause,myHighPause)  #long pause
    print("Pause:"+str(myPause))
    #change user_agent  and provide local language in the User Agent
    #myUserAgent =  getRandomUserAgent(myconfig.userAgentsList, myUserAgentLanguage) 
    myUserAgent = googlesearch.get_random_user_agent()
    print("UserAgent:"+str(myUserAgent))
    #myPause=myPause*(nbTrials+1)  #up the pause if trial get nothing
    #print("Pause:"+str(myPause))
    try  : 
         urls = googlesearch.search(query=myKeyword, tld=myTLD, lang=myHl, safe='off', 
                                                   num=myNum, start=myStart, stop=myStop, domains=None, pause=myPause, 
                                                   tpe='', user_agent=myUserAgent)
         
         df = pd.DataFrame(columns=['keyword', 'page', 'position', 'BERT_score', 'source', 'search_date'])
         for url in urls :
             print("URL:"+url)
             df.loc[df.shape[0],'page'] = url
         df['keyword'] = myKeyword  #fill with current keyword
        # df['tldLang'] = myTLDLang  #fill with current country / tld lang not use here all in in english
         df['position'] = df.index.values + 1 + myStart #position = index +1 + myStart
         df['BERT_score'] = 0 #not yet calculate
         df['source'] = "Scrap"  #fill with source origin  here scraping Google 
         #other potentials options : Semrush, Yooda Insight...
         df['search_date'] = myDate
         dfScrap = pd.concat([dfScrap, df], ignore_index=True) #concat scraps
         # time.sleep(myPause) #add another  pause
         if (df.shape[0] > 0):
             nbTrials = 0
             myStart += 10
         else :
             nbTrials +=1
             if (nbTrials > 3) :
                 nbTrials = 0
                 myStart += 10
             #myStop += 10
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("ERROR")
        print(exc_type.__name__)
        print(exc_value)
        print(exc_traceback)
       # time.sleep(600) #add a big pause if you get an error.
       #/while myStart <  myMaxStart:


dfScrap.info()
dfScrapUnique=dfScrap.drop_duplicates()  #remove duplicates
dfScrapUnique.info()
#Save
dfScrapUnique.to_csv("dfScrapUnique.csv", sep=",", encoding='utf-8', index=False)  #séparateur ; 
dfScrapUnique.to_json("dfScrapUnique.json")

###### filter extensions
extensionsToCheck = ('.7z','.aac','.au','.avi','.bmp','.bzip','.css','.doc',
                                     '.docx','.flv','.gif','.gz','.gzip','.ico','.jpg','.jpeg',
                                     '.js','.mov','.mp3','.mp4','.mpeg','.mpg','.odb','.odf',
                                     '.odg','.odp','.ods','.odt','.pdf','.png','.ppt','.pptx',
                                     '.psd','.rar','.swf','.tar','.tgz','.txt','.wav','.wmv',
                                     '.xls','.xlsx','.xml','.z','.zip')

indexGoodFile= dfScrapUnique ['page'].apply(lambda x : not x.endswith(extensionsToCheck) )
dfUrls2=dfScrapUnique.iloc[indexGoodFile.values]
dfUrls2.reset_index(inplace=True, drop=True)
dfUrls2.info()
                
#######################################################
# Scrap Urls only one time
########################################################
myPagesToScrap = dfUrls2['page'].unique()
dfPagesToScrap= pd.DataFrame(myPagesToScrap, columns=["page"])
#dfPagesToScrap.size #9
#add new variables
dfPagesToScrap['statusCode'] = np.nan
dfPagesToScrap['html'] = ''  #
dfPagesToScrap['encoding'] = ''  #
dfPagesToScrap['elapsedTime'] = np.nan

for i in range(0,len(dfPagesToScrap)) :
    url = dfPagesToScrap.loc[i, 'page']
    print("Page i = "+url+" "+str(i))
    startTime = time.time()
    try:
        #html = urllib.request.urlopen(url).read()$
         r = requests.get(url,timeout=(5, 14))  #request
         dfPagesToScrap.loc[i,'statusCode'] = r.status_code
         print('Status_code '+str(dfPagesToScrap.loc[i,'statusCode']))
         if r.status_code == 200. :   #can't decode utf-7
             print("Encoding="+str(r.encoding))
             dfPagesToScrap.loc[i,'encoding'] = r.encoding
             if   r.encoding == 'UTF-7' :  #don't get utf-7 content pb with db
                 dfPagesToScrap.loc[i, 'html'] =""
                 print("UTF-7 ok page ") 
             else :
                dfPagesToScrap.loc[i, 'html'] = r.text
                #au format texte r.text - pas bytes : r.content
                print("ok page ") 
                #print(dfPagesToScrap.loc[i, 'html'] )
    except:
        print("Error page requests ") 
                
    endTime= time.time()   
    dfPagesToScrap.loc[i, 'elapsedTime'] =  endTime - startTime
    #/
    
dfPagesToScrap.info()
        
#merge dfUrls2, dfPagesToScrap  -> dfUrls3
dfUrls3 = pd.merge(dfUrls2, dfPagesToScrap, on='page', how='left') 
#keep only  status code = 200   
dfUrls3 = dfUrls3.loc[dfUrls3['statusCode'] == 200]  
#dfUrls3 = dfUrls3.loc[dfUrls3['encoding'] != 'UTF-7']   #can't save utf-7  content in db ????
dfUrls3 = dfUrls3.loc[dfUrls3['html'] != ""] #don't get empty html
dfUrls3.reset_index(inplace=True, drop=True)    
dfUrls3.info() # 
dfUrls3 = dfUrls3.dropna()  #remove rows with at least one na
dfUrls3.reset_index(inplace=True, drop=True) 
dfUrls3.info() #
        
#Remove Duplicates before calculate Bert Score
dfPagesUnique = dfUrls3.drop_duplicates(subset='page')  #remove duplicate's pages
dfPagesUnique = dfPagesUnique.dropna()  #remove na
dfPagesUnique.reset_index(inplace=True, drop=True) #reset index


#Create body from HTML and get Bert_score ### may be long 

dfPagesAnswers = pd.DataFrame(columns=['keyword', 'page', 'position', 'BERT_score', 'source', 'search_date','answers','starts', 'ends', 'local_probs', 'total_probs'])


for i in range(0,len(dfPagesUnique)) :
    soup="" 
    print("Page keyword tldLang  i = "+ dfPagesUnique.loc[i, 'page']+" "+ dfPagesUnique.loc[i, 'keyword']+" "+str(i))
    encoding = dfPagesUnique.loc[i, 'encoding'] #get previously
    print("get body content encoding"+encoding)
    try:
        soup = BeautifulSoup( dfPagesUnique.loc[i, 'html'], 'html.parser')
    except :
        soup="" 
               
    if len(soup) != 0 :
        #TBody Content
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        myBody = " ".join(t.strip() for t in visible_texts)
        myBody=myBody.strip()
        #myBody = strip_accents(myBody, encoding).lower()  #think  to do a global clean instead
        myBody=" ".join(myBody.split(" "))  #remove multiple spaces
        print(myBody)
        dfPagesUnique.loc[i, 'body'] = myBody
        answer = model.predict( dfPagesUnique.loc[i, 'body'],myKeyword)
        print("BERT_score"+str(answer['mean_total_prob']))
        dfPagesUnique.loc[i,  'BERT_score'] = answer['mean_total_prob']
        dfAnswer = pd.DataFrame(answer,  columns=['answers','starts', 'ends', 'local_probs', 'total_probs'])
        dfPageAnswer = pd.DataFrame(columns=['keyword', 'page', 'position', 'BERT_score', 'source', 'search_date','answers','starts', 'ends', 'local_probs', 'total_probs'])
        for k in range (0, len(dfAnswer)) :
            dfPageAnswer.loc[k, 'keyword'] = dfPagesUnique.loc[i,  'keyword']
            dfPageAnswer.loc[k, 'page'] = dfPagesUnique.loc[i,  'page']
            dfPageAnswer.loc[k, 'position'] = dfPagesUnique.loc[i,  'position']
            dfPageAnswer.loc[k,'BERT_score'] = dfPagesUnique.loc[i, 'BERT_score']
            dfPageAnswer.loc[k,'source'] = dfPagesUnique.loc[i,'source']
            dfPageAnswer.loc[k,'search_date'] = dfPagesUnique.loc[i,'search_date']
            dfPageAnswer.loc[k,'answers'] = dfAnswer.loc[k,'answers']
            dfPageAnswer.loc[k,'starts'] = dfAnswer.loc[k,'starts']
            dfPageAnswer.loc[k,'ends'] = dfAnswer.loc[k,'ends']
            dfPageAnswer.loc[k, 'local_probs'] = dfAnswer.loc[k, 'local_probs']
            dfPageAnswer.loc[k, 'total_probs'] = dfAnswer.loc[k, 'total_probs']
        dfPagesAnswers = pd.concat([dfPagesAnswers, dfPageAnswer], ignore_index=True) #concat Pages Answers

dfPagesAnswers.info()
#Save Answers
dfPagesAnswers.to_csv("dfPagesAnswers.csv", sep=",", encoding='utf-8', index=False)    

dfPagesUnique.info()
#Save Bert Scores by page
dfPagesSummary = dfPagesUnique[['keyword', 'page', 'position', 'BERT_score', 'search_date']]
dfPagesSummary.to_csv("dfPagesSummary.csv", sep=",", encoding='utf-8', index=False)         
 #Save page content in csv and json
dfPagesUnique.to_csv("dfPagesUnique.csv", sep=",", encoding='utf-8', index=False)  #sep ,
dfPagesUnique.to_json("dfPagesUnique.json")

