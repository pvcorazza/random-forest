import copy
import math

class Node(object):
    def __init__(self):
        self.attribute = None
        self.parent_value = None
        self.childs = None


class Tree(object):
    def __init__(self, data):
        self.attributes = data[0]
        self.attributes.pop(len(self.attributes)-1)
        self.data = data
        self.data.pop(0)
        self.class_entropy = self.info(data,len(self.attributes)-1)
        self.root = self.build_decision_tree(self.data, self.attributes)

    # Possíveis valores para o atributo
    def get_possible_values(self, data, attribute):
        return set([row[attribute] for row in data])

    # Separa os dados em listas baseado nos atributos do index
    def get_child_node_data(self, data, index_attribute, value):
        new_data = []
        for instance in data:
            if (instance[index_attribute] == value):
                new_data.append(instance)
        return new_data

    # Verifica se todos os valores possuem a mesma classe
    def is_same_class(self, data):
        possible_values = self.get_possible_values(data, len(data[0])-1)
        if (len(possible_values) == 1):
            return True
        return False


    def info (self, data, index_attribute):
        all_values = [row[index_attribute] for row in data]
        possible_values = self.get_possible_values(data, index_attribute)
        total_values = len(all_values)

        entropy = 0

        for val in possible_values:
            entropy=entropy-(all_values.count(val)/total_values)*math.log(all_values.count(val)/total_values,2)

        return entropy


    def info_attribute(self, data, index_attribute):
        all_values = [row[index_attribute] for row in data]
        possible_values = self.get_possible_values(data, index_attribute)
        total_values = len(all_values)

        entropy = 0

        for val in possible_values:
            new_data = self.get_child_node_data(data, index_attribute, val)
            entropy=entropy+(len(new_data)/total_values)*self.info(new_data, len(data[0])-1)

        return entropy

    def gain(self, data, index_attribute):
        return self.class_entropy - self.info_attribute(data, index_attribute)

    def get_most_frequent_class(self, data):
        all_values = [row[len(data[0])-1] for row in data]
        print(all_values)

    def build_decision_tree(self, data, attributes):


        # Cria novo nodo
        root = Node()

        # Se todos os valores possuem a mesma classe, retorna um nó folha com o valor dessa classe
        if self.is_same_class(data):
            root.attribute = data[0][len(data[0]) -1]
            return root

        # if len(header) < 1:
        #     return self.get_most_frequent_class(data, self.index_class)
        #
        # print(self.get_most_frequent_class(data,self.index_class))
        if not attributes:
            new_node = Node()  # self.get_most_frequent_class(new_data)
            new_node.attribute = "Nao"
            return new_node

        # Encontra atributo que apresenta o melhor critério de divisão
        gains = []
        for attribute in attributes:
            index_attribute = attributes.index(attribute)
            gains.append(self.gain(data, index_attribute))
        maxIndex = gains.index(max(gains))
        value = attributes[maxIndex]
        index = attributes.index(value)

        # Associa atributo ao nodo
        root.attribute = value

        # Remove atributo da lista de atributos
        attributes.pop(index)

        # Encontra os possíveis valores para determinado atributo e adiciona um filho relativo a cada valor
        possible_values = self.get_possible_values(data, index)

        root.childs = []

        # Para cada valor distindo do atributo encontra um subconjunto dos dados onde existe esse valor
        for value in possible_values:
            new_data = self.get_child_node_data(data, index, value)
            for x in new_data:
                del x[index]

            # Se o subconjunto é vazio, retorna um nodo folha com a classe mais frequente no subconjunto
            # Senão, associa uma subárvore ao nodo, com os novos dados de treinamento
            if not new_data:
                new_node = Node() # self.get_most_frequent_class(new_data)
                new_node.attribute = "Nao"
            else:
                new_node = self.build_decision_tree(new_data, copy.deepcopy(attributes))
                new_node.parent_value = value
            root.childs.append(new_node)

        return root