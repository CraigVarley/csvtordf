# from https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
# converts csv to a pandas dataframe then to rdf, serialized in turtle

import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import urllib.parse

csv = "/Users/craigvarley/PycharmProjects/csvtordf/employees.csv"
df = pd.read_csv(csv) # csv to dataframe

# add new cols to combine or split strings for the URIs and strings
df['Full_Name'] = df['First_Name'] + df['Last_Name']  # print(df) # create a new column from 2 separate name values
df['Full_Name_String'] = df['First_Name'] + ' ' + df['Last_Name'] # creates a string of these for the label
df[['Domain1', 'Domain2']] = df['Domains'].str.split(' ', n=1, expand=True)

g = Graph() # create the graph object

# define my namespaces
ppl = Namespace("http://craigvarley.net/ontology/people/")
dom = Namespace("http://craigvarley.net/ontology/domains/")
id = Namespace("http://craigvarley.net/ontology/ids/")

for index, row in df.iterrows(): # iterate across the csv rows
    g.add((URIRef(ppl + row['Full_Name']), RDF.type, FOAF.Person)) # name is a type of person
    g.add((URIRef(ppl + row['Full_Name']), FOAF.name, Literal(row['Full_Name_String'], datatype=XSD.string))) # name has the string label
    g.add((URIRef(ppl + row['Full_Name']), URIRef(dom), Literal(row['Domain1'], datatype=XSD.string))) # name has these domain strings
    g.add((URIRef(ppl + row['Full_Name']), URIRef(dom), Literal(row['Domain2'], datatype=XSD.string))) # name has these domain strings

# g.add((URIRef(ppl+row['Name']), URIRef(schema+'address'), Literal(row['Address'], datatype=XSD.string) ))
# g.add((URIRef(loc+urllib.parse.quote(row['Address'])), URIRef(schema+'name'), Literal(row['Address'], datatype=XSD.string) ))

print(g.serialize(format='turtle').encode('UTF-8'))
