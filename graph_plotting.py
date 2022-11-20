from ast import parse
import argparse

from math import sqrt

from pyvis.network import Network
from random import random 


net = Network()


def truncado(num):
    num_complet = ""

    num_str = str(num)
    num_str = num_str.split('.')

    num_complet = num_str[0] + '.' + num_str[1][0:2]

    num = float(num_complet)

    return num


def random_hex_color(end = 0xffffff):
    return '#%06X' % round(random() * end)


def check_file(file_t):
    try:
        f = open(file_t, "r")

    except:
        print(f"O arquivo {file_t} não existe ou não pode ser aberto.")

        exit(0)

    return f


def check_conversion(elemento, type_conversion):
    new_element = 0
    try:
        new_element = type_conversion(elemento)

    except:
        print("Algo deu errado na conversão do valor.")

        exit(1)

    return new_element


def conversion_grau_dec_metros(point):
    new_poit = []

    for i in point:
        (x, y) = i

        new_x = check_conversion(x, float)
        new_y = check_conversion(y, float)

        new_poit.append((new_x * (60**2 * 30.87), new_y * (60**2 * 30.87)))

    return new_poit


def heuristic_based_on_the_distance_between_points(starting_point, arrival_point):
    (x_starting_point, y_starting_point) = starting_point
    (x_arrival_point, y_arrival_point) = arrival_point

    s = ((x_starting_point - x_arrival_point)**2) + ((y_starting_point - y_arrival_point)**2)

    return sqrt(s)


def edge_creator(list_of_id_and_position_in_meter, edge_color):
    for i in range(len(list_of_id_and_position_in_meter) - 1):
        graus_in_metros = conversion_grau_dec_metros([list_of_id_and_position_in_meter[i][1], 
        list_of_id_and_position_in_meter[i + 1][1]])

        len_distancia = heuristic_based_on_the_distance_between_points(graus_in_metros[0], graus_in_metros[1])

        len_distancia = truncado(len_distancia)

        net.add_edge(list_of_id_and_position_in_meter[i][0], list_of_id_and_position_in_meter[i + 1][0],
            label=str(len_distancia), color=edge_color)


def graph_file_reader(file_name):
    file_r = check_file(file_name)

    node_elements = []
    list_of_id_and_position_in_meter = []

    for i in file_r:
        string_without_tab = i.strip()

        #tratamento das linhas que começão com #
        if(string_without_tab[0] == '#'):
            node_color = random_hex_color()

            if (list_of_id_and_position_in_meter):
                edge_creator(list_of_id_and_position_in_meter, random_hex_color())

                list_of_id_and_position_in_meter = []

            continue

        #tratamento das linhas que começão com *
        elif (string_without_tab[0] != '*'):
            #as informações do nó está nesse formato: id point_name position_in_metros x y
            node_elements = string_without_tab.split(' ')

            label_node = ' '.join(node_elements[1:])
            id_node = check_conversion(node_elements[0], int)
            net.add_node(id_node, label=label_node, color=node_color)

        else:
            node_elements = string_without_tab[1:].split(' ')

            id_node = check_conversion(node_elements[0], int)            
        
        list_of_id_and_position_in_meter.append([id_node, (node_elements[3], node_elements[2])])
    
    file_r.close()


def main():
    parse = argparse.ArgumentParser(description='argv')
    parse.add_argument('file_txt_entry', help= "input file name")
    args = parse.parse_args()
    
    file_txt_entry = format(args.file_txt_entry)

    graph_file_reader(file_txt_entry)

    net.show_buttons(filter_=['physics'])
    net.show('plot_graphs.html')


if __name__ == '__main__':
    main()