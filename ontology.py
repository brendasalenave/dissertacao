# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import csv

class Ontology(object):
    """docstring for Ontology."""
    def __init__(self):
        super(Ontology, self).__init__()
        #self.arg = arg

    def write_owl(self):
        self.write_city_data()
        #self.write_poi_data()

    def write_city_data(self):
        rows_city = []
        with open('city_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for r in reader:
                rows_city.append(r)

        for x in rows_city:
            print(x)

        rows_pois = []
        with open('preprocessed.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for r in reader:
                rows_pois.append(r)
        # print(type(rows[0][1]))

        # e = rows_pois[1][0].replace(' ','_')
        # print(e)
        food_category = ['Pub Gastronomico','Italiano','Chocolataria', 'Restaurante']
        accommodation_category = ['Hotel', 'Albergue', 'Pousada']
        outdoor_category = ['Praca','Lago']
        culture_category = ['Museu']

        e_names = []
        for i in range(len(rows_pois)-1):
            e = rows_pois[i+1][0].replace(' ','_')
            print(e)
            e_names.append(e)
            category = rows_pois[i+1][1]
            if category in food_category:
                category = 'Food'
            elif category in accommodation_category:
                category = 'Accommodation'
            elif category in outdoor_category:
                category = 'Outdoor'
            elif category in culture_category:
                category = 'Culture'
            self.named_individual(e)
            self.class_assertion('POI',e)
            self.object_property_assertion('POI','contemplates', e, category)


        city_name = rows_city[0][1].split(' - ')[0]
        self.named_individual(city_name)
        self.class_assertion('City',city_name)
        for e in e_names:
            self.object_property_assertion('City','hasPOIs', city_name, e)
        self.data_property_assertion('POI','description',city_name, rows_city[1][1])

        # self.data_property_assertion('City','description',city,rows_city[1][1])

    def object_property_assertion(self, class_owl, property_assertion, individual, property):
        file = './ontology/smart_city_ontology.owl'
        inputfile = open(file, 'r').readlines()
        write_file = open(file,'w')
        flag = 0
        for line in inputfile:
            write_file.write(line)
            if 'ClassAssertion(' in line and class_owl in line and not flag:
               new_line = 'ObjectPropertyAssertion(:'+property_assertion+' :'+individual+' :'+property+')'
               write_file.write(new_line + "\n")
               flag = 1
        write_file.close()

    def data_property_assertion(self, class_owl, property_assertion, individual, property):
        file = './ontology/smart_city_ontology.owl'
        inputfile = open(file, 'r').readlines()
        write_file = open(file,'w')
        flag = 0
        for line in inputfile:
            write_file.write(line)
            if 'ObjectPropertyAssertion' in line and class_owl in line and individual in line and not flag:
               new_line = 'DataPropertyAssertion(:'+property_assertion+' :'+individual+' \"'+property+'\")'
               write_file.write(new_line + "\n")
               flag = 1
        write_file.close()

    def class_assertion(self, class_owl, individual):
        file = './ontology/smart_city_ontology.owl'
        inputfile = open(file, 'r').readlines()
        write_file = open(file,'w')
        flag = 0
        for line in inputfile:
            write_file.write(line)
            # if '# Individual:' in line and not flag:
            if 'ClassAssertion(' in line and not flag:
               new_line = '\n# Individual: :'+individual+' (:'+individual+')\n'
               write_file.write(new_line + "\n")
               new_line = 'ClassAssertion(:'+class_owl+' :'+individual+')'
               write_file.write(new_line + "\n")
               flag = 1
        write_file.close()

    def named_individual(self, individual):
        file = './ontology/smart_city_ontology.owl'
        inputfile = open(file, 'r').readlines()
        write_file = open(file,'w')
        flag = 0
        for line in inputfile:
            write_file.write(line)
            if 'Declaration(NamedIndividual(' in line and not flag:
               # for item in list:
               new_line = 'Declaration(NamedIndividual(:'+individual+'))'
               write_file.write(new_line + "\n")
               flag = 1
        write_file.close()


    def write_poi_data(self):
        with open('foursquare_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                print(row)
