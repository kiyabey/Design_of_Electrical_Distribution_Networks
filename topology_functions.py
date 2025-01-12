import pandapower as pp
import networkx as nx
import pandapower.topology as top
import pandapower.plotting as plot
from collections import Counter
from itertools import islice
from pandapower.plotting import simple_plotly
import math
import numpy as np
import time

net = pp.from_json("example_mv_grid.json")

mg = top.create_nxgraph(net)

lines = net.line.index
buses = net.bus.index


def n_1_safety_ll(net):
    ''' returns the list of the lines that have line loading more than 50%
    '''
    max_ll = 50
    line_loading_too_high = list()
    for m in lines:
         if net.line.loc[m , "name"] == "ring_separation_line":
             net.line.loc[m, "in_service"] = False
    for l in lines:
        if net.line.loc[l, "name"] != "ring_separation_line":
          net.line.loc[l, "in_service"] = False
          pp.runpp(net,numba=False)

          for b in lines:
              if net.line.loc[b, "in_service"] == True and net.res_line.loc[b, "loading_percent"] > max_ll:
                  if b not in line_loading_too_high:
                     line_loading_too_high.append(b)
          net.line.loc[l,"in_service"] = True

    return (line_loading_too_high)


def n_1_safety_ll_counter(net):
    ''' returns the amount of the lines that have line loading more than 50%
    '''
    max_ll = 50
    line_loading_too_high = list()
    for m in lines:
         if net.line.loc[m , "name"] == "ring_separation_line":
             net.line.loc[m, "in_service"] = False
    for l in lines:
        if net.line.loc[l, "name"] != "ring_separation_line":
          net.line.loc[l, "in_service"] = False
          pp.runpp(net,numba=False)

          for b in lines:
              if net.line.loc[b, "in_service"] == True and net.res_line.loc[b, "loading_percent"] > max_ll:
                  line_loading_too_high.append(b)
          net.line.loc[l,"in_service"] = True

    return Counter(line_loading_too_high)


def distance_between_bus(net, starting_bus, target_bus):
  ''' returns the distance between two buses
  '''
  distance = top.calc_distance_to_bus(net, starting_bus)[target_bus]

  return distance


def n_1_safety_v_min(net):
    ''' returns the list of the buses that have a lower voltage than minimum voltage
    '''
    v_min = 0.95
    voltage_too_low = list()
    for m in lines:
         if net.line.loc[m , "name"] == "ring_separation_line":
             net.line.loc[m, "in_service"] = False
    for l in lines:
        if net.line.loc[l, "in_service"] == True :
          net.line.loc[l, "in_service"] = False
          pp.runpp(net,numba=False)

          for b in buses:
              if net.res_bus.loc[b, "vm_pu"] < v_min:
                  if b not in voltage_too_low:
                     voltage_too_low.append(b)
          net.line.loc[l,"in_service"] = True

    return voltage_too_low


def n_1_safety_v_min_counter(net):
    ''' returns the amount of the buses that have a lower voltage than minimum voltage
    '''
    v_min = 0.95
    voltage_too_low = list()
    for m in lines:
         if net.line.loc[m , "name"] == "ring_separation_line":
             net.line.loc[m, "in_service"] = False
    for l in lines:
        if net.line.loc[l, "in_service"] == True :
          net.line.loc[l, "in_service"] = False
          pp.runpp(net,numba=False)

          for b in buses:
              if net.res_bus.loc[b, "vm_pu"] < v_min:
                voltage_too_low.append(b)
          net.line.loc[l,"in_service"] = True

    return Counter(voltage_too_low)


def n_1_safety_v_max(net):
    ''' returns the list of the buses that have a higher voltage than maximum voltage
    '''
    v_max = 1.05
    voltage_too_high = list()
    for m in lines:
         if net.line.loc[m , "name"] == "ring_separation_line":
             net.line.loc[m, "in_service"] = False
    for l in lines:
        if net.line.loc[l, "in_service"] == True:
          net.line.loc[l, "in_service"] = False
          pp.runpp(net,numba=False)

          for b in buses:
              if net.res_bus.loc[b, "vm_pu"] > v_max:
                  voltage_too_high.append(b)
          net.line.loc[l,"in_service"] = True

    return Counter(voltage_too_high)


def n_1_safety_v(net):
    ''' returns the list of the buses that have a voltage problem (both lower than minimum and higher than maximum voltage)
    '''
    v_max = 1.05
    v_min = 0.95
    voltage_problematic_busses = list()
    for m in lines:
      if net.line.loc[m , "name"] == "ring_separation_line":
         net.line.loc[m, "in_service"] = False
    for l in lines:
        if net.line.loc[l, "in_service"] == True :
          net.line.loc[l, "in_service"] = False
          pp.runpp(net,numba=False)

          for b in buses:
              if net.res_bus.loc[b, "vm_pu"] < v_min or net.res_bus.loc[b, "vm_pu"] > v_max:
                  if b not in voltage_problematic_busses:
                     voltage_problematic_busses.append(b)
          net.line.loc[l,"in_service"] = True

    return voltage_problematic_busses




def list_starting_buses_to_bus(net):
    ''' returns the list of the end buses of the starting ring lines
    '''
    starting_buses = list()
    for m in lines:
        if net.line.loc[m, "name"] == "starting_ring_line":
            starting_buses.append(net.line.to_bus[m])
    return starting_buses


def list_starting_buses_from_bus(net):
    ''' returns the list of the start buses of the starting ring lines
    '''
    starting_buses_from_bus = list()
    for m in lines:
        if net.line.loc[m, "name"] == "starting_ring_line":
            starting_buses_from_bus.append(net.line.from_bus[m])
    return starting_buses_from_bus


def list_starting_lines(net):
    ''' returns the list of the starting ring lines
    '''
    starting_lines = list()
    for o in lines:
        if net.line.loc[o, "name"] == "starting_ring_line":
          starting_lines.append(o)

    return starting_lines   


def complete_branches(net):
    ''' returns the branches of the grid
    '''
    branches = []
   
    n = len(list_starting_buses_from_bus(net))
    for b in range(n):
        branches.append([])
    
    before_counter = 0
    for a in range(n):
        branches[before_counter].append(list_starting_buses_from_bus(net)[before_counter])
        branches[before_counter].append(list_starting_buses_to_bus(net)[before_counter])
        before_counter += 1

    after_counter = 0
    for d in range(n):
      current_bus = branches[after_counter][1]
      current_line = list_starting_lines(net)[after_counter]
          
      while net.line.loc[current_line,"name"] != "ring_separation_line":
          for e in lines:
              if net.line.loc[e,"from_bus"] == current_bus and net.line.loc[e, "name"] == "ring_line" and net.line.loc[e, "to_bus"] not in branches[after_counter]:
                  current_bus = net.line.loc[e, "to_bus"]
                  current_line = e
                  branches[after_counter].append(current_bus)
                  break
              
              if net.line.loc[e,"to_bus"] == current_bus and net.line.loc[e, "name"] == "ring_line" and net.line.loc[e, "from_bus"] not in branches[after_counter]:
                  current_bus = net.line.loc[e, "from_bus"]
                  current_line = e
                  branches[after_counter].append(current_bus)
                  break
              
              if net.line.loc[e, "from_bus"] == current_bus and net.line.loc[e, "name"] == "ring_separation_line":
                  current_line = e
                  break
              
              if net.line.loc[e, "to_bus"] == current_bus and net.line.loc[e, "name"] == "ring_separation_line":
                  current_line = e
                  break
              
      after_counter += 1        

                  
    return branches


#2/3
def add_parallel_line_voltage(net,list):
    ''' adds a parallel line to solve the voltage problem
    '''
    all_branches = complete_branches(net)
    counter_array = np.zeros(len(list_starting_lines(net)), dtype = int)
    y = len(list)
    d = len(list_starting_lines(net))
    for m in range(y):
        for h in range(d):
            if list[m] in all_branches[h]:
                counter_array[h] += 1
                break
    
    for k in range(d):
        if counter_array[k] != 0:
            starting_bus = list_starting_buses_from_bus(net)[k]
            target_bus = all_branches[k][int(len(all_branches[k])*(2/3))]
            pp.create_line(net=net , from_bus = starting_bus, to_bus = target_bus, length_km = distance_between_bus( net, starting_bus, target_bus), 
                           std_type = "NA2XS2Y 1x240 RM/25 12/20 kV" ,name="starting_ring_line")
            for t in lines:
                if net.line.loc[t,"to_bus"] == target_bus:
                        net.line.loc[t,"in_service"] = False


#2/3
def add_parallel_line_voltage_with_type(net,list,cable_type):
    ''' adds a parallel line with a specific type to solve the voltage problem
    '''
    all_branches = complete_branches(net)
    counter_array = np.zeros(len(list_starting_lines(net)), dtype = int)
    y = len(list)
    d = len(list_starting_lines(net))
    for m in range(y):
        for h in range(d):
            if list[m] in all_branches[h]:
                counter_array[h] += 1
                break
    
    for k in range(d):
        if counter_array[k] != 0:
            starting_bus = list_starting_buses_from_bus(net)[k]
            target_bus = all_branches[k][int(len(all_branches[k])*(2/3))]
            pp.create_line(net=net , from_bus = starting_bus, to_bus = target_bus, length_km = distance_between_bus( net, starting_bus, target_bus), 
                           std_type = cable_type ,name="starting_ring_line")
            for t in lines:
                if net.line.loc[t,"to_bus"] == target_bus:
                        net.line.loc[t,"in_service"] = False


#1/2
def add_parallel_line_line_loading(net,list):
    ''' adds a parallel line to solve the loading problem
    '''
    all_branches = complete_branches(net)
    counter_array = np.zeros(len(list_starting_lines(net)), dtype = int)
    k = len(list_starting_lines(net))
    m= len(list)

    for h in range(m):
       for j in range(k):
           if net.line.loc[list[h], "from_bus"] in all_branches[j] or net.line.loc[list[h], "to_bus"] in all_branches[j]:
               counter_array[j] += 1

    for p in range(k):
        if counter_array[p] != 0:
            starting_bus = list_starting_buses_from_bus(net)[p]
            target_bus = all_branches[p][int(len(all_branches[k])*(1/2))]
            pp.create_line(net=net , from_bus = starting_bus, to_bus = target_bus, length_km = distance_between_bus( net, starting_bus, target_bus), 
                           std_type = "NA2XS2Y 1x240 RM/25 12/20 kV" ,name="starting_ring_line")
            for t in lines:
                if net.line.loc[t,"to_bus"] == target_bus:
                        net.line.loc[t,"in_service"] = False


#1/2   
def add_parallel_line_line_loading_with_type(net,list,cable_type):
    ''' adds a parallel line with a specific type to solve the loading problem
    '''
    all_branches = complete_branches(net)
    counter_array = np.zeros(len(list_starting_lines(net)), dtype = int)
    k = len(list_starting_lines(net))
    m= len(list)

    for h in range(m):
       for j in range(k):
           if net.line.loc[list[h], "from_bus"] in all_branches[j] or net.line.loc[list[h], "to_bus"] in all_branches[j]:
               counter_array[j] += 1

    for p in range(k):
        if counter_array[p] != 0:
            starting_bus = list_starting_buses_from_bus(net)[p]
            target_bus = all_branches[p][int(len(all_branches[k])*(1/2))]
            pp.create_line(net=net , from_bus = starting_bus, to_bus = target_bus, length_km = distance_between_bus( net, starting_bus, target_bus), 
                           std_type = cable_type ,name="starting_ring_line")
            for t in lines:
                if net.line.loc[t,"to_bus"] == target_bus:
                        net.line.loc[t,"in_service"] = False
    


def types_of_cables(net):
    ''' outputs the types of the cables
    '''
    cable_groups = net.line.groupby("std_type")
    for a,group in cable_groups:
      print("\n",a)


def increase_number_of_parallels_cost(net,list):
    ''' outputs the number of the new parallel lines and costs
    '''
    y = len(list)
    cost = 0.0
    counter = 0.0
    for o in range(y):
        while list[o] in n_1_safety_ll(net):
          net.line.loc[list[o], "parallel"] +=1
          counter += 1
        cost += (counter * net.line.loc[list[o],'length_km'])
    print("the number of new parallel lines :" , counter)
    
    print(cost)



def optimization_line_loading_problem(list):
    ''' Outputs whether adding a new line solves the loading problem.
    '''
    if len(list) == 0:
        print("creating a new line (1/2) works ")
    else:
        print("creating new lines(1/2) doesn't work, so only adding parallel lines is a possible solution")



def optimization_v_problem(list):
    ''' Outputs the types of the cables that solve the voltage problem
    '''
    print("Cable types that can be used to create new lines:")
    types_of_cables(net)



def n_1_complete(net):
    ''' Outputs the problematic lines before and after adding parallel lines (in terms of (n-1) contingency)
    '''
    print("problematic lines before adding parallel lines")
    print(n_1_safety_ll(net))
    increase_number_of_parallels_cost(net,n_1_safety_ll(net))
    print("problematic busses after adding parallel lines")
    print(n_1_safety_ll(net))
