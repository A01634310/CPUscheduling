from tabulate import tabulate

scheduling = ''
quantum = ''
p_time = []
p_action = []
p_pid = []
p_prio = []

def read_file():
    global scheduling, quantum, p_time, p_action, p_pid, p_prio
    with open('example.in', 'r') as f:
        scheduling = f.readline().split(None, 1)[0].strip()
        quantum = f.readline().split()[1].strip()
        next_line = f.readline().strip()
        while next_line.split()[1] != 'endSimulacion':
            p_time.append(next_line.split()[0])
            p_action.append(next_line.split()[1])
            p_pid.append(next_line.split()[2])
            try: p_prio.append(next_line.split()[4])
            except IndexError: p_prio.append('')
            next_line = f.readline().strip()

def RoundRobin(quantum, p_time, p_action, p_pid):
    print('Vamos a hacer RoundRobin')

def PriorityNotPreentive(quantum, p_time, p_action, p_pid, p_prio):
    print('Vamos a hacer Priority Not Preentive')

read_file()
if scheduling == 'RR': RoundRobin(quantum, p_time, p_action, p_pid)
if scheduling == 'prioNotPreentive': PriorityNotPreentive(quantum, p_time, p_action, p_pid, p_prio)