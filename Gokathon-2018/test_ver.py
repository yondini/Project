import serial

bluetoothSerial = serial.Serial("/dev/rfcomm9", baudrate=9600)
variable = 0

while 1:
    variable = (int)(bluetoothSerial.readline())
    if variable==0:
        print variable
    else:
        break

import copy
import random

departure_list = ['n1','n2','n3','n4','n5']

departure = random.choice(departure_list)

fire=departure

while fire ==departure:

    fire = random.choice(departure_list)

 

landscape = {

    'n1':   {'n2':6,'n5':3},

    'n2':   {'n1':6,'n3':3,'n4':2},

    'n3':   {'n2':3,'n5':1},

    'n4':   {'n2':2},

    'n5':   {'n1':3,'n3':1}

}

 

for acc_1,acc_2 in landscape.items():

    for acc_3 in acc_2.keys():

        if acc_3==fire:

            landscape[acc_1][acc_3]=100

 
 

routing = {}

for place in landscape.keys():

    routing[place]={'shortestDist':0, 'route': [], 'visited': 0}

 

def visitPlace(visit):

    routing[visit]['visited'] = 1

    for toGo, betweenDist in landscape[visit].items():

        toDist = routing[visit]['shortestDist'] + betweenDist

        if (routing[toGo]['shortestDist'] >= toDist) or not routing[toGo]['route']:

            routing[toGo]['shortestDist'] = toDist

            routing[toGo]['route'] = copy.deepcopy(routing[visit]['route'])

            routing[toGo]['route'].append(visit)

 

visitPlace(departure)

exit_dis=100

exit_n=''

while 1:

    minDist = max(routing.values(), key=lambda x: x['shortestDist'])['shortestDist']

    toVisit = ''

    for name, search in routing.items():

        if 0 < search['shortestDist'] <= minDist and not search['visited']:

            minDist = search['shortestDist']

            toVisit = name

    if toVisit == '':

        break

    visitPlace(toVisit)

    if toVisit=='n5' or toVisit=='n4':

        if exit_dis>minDist:

            exit_dis=minDist

            exit_n=toVisit

    #print("[" + toVisit + "]")

    #print("Dist :", minDist)

    
print('fire: ', fire) 

if departure=='n4' or departure=='n5':

    print("[", departure, "->", departure, "]")

    print("Route : ", departure)

    print("ShortestDistance : ", 0)

else:

    print("[", departure, "->", exit_n, "]")

    print("Route : ", routing[exit_n]['route'])

    print("ShortestDistance : ", routing[exit_n]['shortestDist'])
