from thespian.actors import *
import time


class Node(Actor):
    def receiveMessage(self, message, sender):
        funs = {
            'init': self.init,
            'elect': self.elect,
            'conduct': self.conduct
        }
        header, payload = message['header'], message['payload']

        # Handle the request
        funs[header](payload, sender)

    @property
    def is_leader(self):
        return self.uid == self.leader_uid

    def init(self, payload, sender):
        self.uid = payload['uid']
        self.leader_uid = -1
        self.neighbour = payload['neighbour']

    def elect(self, payload, sender):
        msg = {
            'header': 'conduct',
            'payload': {'leader_uid': self.uid}
        }
        self.send(self.neighbour, msg)

    def conduct(self, payload, sender):
        leader_uid = payload['leader_uid']

        if leader_uid > self.uid:
            self.leader_uid = leader_uid
            self.send(self.neighbour, {'header': 'conduct', 'payload': payload})
        if leader_uid == self.uid:
            print("I'm leader", self.uid)


def main():
    actors = [ActorSystem().createActor(Node) for _ in range(10)]
    for i, a in enumerate(actors):
        ActorSystem().tell(a, {'header': 'init', 'payload': {'uid': i, 'neighbour': actors[(i-1) % 10]}})

    for a in actors:
        ActorSystem().tell(a, {'header': 'elect', 'payload': None})


if __name__ == "__main__":
    main()
