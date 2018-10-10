import copy
import math
from random import randrange
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
        self.root = self.build_decision_tree(copy.deepcopy(self.data), copy.deepcopy(self.attributes))

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

    # Cálculo da entropia
    def info (self, data, index_attribute):
        all_values = [row[index_attribute] for row in data]
        possible_values = self.get_possible_values(data, index_attribute)
        total_values = len(all_values)
        entropy = 0

        for val in possible_values:
            entropy=entropy-(all_values.count(val)/total_values)*math.log(all_values.count(val)/total_values,2)

        return entropy

    # Cálculo da entropia de um determinado atributo
    def info_attribute(self, data, index_attribute):
        # Todos os valores para o atributo
        all_values = [row[index_attribute] for row in data]
        # Possiveis valores para o atributo
        possible_values = self.get_possible_values(data, index_attribute)
        total_values = len(all_values)
        entropy = 0

        for val in possible_values:
            new_data = self.get_child_node_data(data, index_attribute, val)
            entropy=entropy+(len(new_data)/total_values)*self.info(new_data, len(data[0])-1)

        return entropy

    # Função para determinar o ganho de um determinado atributo
    def gain(self, data, index_attribute):
        return self.info(data,len(data[0])-1) - self.info_attribute(data, index_attribute)

    # Retorna a classe mais frequente no dataset
    def get_most_frequent_class(self):
        all_values = [row[len(self.data[0])-1] for row in self.data]
        return max(set(all_values), key=all_values.count)

    # Verifica se os valores informados são contínuos
    def is_continuous(self, possible_values):
        try:
            float(list(possible_values)[0])
            is_continuous = True
        except ValueError:
            is_continuous = False

        return is_continuous

    # Construção da árvore com o algoritmo ID3
    def build_decision_tree(self, data, attributes):

        selectedAttributes = []
        for numAttributeSelected in range(2):
            if(len(range(2)) > len(attributes)):
                for attribute in attributes:
                    selectedAttributes.append(attribute)
            else:
                selectedAttributes.append(attributes[randrange(len(attributes))])
        # Cria novo nodo
        root = Node()

        # Se todos os valores possuem a mesma classe, retorna um nó folha com o valor dessa classe
        if self.is_same_class(data):
            root.attribute = data[0][len(data[0]) -1]
            return root

        # Se a lista de atributos é vazia, retorna um nó folha com a classe mais frequente no dataset
        if not selectedAttributes:
            root.attribute = self.get_most_frequent_class()
            return root

        # Encontra atributo que apresenta o melhor critério de divisão
        gains = []
        for attribute in selectedAttributes:
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

        root.childs = []

        # Para cada valor distinto do atributo encontra um subconjunto dos dados onde existe esse valor
        for value in possible_values:
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
                new_node = self.build_decision_tree(copy.deepcopy(new_data), copy.deepcopy(attributes))
                new_node.parent_value = value
            root.childs.append(new_node)

        return root

    # Impressão da árvore para debug
    def printTree(self, root):
        if root:
            if root.parent_value:
                print("----->  " + root.parent_value + " ---> " + root.attribute)
            else:
                print("-----  " + root.attribute + "  -----")
            if (root.childs):
                for child in root.childs:
                    self.printTree(child)
                print()


    # Retorna o valor predito para a instância
    def classify(self, instance, node):
        predicted = None
        if node:
            index = self.attributes.index(node.attribute)
            continuous = self.is_continuous(instance[index])
            if (continuous):
                for child in node.childs:
                    if "<" in child.parent_value:
                        val = child.parent_value.replace("<", "")
                        val = float(val.replace("=", ""))
                        if float(instance[index]) <= val:
                            if not child.childs:
                                return child.attribute
                            else:
                                predicted = self.classify(instance, child)
                    else:
                        val = float(child.parent_value.replace(">", ""))
                        if float(instance[index]) > val:
                            if not child.childs:
                                return child.attribute
                            else:
                                predicted = self.classify(instance, child)

            else:
                for child in node.childs:
                    if child.parent_value == instance[index]:
                        if not child.childs:
                            return child.attribute
                        else:
                            predicted=self.classify(instance, child)

        return predicted