from thespian.actors import *


class Node(Actor):
    def receiveMessage(self, message, sender):
        funs = {
            'initialize': self.initialize,
            'elect_start': self.elect_start,
            'elect_pass': self.elect_pass
        }
        header, payload = message['header'], message['payload']

        # Handle the request
        funs[header](message, sender)

    def initialize(self, msg, sender):
        # Obtain uid and neighbour to talk to
        self.uid = msg['payload']['uid']
        self.neighbour = msg['payload']['neighbour']
        # As of now the leader is unknown
        self.leader_uid = -1

        # I'll notify this guy if I'll be the leader :)
        self.master = sender

    def elect_start(self, msg, sender):
        # I'll start election procedure, just pass my uid to neighbour
        self.send(
            self.neighbour,
            {'header': 'elect_pass', 'payload': {'uid': self.uid}}
        )

    def elect_pass(self, msg, sender):
        # If my uid is bigger than the one that just came - DO NOT PASS

        leader_uid = msg['payload']['uid']
        if leader_uid > self.uid:
            # I'll write it to remember who is the (possible) leader
            self.leader_uid = leader_uid
            # Share this good news with neighbour
            self.send(self.neighbour, msg)
        if leader_uid == self.uid:
            # Well, I'm the leader, I'll notify my master
            self.send(self.master, "I'm the leader my master. Yours faithfully, {}".format(self.uid))


def main():
    actors = [ActorSystem().createActor(Node) for _ in range(100)]
    for i, a in enumerate(actors):
        ActorSystem().tell(a, {'header': 'initialize', 'payload': {'uid': i, 'neighbour': actors[(i-1) % 100]}})

    for a in actors:
        ActorSystem().tell(a, {'header': 'elect_start', 'payload': None})

    print(ActorSystem().listen(2))
    ActorSystem().shutdown()


if __name__ == "__main__":
    main()
