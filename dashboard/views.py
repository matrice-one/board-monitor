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

# Add number of occurence
df['Weight_Person'] = df.groupby('Name and Surname')['Name and Surname'].transform('size')
df['Weight_Company'] = df.groupby('Company')['Company'].transform('size')

## Keep relevant columns & remove duplicates
df = df[['Name and Surname','Company','Weight_Person','Weight_Company']]
df =df.drop_duplicates()

# df = pd.read_excel('/Users/neigelinerivollat/Desktop/Pictet project/where_are_you.xlsx')
# df2 = df.set_axis(['Index', 'Name', 'Status', 'Signature mode', 'Company'], axis=1, inplace=False)
# try:
#     df2 = df.set_axis(['Index','Name', 'Status', 'Signature mode', 'Company'], axis=1, inplace=False)
# except:
#     df2 = df.set_axis(['Index','Name', 'Status', 'Signature mode', 'Company'], axis=1, inplace=False)

# df3 = df2["Name"].str.split(',', expand=True)

# try:
#     df3 = df3.set_axis(['Name and Surname', 'Origin', 'To', 'For 1', 'For 2', 'For 3' , 'For 4', 'For 5', 'For 6'], axis=1, inplace=False)
# except:
#     df3 = df3.set_axis(['Name and Surname', 'Origin', 'To', 'For 1', 'For 2' ], axis=1, inplace=False)
# result = pd.concat([df3, df2], axis=1)
# result_epurated = result[['Name and Surname', 'Origin', 'To','Status', 'Signature mode','Company']]

# df = result_epurated.drop_duplicates()

## Remove code
df['Name and Surname'] = df['Name and Surname'].astype(str)
df['Name and Surname'].mask((df['Name and Surname'].str.contains("CHE-")),(df['Name and Surname'].str[:-18]), inplace=True)
df['Name and Surname'].mask((df['Name and Surname'].str.contains("CH-")),(df['Name and Surname'].str[:-19]), inplace=True)

df = df[df['Name and Surname'] != '* du conseil']
df = df[df['Name and Surname'] != '* du conseil de fondation']
df = df[df['Name and Surname'] != '* du comité']
df = df[df['Name and Surname'] != '*du comité']
df = df[df['Name and Surname'] != '* du comité']
df = df[df['Name and Surname'] != '*du conseil de fondation']
df = df[df['Company'].str.contains('\*') == False]
df = df[df['Name and Surname'].str.contains('\*') == False]


def index(request):
    top_connected = pd.DataFrame(df['Name and Surname'].value_counts())
    top_connected = top_connected[top_connected['Name and Surname'] >= 2]
    top_connected = top_connected[0:20]
    top_connected_board_member = top_connected.to_html()

    top_connected = pd.DataFrame(df['Company'].value_counts())
    top_connected = top_connected[top_connected['Company'] >= 2]
    top_connected = top_connected[0:20]
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
        
        df_graph, board_members, companies = get_full_connectivity_company(df, y)
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


    

