class Node:

    def __init__(self, value: object):
        self.value = value
        self.rightChild = None
        self.leftChild = None

    def setRightChild(self, right):
        self.rightChild = right

    def setLeftChild(self, left):
        self.leftChild = left

    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    def getValue(self):
        return self.value


class Tree:

    def __init__(self):
        root = None
        height = None

    def toString(self):
        return 0


class Stack:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(-1)

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def getItems(self):
        return self.items


class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def peekFirst(self):
        return self.items[0]

    def size(self):
        return len(self.items)

    def getItems(self):
        return self.items

    def reverseQueue(self):
        self.items.reverse()


def isOperator(op):
    return op == "+" or op == "-" or op == "*" or op == "/"


def toTree(arr: list, elem: str or Node or int):
    if elem is not Node:
        node = Node(elem)
    else:
        node = elem

    if isOperator(node.getValue()):
        if node.getRightChild() is None:
            node.setRightChild(arr.pop(0))
            toTree(arr, node.getRightChild())
        if node.getLeftChild() is None:
            node.setLeftChild(arr.pop(0))
            toTree(arr, node.getLeftChild())
    print(node.getValue())


def popAndEnqueueInternalParentesisContent(stack, queue):
    while stack.peek() != "(":
        popAndEnqueue(stack, queue)
    stack.pop()


def popAndEnqueue(stack, queue):
    item = stack.pop()
    if item != "(" or item != ")":
        queue.enqueue(item)


def evalStep():
    return 0


def shuntingYard(tokens: list):
    stack = Stack()
    queue = Queue()

    priorityOne = ["+", "-"]
    priorityZero = ["*", "/"]

    for token in tokens:
        if isOperator(token):
            if stack.size() > 0 and stack.peek() in priorityZero:
                if token in priorityZero:
                    stack.push(token)
                elif token in priorityOne:
                    popAndEnqueue(stack, queue)
                    stack.push(token)
            else:
                stack.push(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            popAndEnqueueInternalParentesisContent(stack, queue)
        else:
            queue.enqueue(token)

    # Se restar algo na stack (exemplo: parentenses extras) entao a operaçao é inválida e nao será realizada
    if stack.size() != 0:
        print("Operação Inválida!")
        exit(0)

    return queue


def parser(tokens: list):

    queue = shuntingYard(tokens)

    # Reverter a queue pra que a ordem de avaliação das expressões fique correta
    queue.reverseQueue()

    root = queue.dequeue()

    # Transformando a queue em lista simples para que seja mais fácil de lidar
    listOfNodes = queue.getItems()

    toTree(listOfNodes, root)


def lexer(op: str):
    tokens = op.split(" ")
    # Precisa fazer uma funcao que nao leia com espaços? (Perguntar)

    # Adiçao de parenteses na expressão geral para que a parse funcione corretamente
    tokens.insert(0, "(")
    tokens.insert(-1, ")")

    return tokens


def run_tests():

    testCases = {
        0: ("4 + 18 / ( 9 - 3 )", ['(', '4', '+', '18', '/', '(', '9', '-', '3', ')', ')'], ['4', '18', '9', '3', '-', '/', '+']),
        1: ("4 + 18 / ( 9 - 3 )", ['(', '4', '+', '18', '/', '(', '9', '-', '3', ')', ')'], ['4', '18', '9', '3', '-', '/', '+'])
    }

    for key, case in testCases.items():
        operation = case[0]

        lexerResponse = lexer(operation)
        assert lexerResponse == case[1]

        shuntingYardResponse = shuntingYard(lexerResponse)
        assert shuntingYardResponse.getItems() == case[2]


if __name__ == '__main__':
    run_tests()

