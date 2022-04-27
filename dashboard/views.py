from django.shortcuts import render
from django.http import HttpResponseRedirect
import pandas as pd
import boto3
import json
from .functions import *
#from .models import CompProfile

# Create your views here.
import json
s3 = boto3.resource('s3')
obj = s3.Object('history-1-register', 'initial_db.json')
data = obj.get()['Body'].read().decode('utf-8')
json_data = json.loads(data)
df = pd.DataFrame(json_data)

## Add number of occurence
df['Weight_Person'] = df.groupby('Name and Surname')['Name and Surname'].transform('size')
df['Weight_Company'] = df.groupby('Company')['Company'].transform('size')

## Keep relevant columns & remove duplicates
df = df[['Name and Surname','Company','Weight_Person','Weight_Company']]
df =df.drop_duplicates()

## Remove code
df['Name and Surname'] = df['Name and Surname'].astype(str)
df['Name and Surname'].mask((df['Name and Surname'].str.contains("CHE-")),(df['Name and Surname'].str[:-18]), inplace=True)
df['Name and Surname'].mask((df['Name and Surname'].str.contains("CH-")),(df['Name and Surname'].str[:-19]), inplace=True)


def index(request):
    top_connected = pd.DataFrame(df['Name and Surname'].value_counts())
    top_connected = top_connected[top_connected['Name and Surname'] >= 2]
    top_connected = top_connected[200:220]
    top_connected_board_member = top_connected.to_html()

    top_connected = pd.DataFrame(df['Company'].value_counts())
    top_connected = top_connected[top_connected['Company'] >= 2]
    top_connected = top_connected[200:220]
    top_connected_company = top_connected.to_html()

    context= {
        'df_board':top_connected_board_member,
        'df_company':top_connected_company

    }
    return render(request, 'dashboard/index.html', context=context)


def person_connection(request):
    if request.method == 'POST':
        name = request.POST["name"]
        y = name
        
        df_graph, board_members, companies = get_full_connectivity_board(df, y)
    print(df_graph)
    nodes_list, links_list = get_data_js(df_graph)
    nodes_list = json.dumps(nodes_list)
    links_list = json.dumps(links_list)


    context = {'nodes_list':nodes_list,
    'links_list':links_list}

    print(nodes_list)
    return render(request, 'dashboard/results_d3.html', context =context)


# def person_connection(request):
#     if request.method == 'POST':
#         name = request.POST["name"]
#         y = name
        
#         df_graph, board_members, companies = get_full_connectivity_board(df, y)

    
#     create_graph_person(df_graph)

#     return render(request, 'dashboard/graph_person.html')



def company_connection(request):
    if request.method == 'POST':
        name = request.POST["name"]
        y = name
        
        df_graph, board_members, companies = get_full_connectivity_company(df, y)

    
    create_graph_company(df_graph)

    return render(request, 'dashboard/graph_company.html')


    

