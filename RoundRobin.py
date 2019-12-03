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
            if len(next_line.split()) != 3 and len(next_line.split()) != 5:
                next_line = f.readline().strip()
                continue

            prio = 0
            if len(next_line.split()) > 3:
                prio = int(next_line.split()[4])

            tiempo = int(next_line.split()[0])
            accion = next_line.split()[1]
            p_id = int(next_line.split()[2])

            # Verificaciones, casos en los que se ignora la línea
            if tiempo < 0:
                next_line = f.readline().strip()
                continue
            if accion != 'Llega' and accion != 'Acaba' and accion != 'startI/O' and accion != 'endI/O':
                next_line = f.readline().strip()
                continue
            if p_id < 0:
                next_line = f.readline().strip()
                continue
            if prio < 0:
                next_line = f.readline().strip()
                continue

            eventos.append({
                'Tiempo': tiempo,
                'Accion': accion,
                'PID': p_id,
                'Prio': prio
            })
            str_eventos.append(next_line)
            next_line = f.readline().strip()

        str_eventos.append(next_line)
        terminacion = int(next_line.split()[0])
    return eventos


def priority_insert(prioridades, listos, proceso):
    og_len = len(listos)
    for i in range(0, len(listos)):
        if prioridades[proceso] >= prioridades[listos[i]]:
            listos.insert(i, proceso)
            break
    if og_len == len(listos):
        listos.append(proceso)
    return listos


# CPU Scheduling mediante RoundRobin
def RoundRobin(quantum, eventos):
    listos = []  # Procesos en la cola de listos
    bloqueados = []  # Procesos bloqueados por algún I/O
    terminados = []  # Procesos finalizados por el CPU

    # Proceso actual que corre el CPU y cuándo comenzó
    cpu = {'PID': '', 'entrada': 0}
    output_table = []
    output_headers = ['Evento', 'Cola de listos',
                      'CPU', 'Bloqueados', 'Terminados']
    specs_table = []
    specs_headers = ['Proceso', 'Tiempo de llegada', 'Tiempo de terminación',
                     'Tiempo de CPU', 'Tiempo de espera', 'Turnaround', 'Tiempo de I/O']

    benchmark = {}  # Aquí colocaremos la info de nuestros procesos
    e = eventos.pop(0)  # Primer evento
    for t in range(0, terminacion):
        str_evento = ''  # Será el mensaje a colocar en la tabla en "Evento"
        special = False  # Determina si en esta unidad de tiempo ocurrió algo
        if cpu['PID']:
            benchmark[cpu['PID']][3] += 1
        for p in listos:
            benchmark[p][4] += 1
        for p in bloqueados:
            benchmark[p][6] += 1

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
                print('Proceso ' + str(p_id) + ' creado')
                print(tabulate([[
                    str_evento,
                    ','.join(map(str, listos)),
                    cpu['PID'],
                    ','.join(map(str, bloqueados)),
                    ','.join(map(str, terminados))
                ]], headers=output_headers, tablefmt="psql"))
                print()

            elif accion == 'Acaba':
                # Verificar que el proceso no estuviera ya terminado
                if terminados.count(p_id) == 0:
                    terminados.append(p_id)
                    # Si se acaba el proceso actualmente ejecutándose
                    if p_id == cpu['PID']:
                        cpu['PID'] = ''
                        cpu['entrada'] = 0
                    # Si se acaba un proceso en cola de listos
                    else:
                        listos.remove(p_id)
                    benchmark[p_id][2] = t
                    print('Proceso ' + str(p_id) + ' terminado')
                    print(tabulate([[
                        str_evento,
                        ','.join(map(str, listos)),
                        cpu['PID'],
                        ','.join(map(str, bloqueados)),
                        ','.join(map(str, terminados))
                    ]], headers=output_headers, tablefmt="psql"))
                    print()
                else:
                    special = False

            elif accion == 'startI/O':
                # Verificar si no se le hace un I/O a un proceso terminado
                if terminados.count(p_id) == 0:
                    # Caso de un proceso en CPU entrando a I/O
                    if p_id == cpu['PID']:
                        cpu['PID'] = ''
                        cpu['entrada'] = 0
                    # Caso de un proceso en cola de listos entrando a I/O
                    elif listos.count(p_id) > 0:
                        listos.remove(p_id)
                    bloqueados.append(p_id)
                    print('Proceso ' + str(p_id) + ' entra en I/O')
                    print(tabulate([[
                        str_evento,
                        ','.join(map(str, listos)),
                        cpu['PID'],
                        ','.join(map(str, bloqueados)),
                        ','.join(map(str, terminados))
                    ]], headers=output_headers, tablefmt="psql"))
                    print()
                else:
                    special = False

            elif accion == 'endI/O':
                # Verificar si el proceso ya estaba en I/O
                if bloqueados.count(p_id) > 0:
                    bloqueados.remove(p_id)
                    listos.insert(0, p_id)
                    print('Proceso ' + str(p_id) + ' sale de I/O')
                    print(tabulate([[
                        str_evento,
                        ','.join(map(str, listos)),
                        cpu['PID'],
                        ','.join(map(str, bloqueados)),
                        ','.join(map(str, terminados))
                    ]], headers=output_headers, tablefmt="psql"))
                    print()
                else:
                    special = False

            if len(eventos) > 0:
                e = eventos.pop(0)

        # Si se acaba el quantum del proceso lo regresamos a la cola de listos
        if t == cpu['entrada']+quantum:
            special = True
            listos.insert(0, cpu['PID'])
            cpu['PID'] = ''
            cpu['entrada'] = 0

        # Si el CPU está libre le metemos el último proceso de la cola de listos
        if cpu['PID'] == '' and listos:
            special = True
            if str_evento == '':
                str_evento = str(t) + ' quantum'
                print(str_evento)
                print(tabulate([[
                    str_evento,
                    ','.join(map(str, listos)),
                    cpu['PID'],
                    ','.join(map(str, bloqueados)),
                    ','.join(map(str, terminados))
                ]], headers=output_headers, tablefmt="psql"))
                print()
            cpu['PID'] = listos.pop()
            cpu['entrada'] = t

        if special:
            row = [
                str_evento,
                ','.join(map(str, listos)),
                cpu['PID'],
                ','.join(map(str, bloqueados)),
                ','.join(map(str, terminados))
            ]
            output_table.append(row)

    print(tabulate(output_table, headers=output_headers, tablefmt="psql"))

    # Crear el specs_table con base en los diferentes benchmarks de cada proceso
    total_turnaround = 0
    total_espera = 0
    for p in sorted(benchmark):
        turnaround = benchmark[p][2] - benchmark[p][1]
        benchmark[p][5] = turnaround
        total_turnaround += turnaround
        total_espera += benchmark[p][4]
        specs_table.append(benchmark[p])
    print(tabulate(specs_table, headers=specs_headers, tablefmt="psql"))

    print('Turnaround promedio:', end=' ')
    print("%0.4f" % (total_turnaround/len(benchmark),))
    print('Tiempo espera promedio:', end=' ')
    print("%0.4f" % (total_espera/len(benchmark),))


# CPU Scheduling mediante PriorityNotPreemtive
def PriorityNotPreemtive(eventos):
    listos = []  # Procesos en la cola de listos
    bloqueados = []  # Procesos bloqueados por algún I/O
    terminados = []  # Procesos finalizados por el CPU
    # Proceso actual que corre el CPU y cuándo comenzó
    cpu = {'PID': '', 'entrada': 0}
    prioridades = {}  # Diccionario de las prioridades de cada proceso
    output_table = []
    output_headers = ['Evento', 'Cola de listos',
                      'CPU', 'Bloqueados', 'Terminados']
    specs_table = []
    specs_headers = ['Proceso', 'Tiempo de llegada', 'Tiempo de terminación',
                     'Tiempo de CPU', 'Tiempo de espera', 'Turnaround', 'Tiempo de I/O']

    benchmark = {}  # Aquí colocaremos la info de nuestros procesos
    last_t = 0  # Aquí guardamos el tiempo del evento anterior

    for e in eventos:
        t = e['Tiempo']  # El tiempo de este evento
        accion = e['Accion']  # La acción ocurrida que luego se comparará
        p_id = e['PID']  # ID del proceso al que se le aplica la acción
        prio = e['Prio']  # Priodidad del proceso acontecido
        if cpu['PID']:
            benchmark[cpu['PID']][3] += t - last_t
        for p in listos:
            benchmark[p][4] += t - last_t
        for p in bloqueados:
            benchmark[p][6] += t - last_t

        if accion == 'Llega':
            # Registramos la prioridad del nuevo proceso
            prioridades[p_id] = prio
            listos = priority_insert(prioridades, listos, p_id)
            benchmark[p_id] = [0 for x in range(7)]
            benchmark[p_id][0] = p_id
            benchmark[p_id][1] = t
            print('Proceso ' + str(p_id) + ' creado')

        elif accion == 'Acaba':
            # Revisar que el proceso no estuviera ya terminado
            if terminados.count(p_id) == 0:
                terminados.append(p_id)
                # Si se acaba el proceso actualmente ejecutándose
                if p_id == cpu['PID']:
                    cpu['PID'] = ''
                    cpu['entrada'] = 0
                # Si se acaba un proceso en cola de listos
                elif listos.count(p_id) > 0:
                    listos.remove(p_id)
                benchmark[p_id][2] = t
                print('Proceso ' + str(p_id) + ' terminado')
            else:
                last_t = t
                str_eventos.pop(0)
                continue

        elif accion == 'startI/O':
            # Verificar si no se le hace un I/O a un proceso terminado
            if terminados.count(p_id) == 0:
                # Caso de un proceso en CPU entrando a I/O
                if p_id == cpu['PID']:
                    cpu['PID'] = ''
                    cpu['entrada'] = 0
                # Caso de un proceso en cola de listos entrando a I/O
                elif listos.count(p_id) > 0:
                    listos.remove(p_id)
                bloqueados.append(p_id)
                print('Proceso ' + str(p_id) + ' entra en I/O')
            else:
                last_t = t
                str_eventos.pop(0)
                continue

        elif accion == 'endI/O':
            # Verificar si el proceso ya estaba en I/O
            if bloqueados.count(p_id) > 0:
                listos = priority_insert(prioridades, listos, p_id)
                bloqueados.remove(p_id)
                print('Proceso ' + str(p_id) + ' sale de I/O')
            else:
                last_t = t
                str_eventos.pop(0)
                continue

        if cpu['PID'] == '' and listos:
            cpu['PID'] = listos.pop()
            cpu['entrada'] = t

        last_t = t
        row = [
            str_eventos.pop(0),
            ','.join(map(str, listos)),
            cpu['PID'],
            ','.join(map(str, bloqueados)),
            ','.join(map(str, terminados))
        ]
        print(tabulate([row], headers=output_headers, tablefmt="psql"))
        print()
        output_table.append(row)

    print(tabulate(output_table, headers=output_headers, tablefmt="psql"))

    # Crear el specs_table con base en los diferentes benchmarks de cada proceso
    total_turnaround = 0
    total_espera = 0
    for p in sorted(benchmark):
        turnaround = benchmark[p][2] - benchmark[p][1]
        benchmark[p][5] = turnaround
        total_turnaround += turnaround
        total_espera += benchmark[p][4]
        specs_table.append(benchmark[p])
    print(tabulate(specs_table, headers=specs_headers, tablefmt="psql"))

    print('Turnaround promedio:', end=' ')
    print("%0.4f" % (total_turnaround/len(benchmark),))
    print('Tiempo espera promedio:', end=' ')
    print("%0.4f" % (total_espera/len(benchmark),))


eventos = read_file()
if scheduling == 'RR':
    RoundRobin(quantum, eventos)
elif scheduling == 'prioNonPreemptive':
    PriorityNotPreemtive(eventos)
