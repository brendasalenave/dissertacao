# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from webscraping import Extraction
from ontology import Ontology
from analyser import Analyser
from process import Process
from recommendation import Recommendation
import sys
import csv
import pandas as pd
import pandas_profiling


def read_file(file):
    f = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            f.append(row)
    return f

def main():
    if (sys.argv[-1] == '--collect'):
        url_pois = 'https://pt.foursquare.com/explore?mode=url&ne=-29.358988%2C-50.837817&q=Sele%C3%A7%C3%B5es%20principais&sw=-29.41889%2C-50.887942'
        url_city = 'http://www.dataviva.info/pt/location/5rs020102'

        e = Extraction(url_pois, url_city)
        e.poi_data_extraction()
        e.city_data_extraction()

    # Gera relatório do dataset
    file = 'foursquare_data.csv'
    df = pd.read_csv(file, parse_dates=True, encoding='UTF-8')
    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile='dataset_report.html')

    P = Process(file)
    df = P.method()

    df_report = pd.read_csv('preprocessed.csv', parse_dates=True, encoding='UTF-8')
    profile = pandas_profiling.ProfileReport(df_report)
    profile.to_file(outputfile='preprocessed_dataset_report.html')

    R = Recommendation(df)
    R.pattern_recommendation()
    R.new_recommendation()
    R.compare()
    # R.test_rec()

    ont = Ontology()
    ont.write_owl()

if __name__ == '__main__':
    main()
