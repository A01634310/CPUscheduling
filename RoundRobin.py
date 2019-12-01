from tabulate import tabulate

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

scheduling = ''
quantum = ''

def read_file():
    eventos = []
    with open('example.in', 'r') as f:
        global scheduling
        global quantum
        scheduling = f.readline().split(None, 1)[0].strip()
        quantum = f.readline().split()[1].strip()
        next_line = f.readline().strip()
        while next_line.split()[1] != 'endSimulacion':

            # Para el caso de RR
            prio = ''
            if scheduling == 'prioNonPreemptive': prio = next_line.split()[4]

            eventos.append({
                'Tiempo':next_line.split()[0],
                'Accion':next_line.split()[1],
                'PID':next_line.split()[2],
                'Prio':prio
            })
            next_line = f.readline().strip()
    return eventos

def RoundRobin(quantum, eventos):
    for e in eventos:
        print(e)

def PriorityNotPreentive(eventos):
    for e in eventos:
        print(e)

eventos = read_file()
if scheduling == 'RR': RoundRobin(quantum, eventos)
if scheduling == 'prioNotPreentive': PriorityNotPreentive(eventos)