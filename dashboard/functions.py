from pyvis.network import Network
import pandas as pd

def get_full_connectivity_company(df, y):
    
    ## CASE 2= NOT FOUND ON BOARD BUT IN REGISTER
    ## 1. Find board members
    more_members = (df[df['Company']==str(y)]['Name and Surname']).tolist()
    
    
    board_members = []
    companies = []
    condition = False
    
    while (condition == False):
        
        more_companies = []
        
        ## 2. Search if board members belong to more companies
        for i in more_members:
            find_as_company = (df[df['Name and Surname']==str(i)])['Company'].tolist()
            more_companies = more_companies + find_as_company
            # remove duplicates
            more_companies = list(dict.fromkeys(more_companies))
       
        more_members = []
        
        for i in more_companies:
            find_as_company = (df[df['Company']==str(i)])['Name and Surname'].tolist()
            more_members = more_members + find_as_company
            # remove duplicates
            more_members = list(dict.fromkeys(more_members))
            
        
        condition1 = (more_companies == companies) 
        condition2 = (more_members == board_members)
        condition = condition1 and condition2
        
        companies = more_companies
        board_members = more_members

    board_members = pd.DataFrame(board_members)
    companies = pd.DataFrame(companies)
    board_members.columns = ['member_name']
    companies.columns = ['company_name']

    df_graph = pd.merge(df, companies, how='inner',left_on='Company', right_on='company_name')

    return df_graph, board_members, companies


def get_full_connectivity_board(df, y):
    more_companies = (df[df['Name and Surname']==str(y)]['Company']).tolist()
    
    board_members = []
    companies = []
    condition = False
    
    while (condition == False):
        more_members = []
        
        for i in more_companies:
            find_as_company = (df[df['Company']==str(i)])['Name and Surname'].tolist()
            more_members = more_members + find_as_company
            # remove duplicates
            more_members = list(dict.fromkeys(more_members))
            
        more_companies = []
        
        for i in more_members:
            find_as_company = (df[df['Name and Surname']==str(i)])['Company'].tolist()
            more_companies = more_companies + find_as_company
            # remove duplicates
            more_companies = list(dict.fromkeys(more_companies))
        
        condition1 = (more_companies == companies) 
        condition2 = (more_members == board_members)
        condition = condition1 and condition2
        
        companies = more_companies
        board_members = more_members

    board_members = pd.DataFrame(board_members)
    companies = pd.DataFrame(companies)
    board_members.columns = ['member_name']
    companies.columns = ['company_name']

    df_graph = pd.merge(df, companies, how='inner',left_on='Company', right_on='company_name')

    return df_graph, board_members, companies


def create_graph_person(df_graph):
    net = Network()

    i = 0
    while i < len(df_graph):
        net.add_node(str(df_graph.iloc[i]['Name and Surname']), label=str(df_graph.iloc[i]['Name and Surname']))
        net.add_node(str(df_graph.iloc[i]['Company']), label=str(df_graph.iloc[i]['Company']))

        i += 1

    i = 0
    while i < len(df_graph):
        net.add_edge(str(df_graph.iloc[i]['Name and Surname']), str(df_graph.iloc[i]['Company']))
        i +=1

    net.show_buttons(filter_=True)
    net.show('dashboard/templates/dashboard/graph_person.html')



def create_graph_company(df_graph):
    net = Network()

    i = 0
    while i < len(df_graph):
        net.add_node(str(df_graph.iloc[i]['Name and Surname']), label=str(df_graph.iloc[i]['Name and Surname']))
        net.add_node(str(df_graph.iloc[i]['Company']), label=str(df_graph.iloc[i]['Company']))

        i += 1

    i = 0
    while i < len(df_graph):
        net.add_edge(str(df_graph.iloc[i]['Name and Surname']), str(df_graph.iloc[i]['Company']))
        i +=1

    net.show_buttons(filter_=True)
    net.show('dashboard/templates/dashboard/graph_company.html')