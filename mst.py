from threading import Thread
from queue import Queue
from time import sleep


class Node(Thread):
    def __init__(self, uid: int):
        Thread.__init__(self)
        # Vars
        self.uid = uid
        self.papa = None
        self.children = []
        self.neighbours = []

        self.q = Queue()

    def __str__(self):
        return "Node[{}]".format(self.uid)

    def __repr__(self):
        return self.__str__()

    def msg(self, *msg: tuple):
        """ send message to this node """
        self.q.put(msg)

    def run(self):
        """ simple on-receive loop - can be substituted by actors from some lib"""
        while True:
            while not self.q.empty():
                title, val = self.q.get()
                self.__getattribute__(title)(val)
            sleep(1)

    def look_im_your_papa(self, node):
        """ parent --> child """
        if self.papa is None:
            # Sure you are
            self.papa = node
            # I'll tell my children they have a grandpa
            for n in self.neighbours:
                n.msg("look_im_your_papa", self)
            self.papa.msg("hey_papa", self)
        else:
            # I already have a papa
            pass

    def hey_papa(self, node):
        """ child --> parent """
        self.children.append(node)


def main():
    graph = {
        0: [1],
        1: [0, 2, 3],
        2: [3],
        3: [1, 2]
    }

    nodes = [Node(i) for i in graph]
    for n in nodes:
        n.neighbours = [a for a in nodes if a.uid in graph[n.uid]]

    for n in nodes:
        n.start()

    # Start spanning tree from node[0]
    nodes[0].msg("look_im_your_papa", nodes[0])

    sleep(3)
    for n in nodes:
        print("{} : papa: {} children: {}".format(n, n.papa, n.children))


if __name__ == "__main__":
    main()