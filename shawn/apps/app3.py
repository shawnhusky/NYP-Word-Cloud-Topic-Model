from azure.storage.blob import BlockBlobService
import pandas as pd
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import math

from dash.dependencies import Input, Output
from app import app

"""
STORAGEACCOUNTNAME4= "bla"
STORAGEACCOUNTKEY4= "+/==bla"
LOCALFILENAME4= "bla"
CONTAINERNAME4= "bla"
BLOBNAME4= "topNSentimentSent.csv"


#stream

block_blob_service4 = BlockBlobService(account_name=STORAGEACCOUNTNAME4, account_key=STORAGEACCOUNTKEY4)

from io import BytesIO
import pandas as pd4
with BytesIO() as input_blob4:
    block_blob_service4.get_blob_to_stream(CONTAINERNAME4, BLOBNAME4, input_blob4)
    input_blob4.seek(0)
    df4 = pd4.read_csv(input_blob4)   

"""
input_blob4= "topNSentimentSent.csv"
df4 = pd.read_csv(input_blob4)  

#project and reflections var
#neg_sentences,neg_sent_project,pos_sentences,pos_sent_project

neg_sentences_app4 = df4['neg_sentences']
pos_sentences_app4 = df4['pos_sentences']
neg_sent_project_app4 = df4['neg_sent_project']
pos_sent_project_app4 = df4['pos_sent_project']

"""
print("app4")
print(neg_sentences_app4)
"""

"""
#put in list
neg_sentence_app4 = neg_sentences_app4.split(',')
pos_sentence_app4 = pos_sentences_app4.split(',')
"""


#append sentences list to project name list easier to categorise


#one dropdown control both
no_of_projectsApp4 = len(pos_sent_project_app4)

layout = html.Div([
    html.H1(children='Sentences by Project'),

    html.Div([
dcc.Dropdown(
    id="variable_choice_app4",
    options=[{"label": i, "value": i} for i in neg_sent_project_app4] #no of sentence/6
    )
    ], style={"width": "50%", "display" : "block"}),

    html.Div(id='sentenceapp4')

])


@app.callback(
    Output('sentenceapp4', 'children'),
    Input("variable_choice_app4", "value"))

def update_graph_app4(variable_choice_app4):

    #filter words here when u need to if not use df
    
    #print("shawn")
    #print(variable_choice_app4)

    #find out element in which user press

    #search for the project
    
    #print(df4['neg_sent_project'].where(df4['neg_sent_project'] == variable_choice_app4))

    #get neg
    #where is actually neg_sent_project
    negresult = df4['neg_sentences'].where(df4['neg_sent_project'] == variable_choice_app4)

    negresultList = negresult.values.tolist()

    #get pos
    #where is actually pos_sent_project
    
    posresult = df4['pos_sentences'].where(df4['pos_sent_project'] == variable_choice_app4)

    posresultList = posresult.values.tolist()

    #filter the nans
    
    negcleanedList = [x for x in negresultList if str(x) != 'nan']
    poscleanedList = [x for x in posresultList if str(x) != 'nan']
    #print("result")


    #put in list but must convert to string first
    negcleanedList2 = str(negcleanedList).split(',')
    poscleanedList2 = str(poscleanedList).split(',')

    print(negcleanedList2[0])

    #filter here

    

    
    #append before return since cant iterate any where!
    #old list has items already put in new list then throw to return

    FinalTableReturn = [] #new list

    def generate_html_table_neg(max_rows=99999):

        for i in range(min(len(negcleanedList2), max_rows)):
            FinalTableReturn.append(html.Tr([
                html.Td(html.A([
                #append text to show
                negcleanedList2[i]
                ], id=str(i)))
            ]))

    #pos list
    FinalTableReturn2 = [] #new list

    def generate_html_table_pos(max_rows=5):

        for i in range(min(len(poscleanedList2), max_rows)):
            FinalTableReturn2.append(html.Tr([
                html.Td(html.A([
                #append text to show
                poscleanedList2[i]
                ], id=str(i)))
            ]))

    #update return

    generate_html_table_neg(9999999)
    generate_html_table_pos(9999999)

    return html.Div([
    html.Div(html.Table(
        [
            html.Tr(html.Th("Neg")),
            html.Tbody(FinalTableReturn),
        ]
    ), id='fixedheight',style={"width": "50%", "display" : "inline-flex"}),

    html.Div(html.Table(
        [
            html.Tr(html.Th("Pos")),
            html.Tbody(FinalTableReturn2),
        ]
    ), id='fixedheight',style={"width": "50%", "display" : "inline-flex"})


])


