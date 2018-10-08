import copy
import math
from collections import deque


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
        self.root = self.build_decision_tree(copy.deepcopy(self.data), self.attributes)

    # Possíveis valores para o atributo
    def get_possible_values(self, data, attribute):
        return list(set([row[attribute] for row in data]))

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

    def get_most_frequent_class(self):
        all_values = [row[len(self.data[0])-1] for row in self.data]
        return max(set(all_values), key=all_values.count)

    def is_continuous(self, possible_values):
        is_continuous = False

        try:
            float(list(possible_values)[0])
            is_continuous = True
        except ValueError:
            is_continuous = False

        return is_continuous

    def build_decision_tree(self, data, attributes):

        # Cria novo nodo
        root = Node()

        # Se todos os valores possuem a mesma classe, retorna um nó folha com o valor dessa classe
        if self.is_same_class(data):
            root.attribute = data[0][len(data[0]) -1]
            return root

        # Se a lista de atributos é vazia, retorna um nó folha com a classe mais frequente no dataset
        if not attributes:
            root.attribute = self.get_most_frequent_class()
            return root

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

        average=None
        continuous = self.is_continuous(possible_values)
        majors = []
        minors = []
        if(continuous):
            values = [float(i) for i in possible_values]
            average = sum(values)/len(values)
            for value in possible_values:
                new_data = self.get_child_node_data(data, index, value)
                if float(value)<=average:
                    minors.append(new_data[0])
                else:
                    majors.append(new_data[0])

            possible_values = ["<="+str(average), ">"+str(average)]
            print(possible_values)

        root.childs = []

        # Para cada valor distinto do atributo encontra um subconjunto dos dados onde existe esse valor
        for value in possible_values:

            new_data = []

            if (continuous):
               if (value[0] == "<"):
                   new_data = minors
               else:
                   new_data = majors
            else:
                new_data = self.get_child_node_data(data, index, value)

            for x in new_data:
                del x[index]

            # Se o subconjunto é vazio, retorna um nodo folha com a classe mais frequente no subconjunto
            # Senão, associa uma subárvore ao nodo, com os novos dados de treinamento
            if not new_data:
                new_node = Node()
                new_node.attribute = self.get_most_frequent_class()
            else:
                new_node = self.build_decision_tree(new_data, copy.deepcopy(attributes))
                new_node.parent_value = value
            root.childs.append(new_node)

        return root

    def printTree(self):
        if self.root:
            roots = deque()
            roots.append(self.root)
            while len(roots) > 0:
                root = roots.popleft()
                print(root.attribute)
                if (root.childs):
                    for child in root.childs:
                        print(child.parent_value)
                        print('({})'.format(child.attribute))
                        roots.append(child)
                elif root.attribute:
                    print(root.attribute)