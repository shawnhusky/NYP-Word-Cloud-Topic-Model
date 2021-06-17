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

from dash.dependencies import Input, Output

from app import app

"""
#variables to declare to access azure for stream
STORAGEACCOUNTNAME= "bla"
STORAGEACCOUNTKEY= "bla"
LOCALFILENAME= "bla"
CONTAINERNAME= "bla"
BLOBNAME= "bla"

#actual code for streaming

block_blob_service = BlockBlobService(account_name=STORAGEACCOUNTNAME, account_key=STORAGEACCOUNTKEY)

input_blob = 'topwordsfortopics.csv'
from io import BytesIO
import pandas as pd
with BytesIO() as input_blob:
    block_blob_service.get_blob_to_stream(CONTAINERNAME, BLOBNAME, input_blob)
    input_blob.seek(0)
    df = pd.read_csv(input_blob)    

"""

input_blob = 'topwordsfortopics.csv'
df = pd.read_csv(input_blob)    

#find average no. of elements in list and return

def Average(lst):
    return sum(lst) / len(lst)

aspect_number = 1

#find dataframe rows how many
#print(len(df.index))
dataframerows = len(df)

#empty list init
#aspect_num1_list = [[] for _ in range(dataframerows)]

#string slicing to list

#why need to slice? Because all the words are in one particular cell.Look at csv file.
#slice to put in list so you know exactly how many words there are. 

#aspect num 1 topwords
#aspect num 1 list starts with 0 so -1

aspect_num1_string = df.at[aspect_number-1, 'top_words']

#split the string from df and put inside first list of nested list
aspect_num1_list = (aspect_num1_string.split(':'))



#aspect_num1_string.split(':')
#print(aspect_num1_list)

#aspect num 1 word_impt slicing to list
aspect_num1_wordimpt = df.at[aspect_number-1, 'word_impt']
aspect_num1_wordimptlist = aspect_num1_wordimpt.split(':')
print(aspect_num1_wordimptlist)




#using list comprehension to perform conversion 
#have to float convert 
#if round to int lose too much info
#list comprehension just like for loop but better performance
aspect_num1_wordimptlist = [float(i) for i in aspect_num1_wordimptlist]

#make word bigger
aspect_num1_wordimptlist_scaled = [i*0.45 for i in aspect_num1_wordimptlist]

#make words distinct

#find average
aspect_num1_wordimptlist_average = Average(aspect_num1_wordimptlist_scaled)

#iterate and check if > average
#make word bigger or smaller based on the relative value compared to average

#access word weightage for element 0
#aspect_num1_wordimptlist[0]

#have to access weight list in sync with word list iterate together

aspect_num1_wordimptlist_scaled = [i * 1.3 if i > aspect_num1_wordimptlist_average else i*0.3 for i in aspect_num1_wordimptlist_scaled]


# new empty list
#zip list or tuple together then iterate it as such
#e.g element1 (word,0.4) This will let you manipulate and check weightage of that particular word since its considered as one element now when iterated.
scaled_words_final = []

for word, weightage in zip(aspect_num1_list, aspect_num1_wordimptlist_scaled):
    #print(word, weightage)

    if weightage > aspect_num1_wordimptlist_average:
        scaled_words_final.append(1.4 * weightage*2)
        #scale the words based on preset float * weightage
    elif weightage < aspect_num1_wordimptlist_average:
        scaled_words_final.append(0.8 * weightage* 6)

#print(scaled_words_final) 

#dash scattter graph 
#split needs to be string
#print(aspect_num1_list[0][0])
#plotly color scheme you can change

colors = [px.colors.sequential.Viridis[random.randrange(1,10)] for i in range(30)]
weights = scaled_words_final

#this is the shuffle section. This is is to be use in conjunction with the wordcloud collision detection
#recursive function So the word cloud words will not be overlapped. if you realise when app is loading for a second, 
#word cloud words auto realign. This is because it uses the updated graph from callback which you will see later.

np.random.seed(30)
#x_rand = np.random.randint(0,30,60)
#y_rand = random.choices(range(30), k=31)

#print(len(x_rand))

#no duplicate on y axis 
import random
tab = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
random.shuffle(tab)
y_rand = tab

#no duplicate on x axis 
import random
tab2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
random.shuffle(tab2)
x_rand = tab2


#this has to be here because 'trace' word will pop up for every mouseover on every word. 'Weightage' under
#mystring var is to replace it

#remove trace text
mystring = '<extra>Weightage</extra>'
aspect_num1_wordimptlist_str = [str(s) + mystring for s in aspect_num1_wordimptlist]

#this is here because initially 2 yaxis is requested
#for chart2
trace0 = go.Bar(
name = 'Weight',
x = aspect_num1_list,
y = aspect_num1_wordimptlist,
width=0.5,
marker={'color': '#80e5ff'}

)

datas = [trace0]


variable_indicators = df["aspect_num"]

#layout.purely for display.
#html.H1 is dash built in way of display h1 html.
#html div styling make sure add it after , not )

layout = html.Div(children=[
    html.H1(children='Word Cloud'),
    html.Div([

    html.Div([
dcc.Dropdown(
    id="variable_choice",
    options=[{"label": i, "value": i} for i in variable_indicators],value=1
    )
    ], style={"width": "50%", "display" : "inline-block"}),



    ]),

#put graph in div encapsulation.Then can style.

html.Div([
    dcc.Graph(
        id='scatter_chart',figure = {
                'data' : [
                    go.Scatter(
                        x = tab,
                        y = tab2,
                        mode = 'text',text = aspect_num1_list, textfont={'size': weights,'color' : colors, 'family' : 'Georgia'}, marker ={'opacity':0.01},
                        hovertemplate = aspect_num1_wordimptlist_str
                        )],
                        'layout' : go.Layout(
                        title = 'Word Cloud',
                        xaxis = {'showgrid':False, 'showticklabels':False, 'zeroline': False},
                        yaxis = {'showgrid':False, 'showticklabels':False, 'zeroline': False},
                        hovermode = 'closest',  paper_bgcolor = "rgb(0,0,0,0)",
                    plot_bgcolor =  "rgb(0,0,0,0)", #transparent bg
                    font_color = "#CECECE"
                        )
            }, style={'display': 'inline-block', 'width' : '50%'}
    ),

    dcc.Graph(
        id='weightage_chart',figure = {
                'data' : datas,
                        'layout' : go.Layout(
                        title = 'Word Frequency and Weightage',
                        showlegend = False,
                        xaxis =  {'title': '','showline': True},
                        yaxis = {'title': 'Word Count','side': 'left','showline': True}, paper_bgcolor = "rgb(0,0,0,0)",
                    plot_bgcolor =  "rgb(0,0,0,0)", #transparent bg
                    font_color = "#CECECE"
                        )
            }, style={'display': 'inline-block', 'width' : '50%'}
    )

])
])

#wordcloud update
#

@app.callback(
    Output("scatter_chart", "figure"),
    [Input("variable_choice", "value")])

def update_graph_1(variable_choice):
    #fixed x error on dropdown
    if variable_choice == None:
        variable_choice = 1

    #df create new copy
    dff = df[df["aspect_num"]==variable_choice]

    #update graph vars when click
    #variable_choice = 1 for testing since no default var
    aspect_number = variable_choice
    #print(aspect_number)

    aspect_num1_string = df.at[aspect_number-1, 'top_words']

    #split the string from df and put inside first list of nested list
    aspect_num1_list = (aspect_num1_string.split(':'))

    aspect_num1_wordimpt = df.at[aspect_number-1, 'word_impt']
    aspect_num1_wordimptlist = aspect_num1_wordimpt.split(':')

    #remove trace text
    mystring = '<extra>Weightage</extra>'
    aspect_num1_wordimptlist_str = [str(s) + mystring for s in aspect_num1_wordimptlist]

    #aspect_num = variable_choice

    return {
        'data' : [
                go.Scatter(
                    x = [4,8,8,7,8,5,4,5.5,9,10,8,6,4,5,5,3,2,2,2,2],
                    y = [3,2,3.5,5.5,7,9,7,8,9,10,11,11,11,10,10.5,10,8,6,5,4],
                    mode = 'text',text = aspect_num1_list, textfont={'size': weights,'color' : colors}, marker ={'opacity':0.01},
                    hovertemplate = aspect_num1_wordimptlist_str
                    )],
                    'layout' : go.Layout(
                    title = "Topic " + str(variable_choice),
                    xaxis = {'showgrid':False, 'showticklabels':False, 'zeroline': False, 'rangemode' : 'tozero'},
                    yaxis = {'showgrid':False, 'showticklabels':False, 'zeroline': False, 'rangemode' : 'tozero'},
                    hovermode = 'closest',paper_bgcolor = "rgb(0,0,0,0)",
                    plot_bgcolor =  "rgb(0,0,0,0)", #transparent bg
                    font_color = "#CECECE"
                    )
    }

#word freq chart update

@app.callback(
    Output("weightage_chart", "figure"),
    [Input("variable_choice", "value")])

def update_graph_2(variable_choice):
    #fixed x error on dropdown
    if variable_choice == None:
        variable_choice = 1

    print(variable_choice)

    #df create new copy
    dff = df[df["aspect_num"]==variable_choice]

    #update graph vars when click

    #variable_choice = 1 for testing since no default var
    aspect_number = variable_choice
    #rint(aspect_number)

    aspect_num1_string = df.at[aspect_number-1, 'top_words']

    #split the string from df and put inside first list of nested list
    aspect_num1_list = (aspect_num1_string.split(':'))

    aspect_num1_wordimpt = df.at[aspect_number-1, 'word_impt']
    aspect_num1_wordimptlist = aspect_num1_wordimpt.split(':')



    #for chart2
    trace0 = go.Bar(
    name = 'Weight',
    x = aspect_num1_list,
    y = aspect_num1_wordimptlist,
    width=0.5,
    marker={'color': '#80e5ff'}

    )

    datas = [trace0]

    #might remove if bug
    #remove trace text
    mystring = '<extra>Weightage</extra>'
    aspect_num1_wordimptlist_str = [str(s) + mystring for s in aspect_num1_wordimptlist]


    #aspect_num = variable_choice

    return {
                'data' : datas,
                        'layout' : go.Layout(
                        title = 'Word Weightage',
                        showlegend = False,
                        xaxis =  {'title': '','showline': False, 'showgrid':False, 'zeroline':False},
                        yaxis = {'title': 'Word Weightage','side': 'left','showline': False,'showgrid': False,'zeroline' : False}, plot_bgcolor =  "rgb(0,0,0,0)", #transparent bg
                        paper_bgcolor = "rgb(0,0,0,0)",
                        font_color = "#CECECE"
                        )

        }




