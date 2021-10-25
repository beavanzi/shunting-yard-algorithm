# This is a sample Python script.

# Press ⌃F5 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
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

    def getItself(self):
        return self.value

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

class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


def isOperator(op):
    return op == "+" or op == "-" or op == "*" or op == "/"


def toTree(arr, elem: None or int):
    if elem is not Node:
        node = Node(elem)
    else:
        node = elem

    if isOperator(node.value):
        if node.rightChild is None:
            node.setRightChild(arr.pop(0))
            toTree(arr, node.rightChild)
        if node.leftChild is None:
            node.setLeftChild(arr.pop(0))
            toTree(arr, node.leftChild)
    print(node.value)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    arr = ["+", "/", "-", 3, 9, 18, 4]
    root = arr.pop(0)
    toTree(arr, root)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
