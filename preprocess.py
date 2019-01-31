#!/usr/bin/envpython3
# coding: utf-8

from __future__ import division
import re
import csv
import math
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
from operator import itemgetter
import unicodedata
from string import punctuation
from string import digits
from datetime import datetime, timedelta
import nltk
import spacy

class Preprocess(object):
    """docstring for Preprocess."""
    def __init__(self, file):
        super(Preprocess, self).__init__()
        self.file = file
        self.p_stemmer = RSLPStemmer()
        self.nlp = spacy.load('pt')
        self.stopwords = nltk.corpus.stopwords.words('portuguese')

    def comment_date(self, date):
        #get year
        if date == 'Date': return 'Date'

        current_year = str(datetime.today()).split('-')[0]
        year = date.split(',')[1].replace(' ','') if len(date.split(',')) > 1 else current_year

        if 'semana' in date:
            a = int(date.split()[0]) * 7
            td = datetime.today()
            delta = td - timedelta(days=a)
            formatted_date = str(delta.day)+'-'+ str(delta.month)+'-'+ str(delta.year)
            return formatted_date
        elif 'dia' in date:
            a = int(date.split()[0])
            td = datetime.today()
            delta = td - timedelta(days=a)
            formatted_date = str(delta.day)+'-'+ str(delta.month)+'-'+ str(delta.year)
            return formatted_date
        elif 'hora' in date:
            td = datetime.today()
            formatted_date = str(td.day)+'-'+ str(td.month)+'-'+ str(td.year)
            return formatted_date

        #get month
        month = str(datetime.today()).split('-')[1]
        if re.search('Janeiro',date): month = '01'
        elif re.search('Fevereiro',date): month = '02'
        elif re.search('Março',date): month = '03'
        elif re.search('Abril',date): month = '04'
        elif re.search('Maio',date): month = '05'
        elif re.search('Junho',date): month = '06'
        elif re.search('Julho',date): month = '07'
        elif re.search('Agosto',date): month = '08'
        elif re.search('Setembro',date): month = '09'
        elif re.search('Outubro',date): month = '10'
        elif re.search('Novembro',date): month = '11'
        elif re.search('Dezembro',date): month = '12'
        #elif re.search('dias',date): month = current_month

        #get_day
        day = date.split()[1].replace(',','')

        formatted_date = day+'-'+month+'-'+year
        # print(formatted_date,date)
        return formatted_date

    # preprocess comment text
    def comment_text(self,text):
        tokenizer = RegexpTokenizer(r'\w+')
        # clean and tokenize document string
        raw = text.lower()
        raw = re.sub("\n|\r", "", raw)
        #print(raw)
        raw = unicodedata.normalize('NFKD', raw).encode('ASCII', 'ignore')
        #raw = (str(raw).replace('b\"','').replace('\'',''))

        raw = " ".join(str(raw).split())

        tokens = tokenizer.tokenize(raw)

        # create stop words list
        filtered_words = [word for word in tokens if word not in self.stopwords]

        text = " ".join(filtered_words)

        # remove digits
        remove_digits = str.maketrans('', '', digits)
        text = text.translate(remove_digits)

        text = self.nlp(text[2:])
        lemmas = [token.lemma_ for token in text]
        text = " ".join(lemmas)
        return text

    def normalize_utf8(self, features):
        normalized = []
        for f in features:
            f = unicodedata.normalize('NFKD', f).encode('ASCII', 'ignore')
            f = re.sub(r'(^b\')|(\'$)|(^b\")|(\"$)','',str(f))
            normalized.append(f)

        return normalized

    def preprocess(self):
        with open(self.file, 'r', newline='') as csvfile:
            seen = set()
            with open ('preprocessed.csv', 'w',newline='') as outputfile:
                writer = csv.writer(outputfile, delimiter=',', quotechar='"')
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in reader:
                    if str(row) in seen:
                        continue #skip duplicate
                    seen.add(str(row))
                    row[0] = row[0].replace('&amp','e')
                    normalized1 = self.normalize_utf8(row[:6])
                    comment = self.comment_text(row[6])
                    date = self.comment_date(row[7])
                    normalized2 = self.normalize_utf8(row[8:])
                    new_row = normalized1 + [comment] + [date] + normalized2
                    writer.writerow(new_row)
