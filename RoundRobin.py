from tabulate import tabulate

scheduling = ''
quantum = 0
terminacion = 0
str_eventos = []

def read_file():
    eventos = []
    with open('example.in', 'r') as f:
        global scheduling, scheduling, terminacion, str_eventos, quantum
        scheduling = f.readline().split(None, 1)[0].strip()
        quantum = int(f.readline().split()[1].strip())
        next_line = f.readline().strip()
        while next_line.split()[1] != 'endSimulacion':
            str_eventos.append(next_line)
            prio = 0
            if scheduling == 'prioNonPreemptive': prio = int(next_line.split()[4])
            eventos.append({
                'Tiempo':int(next_line.split()[0]),
                'Accion':next_line.split()[1],
                'PID':next_line.split()[2],
                'Prio':int(prio)
            })
            next_line = f.readline().strip()
        str_eventos.append(next_line)
        terminacion = int(next_line.split()[0])
    return eventos

def RoundRobin(quantum, eventos, benchmark):
    listos = []
    bloqueados = []
    terminados = []
    cpu = { 'PID':'', 'entrada':0 }
    output_table = [['Evento','Cola de listos','CPU','Bloqueados','Terminados']]

    # Primer evento
    e = eventos.pop(0)
    str_evento = ''
    for t in range(0,terminacion):
        str_evento = ''
        special = False

        # Si llega algún evento
        if t == e['Tiempo']:
            special = True
            accion = e['Accion']
            p_id = e['PID']
            str_evento = str_eventos.pop(0)
            if accion == 'Llega':
                listos.insert(0, p_id)
            elif accion == 'Acaba':
                terminados.append(p_id)
                # Si se acaba el proceso actualmente ejecutándose
                if p_id == cpu['PID']:
                    cpu['PID'] = ''
                    cpu['entrada'] = 0
                # Si se acaba un proceso en cola de listos
                else:
                    listos.remove(p_id)
            elif accion == 'startI/O':
                bloqueados.append(p_id)
                cpu['PID'] = ''
                cpu['entrada'] = 0
            elif accion == 'endI/O':
                bloqueados.remove(p_id)
                listos.insert(0, p_id)

            if len(eventos) > 0: e = eventos.pop(0)

        # Se acaba el quantum del proceso y lo regresamos a la cola de listos
        if t == cpu['entrada']+quantum:
            special = True
            listos.insert(0, cpu['PID'])
            cpu['PID'] = ''
            cpu['entrada'] = 0

        # Si el CPU está libre metemos el proceso a la cola de listos
        if cpu['PID'] == '' and len(listos) > 0:
            special = True
            if str_evento == '': str_evento = str(t) + ' quantum'
            cpu['PID'] = listos.pop()
            cpu['entrada'] = t

        if special:
            output_table.append([
                str_evento,
                ','.join(map(str, listos)),
                cpu['PID'],
                ','.join(map(str, bloqueados)),
                ','.join(map(str, terminados))
            ])

    return output_table


def PriorityNotPreentive(eventos):
    for e in eventos:
        print(e)

eventos = read_file()
if scheduling == 'RR': output_table = RoundRobin(quantum, eventos)
if scheduling == 'prioNotPreentive': output_table = PriorityNotPreentive(eventos)
print(tabulate(output_table))
