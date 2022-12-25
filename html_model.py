from abc import abstractmethod

import memory
from memory import virtualMemory

class HTMLmodel:
    def __init__(self,tag):
        self.tag = tag
        self.parent = None

class ContainerModel(HTMLmodel):
    def __init__(self,tag):
        super().__init__(tag)
        self.child_nodes = []

    def add_child(self,data):
        self.child_nodes.append(data)
        if issubclass(type(data),HTMLmodel):
            data.parent = self

class Var(HTMLmodel):
    def __init__(self,tag):
        super().__init__(tag)
        self.name = None
    def setName(self,name):
        self.name = name

class Article(ContainerModel):
    def __init__(self, tag):
        super().__init__(tag)

    def _run(self,statement):
        if len(statement) == 1:
            assert statement[0] != '+', 'syntax error : + is not only'
            assert statement[0] != '=', 'syntax error : = is not only'
            if type(statement[0]) is Var:
                assert memory.virtualMemory.get().get(statement[0].name) is not None, 'variable is not declared'
                return memory.virtualMemory.get()[statement[0].name]
            return statement[0]

        for i, node in enumerate(statement):
            if node == '=':
                assert i == 1, '= left value not exist'
                assert i < len(statement) - 1, '= right value not exist'
                assert type(statement[0]) is Var,'= left value is not Var tag'
                lvalue = statement[0].name
                rvalue = self._run(statement[i+1:])
                assert memory.virtualMemory.get().get(lvalue) is not None, 'variable is not declared'
                memory.virtualMemory.get()[lvalue] = rvalue
                return rvalue
            if node == '+':
                assert i == 1, '= left value not exist'
                assert i < len(statement) - 1, '= right value not exist'
                lvalue = self._run(statement[:i])
                rvalue = self._run(statement[i + 1:])
                return lvalue + rvalue

    def run(self):
        return self._run(self.child_nodes)




class P(ContainerModel):
    def __init__(self,tag):
        super().__init__(tag)

    def run(self):
        if type(self.child_nodes[0]) is Article:
            printValue = self.child_nodes[0].run()
            print(printValue)
            return printValue
        if type(self.child_nodes[0]) is str:
            printValue = self.child_nodes[0]
            print(printValue)
            return printValue

class Input(HTMLmodel):
    def __init__(self,tag,attrs):
        super().__init__(tag)
        self.name = None
        self.data_type = None
        self.value = None
        for attr in attrs:
            attr_name = attr[0]
            attr_value = attr[1]
            if attr_name == 'name':
                self.name = attr_value
                continue
            if attr_name == 'type':
                self.data_type = attr_value
                continue
            if attr_name == 'value':
                self.value = attr_value
                continue
        assert self.name is not None, 'input name not exist'
        assert self.data_type is not None,'input type not exist'
        assert self.value is not None,'input value not exist'
    def run(self):
        assert memory.virtualMemory.get().get(self.name) is None, 'variable already declared'
        memory.virtualMemory.get()[self.name] = self.value