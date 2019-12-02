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
                'Tiempo': int(next_line.split()[0]),
                'Accion': next_line.split()[1],
                'PID': next_line.split()[2],
                'Prio': int(prio)
            })
            next_line = f.readline().strip()
        str_eventos.append(next_line)
        terminacion = int(next_line.split()[0])
    return eventos


# CPU Scheduling mediante RoundRobin
def RoundRobin(quantum, eventos):
    listos = []  # Procesos en la cola de listos
    bloqueados = []  # Procesos bloqueados por algún I/O
    terminados = []  # Procesos finalizados por el CPU
    cpu = {'PID': '', 'entrada': 0}  # Proceso actual que corre el CPU y cuándo comenzó
    output_table = [['Evento', 'Cola de listos', 'CPU', 'Bloqueados', 'Terminados']]
    specs_table = [['Proceso', 'Tiempo de llegada', 'Tiempo de terminación', 'Tiempo de CPU', 'Tiempo de espera', 'Turnaround', 'Tiempo de I/O']]

    benchmark = {}  # Aquí colocaremos la info de nuestros procesos
    e = eventos.pop(0)  # Primer evento
    for t in range(0, terminacion):
        str_evento = ''  # Será el mensaje a colocar en la tabla en "Evento"
        special = False  # Determina si en esta unidad de tiempo ocurrió algo
        if cpu['PID']: benchmark[cpu['PID']][3] += 1
        for p in listos: benchmark[p][4] += 1
        for p in bloqueados: benchmark[p][6] += 1

        # Si llega algún evento en esta unidad de tiempo
        if t == e['Tiempo']:
            special = True
            accion = e['Accion']
            p_id = e['PID']
            str_evento = str_eventos.pop(0)
            if accion == 'Llega':
                listos.insert(0, p_id)
                benchmark[p_id] = [0 for x in range(7)]
                benchmark[p_id][0] = p_id
                benchmark[p_id][1] = t
            elif accion == 'Acaba':
                terminados.append(p_id)
                # Si se acaba el proceso actualmente ejecutándose
                if p_id == cpu['PID']:
                    cpu['PID'] = ''
                    cpu['entrada'] = 0
                # Si se acaba un proceso en cola de listos
                else:
                    listos.remove(p_id)
                benchmark[p_id][2] = t
            elif accion == 'startI/O':
                bloqueados.append(p_id)
                cpu['PID'] = ''
                cpu['entrada'] = 0
            elif accion == 'endI/O':
                bloqueados.remove(p_id)
                listos.insert(0, p_id)

            if len(eventos) > 0: e = eventos.pop(0)

        # Si se acaba el quantum del proceso lo regresamos a la cola de listos
        if t == cpu['entrada']+quantum:
            special = True
            listos.insert(0, cpu['PID'])
            cpu['PID'] = ''
            cpu['entrada'] = 0

        # Si el CPU está libre le metemos el último proceso de la cola de listos
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

    print(tabulate(output_table))

    # Crear el specs_table con base en los diferentes benchmarks de cada proceso
    for p in sorted(benchmark):
        benchmark[p][5] = benchmark[p][2] - benchmark[p][1]
        specs_table.append(benchmark[p])
    print(tabulate(specs_table))


# CPU Scheduling mediante PriorityNotPreemtive
def PriorityNotPreemtive(eventos):
    print('Wenas')


eventos = read_file()
if scheduling == 'RR': RoundRobin(quantum, eventos)
elif scheduling == 'prioNotPreentive': PriorityNotPreemtive(eventos)
