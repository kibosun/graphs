import time

import networkx
import networkx as nx
from pythonds.basic import Queue
import random


freq_for_each_year = {} #  freq for each year we read in the file
# how many times we have encoutered the year--> +1
def create_graphs(file, position):
    G = nx.Graph()
    dict_id_authors = {}  # {'id': ['a1', 'a2',...,'ai']}
    for line in file:
        line= line.replace("\n", "")
        fields_list = line.split(';')
        publication = fields_list[0]
        authors_list = fields_list[position].split('|')
        dict_id_authors[publication] = authors_list
        year = fields_list[-1]
        freq = freq_for_each_year.get(year)
        # Case we don't have that year:
        if freq is None:
            freq_for_each_year.update({year: 1})
        else:
            freq_for_each_year.update({year: freq + 1})
        id = fields_list[0]
        G.add_node(id, type="publication", color = 'white')
        for i in authors_list:
            if G.nodes.get(i) is None:
                G.add_node(i, color = 'white')
            G.add_edge(i, id)
    return (G, dict_id_authors)  # Tupla


def question_1():
    minimum = 1949 # we have printed for each file the lowest key of the freq_for_each_year , and we have taken the lowest year of the seven
    current_cumul= 0
    for x in [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023]:
        for k in freq_for_each_year.keys():
            if k <= str(x):
                current_cumul += freq_for_each_year[k] # number of publications from 1949 to x
        diff = x - minimum + 1  # number of years from 1949 to x
        result = current_cumul / diff
        print("The mean is "+ str(result))


def my_bfs(my_graph: networkx.Graph):
    all_white_nodes_dict = dict.fromkeys(my_graph.nodes, 1)  # Create a new dictionary s.th nodes = keys and each value set to 1. it is a for loop  {id : 1, a1:1 etc}
    tot_number_nodes = my_graph.number_of_nodes()
    list_of_tuples = list(all_white_nodes_dict.items()) # list of tuples s.th. [(id, 1), (a1,1) etc]. color = 'white' = 1
    max_component_size = 0 # I initialize the size of the CC
    max_component = [] # it is the list of the nodes that costitute the CC
    start = 0 # index list_of_tuples
    while max_component_size < tot_number_nodes: # num of BLACK NODES (0) of my list < num of WHITE NODES (1) of the graph
        node, color = list_of_tuples[start]
        start += 1
        if color != 0: # i.e. the node is white
            component = [] # list of black for the current BFS
            component_size = 0
            vertQueue = Queue()
            vertQueue.enqueue(node)
            all_white_nodes_dict[node] = 0  # start node becomes now black (it is in the queue)
            while vertQueue.size() > 0:
                visited = vertQueue.dequeue()
                component_size += 1
                component.append(visited)
                for neighbor in my_graph.neighbors(visited):
                    if all_white_nodes_dict[neighbor] == 1: # if white--> = black
                            all_white_nodes_dict[neighbor] = 0
                            vertQueue.enqueue(neighbor)
            if component_size > max_component_size:
                max_component_size = component_size
                max_component = component
            tot_number_nodes -= component_size # delete the visited nodes (black) from those one that are white
            print("the total number of node is " + str(tot_number_nodes) + " and the size of current CC is " + str(max_component_size))
    return  max_component # CC


def create_sub_graph(max_component, dict_id_authors): # O(m * n)
    sub_graph = nx.Graph()  # this graph is empty
    # filling the sub-graph
    for id in max_component: # O (n)
        if id in dict_id_authors:
            sub_graph.add_node(id, type = 'publication') # id = key of dict_id_authors i.e. publications
            for author in dict_id_authors[id]: # O(m)
                sub_graph.add_edge(author, id) # each value is costituited by the lists of authors {'122': ['chiara', 'martina'] etc}
    print("the dimension of the sub_graph is "+ str(sub_graph.number_of_nodes())+ ' i.e., the len of '+ str(len(max_component)))
    return sub_graph

"""
def closeness_centrality_question2(sub_graph):
    closeness_centrality = nx.closeness_centrality(sub_graph) # for each vertex of the sub_graph, returns a dictionary {node: closeness centrality scores}
    sorted_nodes = sorted(closeness_centrality, key= closeness_centrality.get,reverse=True)
    # key= closeness_centrality.get --> it reverses my dict
    res= []
    for i in sorted_nodes:
        if not i.isdigit():
            centrality = closeness_centrality[i]
            res.append(str(i)+ ": " + str(centrality))
    print(res[:10])
"""

def bfs_question2(G, start):
        start.setDistance(0)
        start.setPred(None)
        vertQueue = Queue()
        vertQueue.enqueue(start)
        while (vertQueue.size() > 0):
            currentVert = vertQueue.dequeue()
            for nbr in currentVert.getConnections():
                if (nbr.getColor() == 'white'):
                    nbr.setColor('gray')
                    nbr.setDistance(currentVert.getDistance() + 1)
                    nbr.setPred(currentVert)
                    vertQueue.enqueue(nbr)
            currentVert.setColor('black')
        return start.getDistance()


def closeness_centrality_question2(sub_graph: networkx.Graph, k, max_component):
    count = [0] * len(max_component)
    for element in range(2):
        r = random.randint(0, len(max_component))
        random_node = max_component[r]  # U = [random_node1,..., random_nodek]
        bfs_question2(sub_graph, random_node)
        distance = bfs_question2(sub_graph, random_node)
        for v in sub_graph.nodes():
            count[v] += distance
        for v in sub_graph.nodes():
            count[v] = count[v] / k
    array = sorted(count)
    closeness = array[:10]
    print(closeness)



def degree_of_author(graph):
    author_paper_counts = {}
    # Calculate the degree for each author: how many publications he/she wrote
    for author, data in graph.nodes(data=True):
        if 'type' not in data:
            author_paper_counts[author] = graph.degree(author) # {author: degree}
    return author_paper_counts


def question_3(author_paper_counts, dict_id_authors):
    d1_new = {}
    for key, value in dict_id_authors.items():
        corr = []
        for name in value:
            if name in author_paper_counts and len(name) > 0:
                    corr.append(author_paper_counts[name]) # taking the degree of name (i.e. the author)
        d1_new[key] = corr # {'121081': [1, 1, 1], '140029': [1, 1], ecc} i.e. {id: list of degrees}
    maximum = 0
    for i in d1_new.items(): # tuple, ex. (id, [1,1,1])
        sum_values = sum(i[1]) # sum the list, i.e. the second element of the tuple
        if sum_values > maximum:
            maximum = sum_values
            id_max = i[0]
    print("The publication with the largest number of popular authors has the following ID: " + str(id_max))


file_book = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_book.txt', 'r', encoding='utf8')
file_article = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_article.txt', 'r', encoding='utf8')
file_incollection = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_incollection.txt', 'r', encoding='utf8')
file_inproceedings = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_inproceedings.txt', 'r', encoding='utf8')
file_mastersthesis = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_mastersthesis.txt', 'r', encoding='utf8')
file_phdthesis = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_phdthesis.txt', 'r', encoding='utf8')
file_proceedings = open('C:/Users/Utente/Desktop/IPAD PROJECT FILES/out-dblp_proceedings.txt', 'r', encoding='utf8')




def main():
    file_list = [file_article, file_proceedings, file_mastersthesis, file_incollection, file_inproceedings, file_phdthesis, file_book]
    # if i split with respect to ; the field author changes position
    positions = [1, 6, 1, 1, 1, 1, 1]
    positions= [positions[3]]
    file_list = [file_list[3]]
    for file, position in zip(file_list, positions):
        my_graph, my_dictionary = create_graphs(file, position)
        print("The number of total nodes is " + str(my_graph.number_of_nodes()) + " and the number of edges is " + str(my_graph.size()))
        file_article.close()
        file_proceedings.close()
        file_mastersthesis.close()
        file_incollection.close()
        file_proceedings.close()
        file_phdthesis.close()
        file_book.close()
        #question_1()
        #max_component = my_bfs(my_graph)
        #sub_graph = create_sub_graph(max_component, my_dictionary)
        #closeness_centrality_question2(sub_graph, 2, max_component)
        degree_of_each_author = degree_of_author(my_graph)
        question_3(degree_of_each_author, my_dictionary)
        start = time.time()
        print("TIME: " + str(time.time() - start))




if __name__ == '__main__':
    main()
