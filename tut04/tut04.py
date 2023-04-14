
from collections import defaultdict
import threading
import time
INF = float('inf')
#calling router in the form of a thread
class Router_instance(threading.Thread):
    def __init__(self, router, router_links):
        threading.Thread.__init__(self)
        self.router = router
        #create dictionary of the router's neighbours
        self.routers_neighbors = {router_link[0]: int(router_link[1]) for router_link in router_links}
        #make a table for router; it contains information of shortest cost of going to another router, along with the hop sequence in which the other router could be reached in the shortest cost
        self.routing_table = {}
        for router in routers_list:
            if router == self.router:
                self.routing_table[router] = (0, [router])
            elif router in self.routers_neighbors:
                self.routing_table[router] = (self.routers_neighbors[router], [router])#initialise with the cost of the edge between the routers
            else:
                self.routing_table[router] = (INF, [])#else if not a neighbour, set cost to infinity
        self.updated_or_not = defaultdict(lambda: -1)#acknowledge that the cost is updated(for asterisk mark)
        

    def run(self):
        #note that the output would go on printing in an infinite loop
        while True:            
            time.sleep(0.5)
            for neighbor in self.routers_neighbors:
                        router_queue[neighbor].append((self.router, self.routing_table))#share the routing table to its neighbors 
            time.sleep(1)
            self.updated_or_not = defaultdict(lambda: -1)#default value is -1 for the key
            #to update the routing table of the router previously shared to its neighbors; the routing table entries are updated using the Bellman Ford equation     
            while router_queue[self.router]:
               router_queue_element=router_queue[self.router].pop(0)
               sender=router_queue_element[0]
               shared_routing_table=router_queue_element[1]       
               #using Bellman Ford equation for updating table entries     
               for dest, (cost_for_going, hop) in shared_routing_table.items():
                   if cost_for_going != INF:
                         if self.routing_table[dest][0] == INF or self.routing_table[dest][0]>self.routers_neighbors[sender] + cost_for_going:
                             self.routing_table[dest] = (self.routers_neighbors[sender] + cost_for_going, [sender]+(hop))# update with the shortest possible cost; along with that, update the hop sequence
                             self.updated_or_not[dest] = 1   #acknowledge that the cost is updated(for asterisk mark)                
                   else:
                       continue    
            time.sleep(0.5)

# for printing the router table
def print_routing_tables(router_threads):
    num_of_iterations=0
    while True:
        print("Iteration: {}".format(num_of_iterations),"       ")
        num_of_iterations += 1        
        for router in router_threads:
            print("Router of which routing table is being printed: {}".format(router.router))
            print("the routing table:", end="\t")            
            for destination, (cost_for_going, hop_sequence) in router.routing_table.items():
                print('\n')
                print(f"for destination: {destination} ; edge weight : {cost_for_going}{'*' if router.updated_or_not[destination]==1 else''} \t hop_order: {hop_sequence}",end="\t",)
            print('\n')                       
        time.sleep(2)
# starting of the program; read the input from the file and store it in a graph, which has the routers and the weights of the edges with that router
graph = defaultdict(list)
#note that the text file from whcih it is read is topology.txt
file1=open('topology.txt')
num_routers=int(file1.readline().strip())
routers_list=file1.readline().strip().split()
for line in file1:
    if line.strip()=='EOF':
        break
    values=line.strip().split()
    first_router=values[0]
    second_router=values[1]
    edge_wt=values[2]
    graph[first_router].append((second_router,edge_wt))
    graph[second_router].append((first_router,edge_wt))    
router_queue={router:[] for router in routers_list} 
#store the router threads
router_threads = []
for router in routers_list:
    router_connections = graph[router]
    router_thread = Router_instance(router, router_connections)
    router_threads.append(router_thread)#append the router threads
    router_thread.start()#start the router thread
# running the printer thread
printer_thread = threading.Thread(target=print_routing_tables, args=(router_threads,))
printer_thread.start()
#for joining the router threads
for router_thread in router_threads:
    router_thread.join()
# joining the printer threads
printer_thread.join()







