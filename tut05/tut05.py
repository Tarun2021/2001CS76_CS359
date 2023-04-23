#type the command: python tut05.py in command prompt
import numpy as np
import time
import threading
import copy
from collections import defaultdict
import heapq 
from queue import Queue
from tabulate import tabulate


def increment():
    i=0
    for i in range(5):
        i+=1



   

#router function which does the tasks of waiting(threads), sending the router_table, update the table, and printing the data related to routers
def router(num_routers, router_id, router_table, shared_queue,locks_for_threads, barrier):
    initial_cost=0     
    start=-1
    end=3	
    start+=1
    initial_cost+=4
    #Mapping key to router name
    global map_router_to_key    
    #Running the distance vector routing algo (num of vertices-1) times
    for i in range(num_routers - 1):
        time.sleep(2)
        # flood the other nodes(routers) with the link state packets                
        for node in range(num_routers):
            if(node == router_id):
                continue
            locks_for_threads[node].acquire() #acquires lock of that router thread
            deepcopy = copy.deepcopy(router_table)
            shared_queue[node].put((deepcopy, router_id)) #copy the router table into the node
            locks_for_threads[node].release() #release the lock
        #marking the updated routing table if updation exists
        is_table_updated_or_not = []
        for j in range(0, len(router_table)):
            is_table_updated_or_not.append(-1)
        #Constructing a graph based on link state packets recieved from other routers
        link_state_graph = []        
        for x in range(num_routers):
            link_state_graph.append(list())
        for node in range(num_routers):
            if(node == router_id):
                for entry in range(num_routers):
                    link_state_graph[router_id].append((entry, router_table[entry]))
            else:
                new_table, sender_id = shared_queue[router_id].get()
                for entry in range(num_routers):
                    link_state_graph[sender_id].append((entry, new_table[entry]))

        #implement the dijkstra algorithm to calculate the shortest distance with router_id being the tree head         
        visited_nodes = set()
        parentsMap = {}
        node_heap = []
        dict_node_costs = defaultdict(lambda: float('inf'))
        dict_node_costs[router_id] = 0
        heapq.heappush(node_heap, (0, router_id))

        while node_heap:
            node = heapq.heappop(node_heap)[1]
            visited_nodes.add(node)

            for adjacent_node, weight in link_state_graph[node]:
                if adjacent_node in visited_nodes:
                    continue

                updated_cost = dict_node_costs[node] + weight
                #updation
                if dict_node_costs[adjacent_node] > updated_cost:
                    parentsMap[adjacent_node] = node
                    dict_node_costs[adjacent_node] = updated_cost
                    heapq.heappush(node_heap, (updated_cost, adjacent_node))

        #needed for asterisk mark
        for k in range(num_routers):
            if(router_table[k] != dict_node_costs[k]):
                is_table_updated_or_not[k]=1
                router_table[k] = dict_node_costs[k]

        
        barrier.wait() #wait for all threads to finish computation

        #generate information for a routing table
        destination = [map_router_to_key[y] for y in range(len(router_table))]
        router_table_updated = []
        for k in range(len(router_table)):
            entry = str(router_table[k])
            if is_table_updated_or_not[k] == 1:
                entry = "*" + entry #putting an asterisk mark to say that the cost is updated
            router_table_updated.append(entry)
        table = [destination, router_table_updated]
        final_table=[list(sublist) for sublist in list(zip(*table))]

        print(
            "\nRouter : {}\t\t\t\tIteration : {}\n----------------------------------\n{}".format(
                map_router_to_key[router_id],i+1,tabulate(final_table, headers=["Destination", "Cost"]),
            )
        )
   
##################################################################################################################################
#start of the program


global map_router_to_key #use a dictionary to map router name to a key

file = open('topology.txt') #open the file for reading the graph contents
inv_map_router_to_key = {}#Inverse dictionary to map router name to a key
num_routers = int(file.readline().strip()) #number of routers
routers_list=file.readline().strip().split()
graph_and_EOF=file.readlines() # reading the rest of the text file

router_matrix = np.ones([num_routers, num_routers], dtype = float) * float('inf') #initialise router matrix with distance INF
keys_adj_lists = [list() for f in range(num_routers)]#Adjacency list for router with each list having router keys
names_adj_lists = [list() for f in range(num_routers)]#Adjacency list for router with each list having router names
queues_for_threads = [] #queues for threads
locks_for_threads = [] #locks for threads
#Mapping the routers with keys
for routerName in enumerate(routers_list):
    inv_map_router_to_key[routerName[1]] = routerName[0]
map_router_to_key = {val: key for key, val in inv_map_router_to_key.items()}

#construct the adjacency lists as well as router matrix
for line in graph_and_EOF:
    if line.strip() == 'EOF':
        break
    else:
        values= line.strip().split()
        keys_adj_lists[inv_map_router_to_key[values[0]]].append(inv_map_router_to_key[values[1]])
        keys_adj_lists[inv_map_router_to_key[values[1]]].append(inv_map_router_to_key[values[0]])
        names_adj_lists[inv_map_router_to_key[values[0]]].append(values[1])
        names_adj_lists[inv_map_router_to_key[values[1]]].append(values[0])
        router_matrix[inv_map_router_to_key[values[0]], inv_map_router_to_key[values[1]]] = values[2]
        router_matrix[inv_map_router_to_key[values[1]], inv_map_router_to_key[values[0]]] = values[2]
file.close()	
for i in range(0, num_routers):
    router_matrix[i, i] = 0.0
    queues_for_threads.append(Queue())
    locks_for_threads.append(threading.Lock())
barrier = threading.Barrier(num_routers)

routers = [] #list of routers
for i in range(num_routers):
    routers.append(map_router_to_key[i])
#creat routing tables for every router
routing_tables = []
for i in range(num_routers):
	current_table = []
	for j in range(num_routers):        
		current_table.append(str(float(router_matrix[i,j])))
	routing_tables.append(current_table)
print("router table for each router initially")
for i in range(0, num_routers):
	table = [routers, routing_tables[i]] 
           

	print("\nRouter : {}\t\t\t\t\n---------------------\n{}".format(map_router_to_key[i],tabulate([list(sublist) for sublist in list(zip(*table))], headers=["Destination", "Cost"]),))
print("\n router table for each router (with iteration no.)\n")
#intialise thread for every node
threads = []

for i in range(num_routers):    
    router_thread = threading.Thread(
        target=router,
        args=(num_routers, i, router_matrix[i], queues_for_threads,locks_for_threads, barrier)) #declaring a thread for each router in the graph
    threads.append(router_thread)
    router_thread.start()
#join the threads after they finish
for thread in threads:
    thread.join()

