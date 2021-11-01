class Node:
    def __init__(self, value: str):
        self.value: str = value
        self.rightChild: Node or None = None
        self.leftChild: Node or None = None

    def setValue(self, value: str):
        self.value = value

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
    def __init__(self, root: Node):
        self.root = root
        self.listNodes: list = []

    def getRootValue(self):
        return self.root.getValue()

    def getRoot(self):
        return self.root

    def appendListNodes(self, value):
        self.listNodes.append(value)

    def clearListNodes(self):
        self.listNodes = []

    def listNodesToString(self):
        str = ""
        for item in self.listNodes:
            str += item + " "
        return str


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


def thereIsNoRightChild(node: Node):
    return node.getRightChild() is None


def thereIsNoLeftChild(node: Node):
    return node.getLeftChild() is None


def toTree(arr: list, node: str or Node, tree: Tree):

    if isOperator(node.getValue()):
        if thereIsNoRightChild(node):
            node.setRightChild(Node(arr.pop(0)))
            toTree(arr, node.getRightChild(), tree)
        if thereIsNoLeftChild(node):
            node.setLeftChild(Node(arr.pop(0)))
            toTree(arr, node.getLeftChild(), tree)


def popAndEnqueueInternalParentesisContent(stack, queue):
    while stack.peek() != "(":
        popAndEnqueue(stack, queue)
    stack.pop()


def popAndEnqueue(stack, queue):
    item = stack.pop()
    if item != "(" or item != ")":
        queue.enqueue(item)


def isChildLowPriority(node: Node, child: Node):
    priorityOne = ["+", "-"]
    priorityZero = ["/", "*"]

    return child.getValue() in priorityOne and node.getValue() in priorityZero


def toString(node: Node, tree: Tree):
    if isOperator(node.getValue()):
        right: Node = node.getRightChild()
        left: Node = node.getLeftChild()
        if left.getValue() is not None:
            childWithLowPriority = isChildLowPriority(node, left)
            if childWithLowPriority:
                tree.appendListNodes("(")
            toString(left, tree)
            tree.appendListNodes(node.getValue())
            if childWithLowPriority:
                tree.appendListNodes(")")
        if right.getValue() is not None:
            childWithLowPriority = isChildLowPriority(node, right)
            if childWithLowPriority:
                tree.appendListNodes("(")
            toString(right, tree)
            if childWithLowPriority:
                tree.appendListNodes(")")
    else:
        tree.appendListNodes(node.getValue())

    if node == tree.getRoot():
        print(tree.listNodesToString())


def evaluate(right: float, left: float, operation: str):
    if operation == "+":
        return left + right
    elif operation == "-":
        return left - right
    elif operation == "*":
        return left*right
    elif operation == "/":
        if right != 0:
            return left/right
        else:
            print("Divisão por zero não permitida.")
            exit(0)


def walkToOperation(node: Node):
    if isOperator(node.getValue()):
        right: Node = node.getRightChild()
        left: Node = node.getLeftChild()
        if not isOperator(right.getValue()) and not isOperator(left.getValue()):
            return node
        else:
            if isOperator(left.getValue()):
                return walkToOperation(left)
            elif isOperator(right.getValue()):
                return walkToOperation(right)


def evalStep(tree: Tree):
    toString(tree.getRoot(), tree)
    root: Node = tree.getRoot()

    while isOperator(root.getValue()):
        # Descendo até o ultimo nó antes das folhas mais inferiores
        node = walkToOperation(root)

        # Casting para int
        right = float(node.getRightChild().getValue())
        left = float(node.getLeftChild().getValue())
        operation = node.getValue()

        # Avaliando a operaçao
        result = evaluate(right, left, operation)

        # Substituindo na arvore
        # Essa formataçao é pra tirar as casas decimais do float se necessario
        node.setValue('{0:.2f}'.format(result).rstrip('0').rstrip('.'))
        node.setRightChild(None)
        node.setLeftChild(None)

        tree.clearListNodes()
        toString(tree.getRoot(), tree)


def shuntingYard(tokens: list):
    stack = Stack()
    queue = Queue()

    priorityOne = ["+", "-"]
    priorityZero = ["/", "*"]

    for token in tokens:
        if isOperator(token):
            if stack.size() > 0:
                top = stack.peek()
                while stack.size() > 0 and top in priorityZero and (token in priorityOne or token in priorityZero):
                    popAndEnqueue(stack, queue)
                    top = stack.peek()
            stack.push(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            popAndEnqueueInternalParentesisContent(stack, queue)
        else:
            queue.enqueue(token)

    # Se restar algo na stack (exemplo: parenteses extras) entao a operaçao é inválida e nao será realizada
    if stack.size() != 0:
        print("Operação Inválida!")
        exit(0)

    return queue


def parser(tokens: list):
    queue = shuntingYard(tokens)

    # Reverter a queue pra que a ordem de avaliação das expressões fique correta
    queue.reverseQueue()

    rootElem = queue.dequeue()
    rootNode = Node(rootElem)

    # Transformando a queue em lista simples para que seja mais fácil de lidar
    listOfNodes = queue.getItems()

    tree = Tree(rootNode)
    toTree(listOfNodes, rootNode, tree)

    return tree


def lexer(op: str):
    tokens = op.split(" ")

    # Adiçao de parenteses na expressão geral para que a parse funcione corretamente
    tokens.insert(0, "(")
    tokens.append(")")

    return tokens


def runTests():

    testCases = {
        0: ("4 + 18 / ( 9 - 3 )", ['(', '4', '+', '18', '/', '(', '9', '-', '3', ')', ')'], ['4', '18', '9', '3', '-', '/', '+'], '+', ('-', '9', '3')),
        1: ("7 * 100 / ( 20 - 10 ) + 15 * 3", ['(', '7', '*', '100', '/', '(', '20', '-', '10', ')', '+', '15', '*', '3', ')'], ['7', '100', '*', '20', '10', '-', '/', '15', '3', '*', '+'], '+', ('*', '7', '100'))
        # 2: ("(1 + 2 + 3) * 4"),
        # 3: ("(10 / 3 + 23) * (1 - 4)"),
        # 4: ("58 - -8 * (58 + 31) - -14"),
        # 5: ("-71 * (-76 * 91 * (10 - 5 - -82) - -79)"),
    }

    for key, case in testCases.items():
        print("Caso ", key)
        operation = case[0]

        lexerResponse = lexer(operation)
        assert lexerResponse == case[1]

        shuntingYardResponse = shuntingYard(lexerResponse)
        assert shuntingYardResponse.getItems() == case[2]

        parserResponse = parser(lexerResponse)
        assert parserResponse.getRootValue() == case[3]

        operationResponse = walkToOperation(parserResponse.getRoot())
        assert operationResponse.getValue() == case[4][0]
        assert operationResponse.getLeftChild().getValue() == case[4][1]
        assert operationResponse.getRightChild().getValue() == case[4][2]

        evalStep(parserResponse)
        assert parserResponse.getRoot().getValue().isnumeric()
        print('\n')


if __name__ == '__main__':
    runTests()

