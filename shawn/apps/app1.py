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

#main concept of this is 2 different list no zip

input_blob = 'topwordsfortopics.csv'
df = pd.read_csv(input_blob)    

def Average(lst):
    return sum(lst) / len(lst)

aspect_number = 1

#find dataframe rows how many
#print(len(df.index))

#1.access dataframe--------------------------------
dataframerows = len(df)
aspect_num1_string = df.at[0, 'top_words']

#2.put string and slice to list---------------------
aspect_num1_list = (aspect_num1_string.split(':'))

#3.same thing aspect num 1 word_impt slicing to list
aspect_num1_wordimpt = df.at[aspect_number-1, 'word_impt']
aspect_num1_wordimptlist = aspect_num1_wordimpt.split(':')
#print(aspect_num1_wordimptlist)

#4.using list comprehension to perform conversion 
#have to float convert 
#if round to int lose too much info
#list comprehension just like for loop but better performance
aspect_num1_wordimptlist = [float(i) for i in aspect_num1_wordimptlist]

#5.make word bigger
aspect_num1_wordimptlist_scaled = [i*0.45 for i in aspect_num1_wordimptlist]

#6.find average
aspect_num1_wordimptlist_average = Average(aspect_num1_wordimptlist_scaled)

#7.
#iterate and check if > average
#make word bigger or smaller based on the relative value compared to average
#access word weightage for element 0
#aspect_num1_wordimptlist[0]

#have to access weight list in sync with word list iterate together
#word and weightage lists will run in conjunction
aspect_num1_wordimptlist_scaled = [i * 1.3 if i > aspect_num1_wordimptlist_average else i*0.3 for i in aspect_num1_wordimptlist_scaled]

#8.scale word size up
scaled_words_final = []

#aspect_num1_list is words
#aspect_num1_wordimptlist_scaled is weightage but scaled

for weightage in aspect_num1_wordimptlist_scaled:
    
    if weightage > aspect_num1_wordimptlist_average:
        scaled_words_final.append(1.4 * weightage*2) #this is actually just appending weightage to the scaled_wrods_final list
        #scale the words based on preset float * weightage
    elif weightage < aspect_num1_wordimptlist_average:
        scaled_words_final.append(0.8 * weightage* 6)

#print('shawn word')
#print(scaled_words_final) 

#dash scattter graph 
#split needs to be string
#print(aspect_num1_list[0][0])

#9.
#plotly color scheme you can change

colors = [px.colors.sequential.Viridis[random.randrange(1,10)] for i in range(30)]
weights = scaled_words_final

#10.
#this has to be here because 'trace' word will pop up for every mouseover on every word. 'Weightage' under
#mystring var is to replace it

#remove trace text
mystring = '<extra>Weightage</extra>'
aspect_num1_wordimptlist_str = [str(s) + mystring for s in aspect_num1_wordimptlist]

#11.
#this is here because initially 2 yaxis is requested trace0 and trace1 on right chart legacy code so i just used this way
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

#12.
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
#left chart
html.Div([
    dcc.Graph(
        id='scatter_chart',figure = {
                'data' : [
                    go.Scatter(
                       x = [4,8,8,7,8,5,4,5.5,9,10,8,6,4,5,5,3,2,2,2,2],
                      y = [3,2,3.5,5.5,7,9,7,8,9,10,11,11,11,10,10.5,10,8,6,5,4],
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
#right chart
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
#dash built in callback for no refresh and instant response 
#output to scatter chart
#but below callback update_graph_1 is standard format to override the data in the current chart 

@app.callback(
    Output("scatter_chart", "figure"),
    [Input("variable_choice", "value")])

def update_graph_1(variable_choice):
    #fixed x error on dropdown
    if variable_choice == None:
        variable_choice = 1

    #df create new copy as good practice
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

    #print(variable_choice)

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




