from pyvis.network import Network
import pandas as pd

def get_full_connectivity_company(df, y):
    board_members = []
    board_members_export = []
    companies = []
    
    condition = False
    n = 0
    l = 0
    j = 0
    
    ## CASE 2= NOT FOUND ON BOARD BUT IN REGISTER
    ## 1. Find board members
    if (df['Company'].str.contains(y).any()):
        board_members = (df[df['Company']==str(y)]['Name and Surname']).tolist()
    
    elif (df['Name and Surname'].str.contains(y).any()):
        board_members = (df[df['Name and Surname']==str(y)]['Name and Surname']).tolist()

    else:
        condition = True
        board_members = ['None']
        companies = ['None']
        

    while (j < 900):
        more_companies = []
        more_members = []
        
        ## 2. Search if board members belong to more companies
        for i in board_members:
            find_as_company = (df[df['Name and Surname']==str(i)])['Company'].tolist()
            j += len(more_companies)
            
            more_companies = more_companies + find_as_company
            # remove duplicates
            more_companies = list(dict.fromkeys(more_companies))
        print('more_companies')
       
        
        for i in more_companies:
            find_as_company = (df[df['Company']==str(i)])['Name and Surname'].tolist()
            j += len(find_as_company)
            more_members = more_members + find_as_company
            # remove duplicates
            more_members = list(dict.fromkeys(more_members))
        print('more_members')

        
        companies = more_companies
        board_members = more_members + more_companies
        
        l += 1
        print('Going one level deeper for a total of', l)

    board_members = pd.DataFrame(board_members)
    companies = pd.DataFrame(companies)
    board_members.columns = ['member_name']
    companies.columns = ['company_name']

    df_graph = pd.merge(df, board_members, how='right',left_on='Name and Surname', right_on='member_name')
    
    ## This should be replaced later on
    df_graph = df_graph[:200]
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



def get_data_js(df_graph):
    df_graph = df_graph[['Name and Surname', 'Company']]
    df_graph.columns = ['source','target']
    grouped_src_dst = df_graph.groupby(["source","target"]).size().reset_index()
    
    unique_nodes = pd.Index(grouped_src_dst['source']
                      .append(grouped_src_dst['target'])
                      .reset_index(drop=True).unique())

    nodes_list = []
    for ip in unique_nodes:
        nodes_list.append({"name":ip})
    nodes_list

    df1 = pd.DataFrame(nodes_list)


    yala = []
    i = 0
    while i < len(grouped_src_dst):
        yala.append({"group":1, "name":grouped_src_dst.iloc[i]['source']})
        yala.append({"group":2, "name":grouped_src_dst.iloc[i]['target']})
        i +=1

    df2 = pd.DataFrame(yala)
    result = pd.merge(df1, df2, on=["name", "name"])
    check = df1.merge(df2, how='left', on='name').drop_duplicates()
    
    nodes_list = []

    i = 0 
    while i < len(check):
        nodes_list.append({"group":str(check.iloc[i]['group']), "name":str(check.iloc[i]['name'])})
        #nodes_list.append({"name":str(check.iloc[i]['name'])})
        i += 1
        
    grouped_src_dst.rename(columns={0:'count'}, inplace=True)
    temp_links_list = list(grouped_src_dst.apply(lambda row: {"source": row['source'], "target": row['target'], "value": row['count']}, axis=1))

    links_list = []
    for link in temp_links_list:
        record = {"source":unique_nodes.get_loc(link['source']),
         "target": unique_nodes.get_loc(link['target'])}
        links_list.append(record)
        
    return nodes_list, links_list