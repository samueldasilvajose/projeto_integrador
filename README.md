# Projeto integrador
construção de rotas e plotagem do mapa

## Instalação
O programa foi construido e testado usando o python 3.8.10 e ultiliza as bibliotecas networkx, matplotlib, pyvis. Abaixo estão o metodo de instalação.

    pip3 install networkx
    pip3 install matplotlib
    pip3 install pyvis

## Método de execução
O programa necessita somente do arquivo txt que contenha os pontos necessarios para a construção das rotas, exemplo para construção das rotas: 

    python3 route_builder_using_graphs.py -fg list_of_graph_points_near_my_house.txt

 Esse comando irá criar um diretório chamado "process_result" no mesmo diretório de execução do arquivo, esse diretório irá conter subdiretorios, esse diretório possui o nome baseado no horário e dia atual, com a saída definitiva do programa. Essa saída é composta por três arquivos, sendo um arquivo que contem os pontos, outro que contem as rotas e um arquivo ".png" que contem um desenho do grafo produzido na execução do programa.

 Existe um programa auxiliar que é utilizado para construir um grafo para vizualizar melhor as informações inseridas, ele requer também o nome do arquivo com as informações dos nos, exmplo para platagem do grafo:

    python3 graph_plotting.py list_of_graph_points_near_my_house.txt

Ao ser executado esse programa será gerado um arquivo ".html" e irá aparecer uma nova pagina web.

## Considerações
O arquivo usado nos exemplos já está presente no respositório, ele usa um padrão meio especifico de organizar as informações, algumas delas citadas a baixo:

- O "#" demarca as linhas que são o inicio das sequencias de pontos de uma rota completa.
- O "*" demarca os nós que já foram mostrados anteriormente
- A estrutura basica de uma linha é id do nó (representado por um inteiro), nome do nó, posição em graus decimais, y e x, iqual os dados fornecidos pelo google maps
- Ás informações são separadas por um espaço em branco