#used libraries
from ast import parse
import argparse

import os
from datetime import datetime
from math import sqrt

import linecache

import matplotlib.pyplot as plt
import networkx as nx

#creating structure for mounting the graph
G = nx.Graph()


def check_file(file_t, file_opening_template):
    try:
        f = open(file_t, file_opening_template)

    except:
        print(f"O arquivo {file_t} não existe ou não pode ser aberto.")

        exit(1)

    return f


def check_conversion(element, type_conversion):
    new_element = 0
    try:
        new_element = type_conversion(element)

    except:
        print("Algo deu errado na conversão do valor.")

        exit(1)

    return new_element


def truncated(num):
    num_complet = ""

    num_str = str(num)
    num_str = num_str.split('.')

    num_complet = num_str[0] + '.' + num_str[1][0:2]

    num = float(num_complet)

    return num


def creator_dir(path, name_dir):
    global path_folder

    if (path == "" and name_dir != "/process_result/"):
        print("caminho de criação não especificado.")

        exit()

    if (name_dir == "/process_result/"):
        original_path = os.path.abspath(__file__)

        new_path = original_path.split('/')
        new_path = '/'.join(new_path[0:-1])

        full_path = new_path + name_dir

        if not os.path.isdir(full_path):
            os.mkdir(full_path)

    else:
        full_path = path + name_dir

        os.mkdir(full_path)

    path_folder = full_path

    return path_folder


def current_day():
    day_plus_hours = datetime.now()
    day_in_str = day_plus_hours.strftime("%d-%m-%Y_%H:%M:%S")
    
    return day_in_str


def name_file(dir, str_input):
    global global_file_name
    if(dir == ""):
        routes_file_name = path_folder

    routes_file_name = dir

    day_in_str = current_day()

    global_file_name = str_input + day_in_str
    routes_file_name += global_file_name

    return routes_file_name


def file_node_creator(file_name):
    global global_point_file_name;
    global global_main_directory_path
    global global_source

    global_source = creator_dir("", "/process_result/")
    global_main_directory_path = creator_dir(global_source, (current_day() + "/"))
    
    global_point_file_name = name_file(global_main_directory_path, "points_")
    
    file_w = check_file((global_point_file_name + ".txt"), "w")
    file_r = check_file(file_name, "r")

    for i in file_r:
        string_without_tab = i.strip()

        if (string_without_tab[0] != '*' and string_without_tab[0] != '#'):
            file_w.write(i)

    file_w.close()


def converting_decimal_degrees_to_meters(point):
    new_poit = []

    for i in point:
        (new_x, new_y) = i

        new_poit.append((new_x * (60**2 * 30.87), new_y * (60**2 * 30.87)))

    return new_poit


def string_point_conversion(points_routes):
    str_id_node = ""

    route_length = 0

    len_rota = len(points_routes)

    for i in range(len_rota):
        id_node_1 = G._node.get(points_routes[i])

        str_id_node += str(id_node_1['id']) + " "

        if (i < len_rota - 1):
            route_length += G.get_edge_data(points_routes[i], points_routes[i + 1])['weight']

    if (route_length != 0):
        route_length = truncated(route_length)

    route_length_str = str(route_length)

    return str_id_node, route_length_str


def get_node_line(arquive, line):
    node = linecache.getline(arquive, line)

    node_split = node.strip().split(' ')
    node_line = (node_split[3], node_split[2])
    
    return node_line


def creator_geojson(id_node, name_arquive):
    file_w = check_file((name_arquive + ".geojson"), "w")

    file_w.write("{\n\t\"type\": \"FeatureCollection\",\n\t\"features\": [")
    file_w.write("\n\t\t{\n\t\t\t\"type\": \"Feature\",\n\t\t\t\"geometry\": {\n\t\t\t\t\"type\": \"LineString\",\n\t\t\t\t\"coordinates\": [\n")

    for i in id_node[0:-1]:
        number_line = check_conversion(i, int)
        position_node = get_node_line((global_point_file_name + ".txt"), (number_line + 1))

        file_w.write("\n\t\t\t\t\t[" + "\n\t\t\t\t\t\t" + position_node[0] + "," + "\n\t\t\t\t\t\t" + position_node[1] + "\n\t\t\t\t\t],")

    number_line = check_conversion(id_node[-1], int)
    position_node = get_node_line((global_point_file_name + ".txt"), (number_line + 1))

    file_w.write("\n\t\t\t\t\t[" + "\n\t\t\t\t\t\t" + position_node[0] + "," + "\n\t\t\t\t\t\t" + position_node[1] + "\n\t\t\t\t\t]")
    file_w.write("\n\t\t\t\t]\n\t\t\t}\n\t\t}\n\t]\n}\n")

    file_w.close()


#distância euclidiana
def heuristic_based_on_the_distance_between_points(starting_point, arrival_point):
    (x_starting_point, y_starting_point) = starting_point
    (x_arrival_point, y_arrival_point) = arrival_point

    s = ((x_starting_point - x_arrival_point)**2) + ((y_starting_point - y_arrival_point)**2)

    return sqrt(s)


def route_generator(destination_point_list):
    global_routes_file_name = name_file(global_main_directory_path, "routes_")
    
    file_w = check_file((global_routes_file_name + ".txt"), "w")

    path_geojson = creator_dir(global_main_directory_path, ("route_geojson_" + current_day() + "/"))

    for i in destination_point_list:

        for j in G.nodes():
            points_routes = nx.astar_path(G, j, i[0], heuristic=heuristic_based_on_the_distance_between_points,
            weight="weight")

            str_route, route_length = string_point_conversion(points_routes)
            str_route_split = str_route.split()

            codec = f"of_{str_route_split[0]}_for_{str_route_split[-1]}"
            name_route = f"route_my_house_{codec}"

            file_geojson = name_file(path_geojson, name_route + "_")

            creator_geojson(str_route_split, file_geojson)
            
            file_w.write(f"{name_route} {route_length} {global_file_name}.geojson\n")

    file_w.close()


def edge_creator(list_of_id_and_position):
    x_and_y_in_meters = converting_decimal_degrees_to_meters(list_of_id_and_position)

    for i in range(len(x_and_y_in_meters) - 1):
        len_distancia = heuristic_based_on_the_distance_between_points(x_and_y_in_meters[i], x_and_y_in_meters[i + 1])

        #add uma vertice ponderada
        G.add_edge(x_and_y_in_meters[i], x_and_y_in_meters[i + 1],
         weight=len_distancia)


def node_creator(nodes, nodes_id):
    x_and_y_in_meters = converting_decimal_degrees_to_meters(nodes)

    for i, j in zip(x_and_y_in_meters, nodes_id):
        G.add_node(i, id = j)


def graph_creator(file_name, destination_point):
    id_node = ""  

    file_r = check_file(file_name, "r")

    flag_node_repetition = True

    nodes = []
    nodes_id = []
    node_elements = []
    destination_point_list = []
    list_of_id_and_position = []

    for i in file_r:
        string_without_tab = i.strip()

        #tratamento das linhas que começão com #
        if(string_without_tab[0] == '#'):
            if (list_of_id_and_position):
                #criando nó
                node_creator(nodes, nodes_id)

                #criando aresta
                edge_creator(list_of_id_and_position)

                nodes = []
                nodes_id = []
                list_of_id_and_position = []

            continue

        #tratamento das linhas que começão com *
        elif (string_without_tab[0] != '*'):
            #as informações do nó está nesse formato: id point_name position_in_metros x y
            node_elements = string_without_tab.split(' ')

            x = check_conversion(node_elements[3], float)
            y = check_conversion(node_elements[2], float)
            id_node = check_conversion(node_elements[0], int)

            nodes.append((x, y))
            nodes_id.append(id_node)

        else:
            node_elements = string_without_tab[1:].split(' ')

            x = check_conversion(node_elements[3], float)
            y = check_conversion(node_elements[2], float)

            flag_node_repetition = False 

        if (destination_point in node_elements[1] and flag_node_repetition):
            aux_conv = converting_decimal_degrees_to_meters([(x, y)])
            destination_point_list.append((aux_conv[0], id_node))

        flag_node_repetition = True    
        
        list_of_id_and_position.append((x, y))
    
    file_r.close()

    return destination_point_list


def main():
    #inicio de tratamento de parametros
    parse = argparse.ArgumentParser(description='argv')

    parse.add_argument('--file_graphs', '-fg', required=True, help="input file name")
    parse.add_argument('--file_png', '-fp', help= "input file name")

    argv = parse.parse_args()
    
    file_graphs = format(argv.file_graphs)
    file_png = format(argv.file_png)
    #fim de tratamento de parametros

    destination_point = "bus_stop_"

    #fazendo um novo arquivo .png 
    if (file_png != "None"):
        file_r = check_file(file_png, "r")
        file_r.close()

        destination_point_list = graph_creator(file_graphs, destination_point)

        nx.draw(G)
        plt.savefig(file_png)

        print("Alteração realizada com sucesso.")

        exit(0)

    file_node_creator(file_graphs)

    destination_point_list = graph_creator(file_graphs, destination_point)

    route_generator(destination_point_list)

    #desenha o grafo criado
    nx.draw(G)

    #salva o desenho em um arquivo .png
    img_graph = name_file(global_main_directory_path, "graph_")
    plt.savefig((img_graph + ".png"))


if __name__ == '__main__':
    main()