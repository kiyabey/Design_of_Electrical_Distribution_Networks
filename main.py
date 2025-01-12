import pandapower as pp
import networkx as nx
import pandapower.topology as top
import pandapower.plotting 
import matplotlib.pyplot as plt
from collections import Counter
from itertools import islice
import math
import time

#load the file
print("Please enter the name of the data, so as to load it into pandapower ")
net_input = input()

try:
    net = pp.from_json(net_input)
    pandapower.plotting.simple_plot(net)
    
except:
    print("It is not a json file")

try:
    net = pp.from_pickle(net_input)  
    pandapower.plotting.simple_plot(net)
except:
    print("It is not a pickle file") 
    

try:
    net = pp.from_excel(net_input)
    pandapower.plotting.simple_plot(net)
except:
    print("It is not an excel file")  


#Ask the user, if he/she wants to check and print the powerflow results of lines and/or trafo
#Ask the user, if he/she wants to add parallel lines and/or change existing lines
print("For powerflow calculations enter 1 | to add/change lines enter 2 | to test n-1 safety enter 3")
first_input = input()

if first_input == '1':

 print("If you want to check and print the powerflow results of |the lines, enter 1 | the trafo(s), enter 2 | both the lines and the trafo(s) enter 3 ")

 number_first = input()

 #Power flow only for lines
 if number_first == '1':
   #Ask the user, if he/she wants to calculate in 1-default, 2-feed-in or 3-high-load scenario
   print("If you want to calculate in |default case enter 1 |feed-in case enter 2 | high-load case enter 3 ")
   number_second = input()

   #Default case
   if number_second == '1':
       pp.runpp(net,numba=True)
       plt.hist(net.res_line.loading_percent,bins=10)
       fig = pp.plotting.plotly.pf_res_plotly(net, on_map = True, map_style = 'dark',line_width = 6)

   #Feed-in case
   elif number_second == '2':
       net.sgen.scaling = 0.8
       net.load.scaling = 0.1
       pp.runpp(net,numba=True)
       plt.hist(net.res_line.loading_percent,bins=10)
       fig = pp.plotting.plotly.pf_res_plotly(net, on_map = True, map_style = 'dark',line_width = 6)

   #High load case
   elif number_second == '3':
       net.sgen.scaling = 0
       net.load.scaling = 0.6
       pp.runpp(net,numba=True)
       plt.hist(net.res_line.loading_percent,bins=10)
       fig = pp.plotting.plotly.pf_res_plotly(net, on_map = True, map_style = 'dark',line_width = 6)

   else: 
       print("Please enter one of those numbers: 1, 2 or 3")        



 #Power flow only for Transformers
 elif number_first ==  '2':
   #Ask the user, if he/she wants to calculate in 1-default, 2-feed-in or 3-high-load scenario
   print("If you want to calculate in |default case enter 1 |feed-in case enter 2| high-load case enter 3 ")
   number_second = input()
   
   #Default case
   if number_second == '1':
       pp.runpp(net,numba=True)
       print("The utilization of the trafo is:",net.res_trafo.loading_percent )
       print("The voltage magnitude of the lower voltage side at the trafo :", net.res_trafo.vm_lv_pu)

   #Feed-in case
   elif number_second == '2':
       net.sgen.scaling = 0.8
       pp.runpp(net,numba=True)
       print("The utilization of the trafo is:",net.res_trafo.loading_percent )
       print("The voltage magnitude of the lower voltage side at the trafo :", net.res_trafo.vm_lv_pu)

   #High load case
   elif number_second == '3':
       net.sgen.scaling = 0
       pp.runpp(net,numba=True)
       print("The utilization of the trafo is:",net.res_trafo.loading_percent )
       print("The voltage magnitude of the lower voltage side at the trafo :", net.res_trafo.vm_lv_pu)
   else: 
       print("Please enter one of those numbers: 1, 2 or 3") 

       



 #Power flow both for lines and transformers
 elif number_first ==  '3':
   #Ask the user, if he/she wants to calculate in 1-default, 2-feed-in or 3-high-load scenario
   print("If you want to calculate in |default case enter 1 |feed-in case enter 2| high-load case enter 3 ")
   number_second = input()
   
   #Default case
   if number_second == '1':
       pp.runpp(net,numba=True)
       print("The utilization of the trafo is:",net.res_trafo.loading_percent )
       print("The voltage magnitude of the lower voltage side at the trafo :", net.res_trafo.vm_lv_pu)
       plt.hist(net.res_line.loading_percent,bins=10)
       fig = pp.plotting.plotly.pf_res_plotly(net, on_map = True, map_style = 'dark',line_width = 6)

   #Feed-in case
   elif number_second == '2':
       net.sgen.scaling = 0.8
       net.load.scaling = 0.1
       pp.runpp(net,numba=True)
       print("The utilization of the trafo is:",net.res_trafo.loading_percent )
       print("The voltage magnitude of the lower voltage side at the trafo :", net.res_trafo.vm_lv_pu)
       plt.hist(net.res_line.loading_percent,bins=10)
       fig = pp.plotting.plotly.pf_res_plotly(net, on_map = True, map_style = 'dark',line_width = 6)

   #High load case
   elif number_second == '3':
       net.sgen.scaling = 0
       net.load.scaling = 0.6
       pp.runpp(net,numba=True)
       print("The utilization of the trafo is:",net.res_trafo.loading_percent )
       print("The voltage magnitude of the lower voltage side at the trafo :", net.res_trafo.vm_lv_pu)
       plt.hist(net.res_line.loading_percent,bins=10)
       fig = pp.plotting.plotly.pf_res_plotly(net, on_map = True, map_style = 'dark',line_width = 6)


   else: 
       print("Please enter one of those numbers: 1, 2 or 3") 

       

elif first_input == '2':
    print(net.line)
    print("If you want to | add parallel lines enter 1 | change existing lines enter 2 | ")

    line_input = input()
    if line_input == '1':
        
        print("Enter the line number")
        line_number = input()
        
        print("Enter the number of parallel lines you want to add")
        line_amount = input()
        
        net.line.parallel[line_number] = line_amount
        print(net.line)

    elif line_input == '2':
        print("Enter the line number")
        line_number = input()
        line_number = int(line_number)
        

        print("Enter the letter of the cable, you want to lay new") 
        print("Type A-> 0.0221 ohm per km\n Type B -> 0.0283 ohm per km\nType C -> 0.0366 ohm per km\n Type D -> 0.047 ohm per km\n")   
        print("Type E -> 0.058 ohm per km\n Type F -> 0.0601 ohm per km\nType G -> 0.0754 ohm per km\n Type H -> 0.084 ohm per km\n")  
        print("Type I -> 0.09 ohm per km\n Type J -> 0.12 ohm per km\nType K -> 0.15 ohm per km\n Type L -> 0.19 ohm per km\n")  
        print("Type M -> 0.2 ohm per km\n Type N -> 0.25 ohm per km\nType O -> 0.346 ohm per km\n Type P -> 0,387 ohm per km\n")  

        new_cable_type = input()
        
        if new_cable_type == 'A':
            net.line.r_ohm_per_km[line_number] = 0.0221
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])

        elif new_cable_type == 'B': 
            net.line.r_ohm_per_km[line_number] = 0.0283
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
            

        elif new_cable_type == 'C':
            net.line.r_ohm_per_km[line_number] = 0.0366
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'D': 
            net.line.r_ohm_per_km[line_number] = 0.047
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])

        elif new_cable_type == 'E':
            net.line.r_ohm_per_km[line_number] = 0.058
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'F': 
            net.line.r_ohm_per_km[line_number] = 0.0601
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])

        elif new_cable_type == 'G':
            net.line.r_ohm_per_km[line_number] = 0.0754
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'H': 
            net.line.r_ohm_per_km[line_number] = 0.084
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])

        elif new_cable_type == 'I':
            net.line.r_ohm_per_km[line_number] = 0.09
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'J': 
            net.line.r_ohm_per_km[line_number] = 0.12
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])

        elif new_cable_type == 'K':
            net.line.r_ohm_per_km[line_number] = 0.15
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'L': 
            net.line.r_ohm_per_km[line_number] = 0.19
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'M':
            net.line.r_ohm_per_km[line_number] = 0.2
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'N': 
            net.line.r_ohm_per_km[line_number] = 0.25
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])

        elif new_cable_type == 'O':
            net.line.r_ohm_per_km[line_number] = 0.346
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])
        
        elif new_cable_type == 'P': 
            net.line.r_ohm_per_km[line_number] = 0.387
            print("the new parameters of the line ",line_number ,"are:\n ",net.line.loc[line_number])


elif first_input == '3':
    print("for calculation | in default case enter 1 | in feed in case enter 2 | in heavy load case enter 3 ")
     
    case_input = input()
    
    # Default case
    if case_input == '1':
        
    
         net.line.in_service = True


         #Limits
         vmax =  1.05
         vmin = 0.95
         max_ll = 100

         lines = net.line.index
         most_critical_lines_vmax = list()
         most_critical_lines_vmin = list()
         most_critical_lines_ll = list()
         line_utilization = list()
         max_voltage = list()
         min_voltage = list()

         for l in lines:
             net.line.loc[l, "in_service"] = False
             pp.runpp(net,numba=False)
   
          
             if net.res_bus.vm_pu.max() > vmax:
                  most_critical_lines_vmax.append(l)
                  max_voltage.append(net.res_bus.vm_pu.max())
                
               
               
          
             if  net.res_bus.vm_pu.min() < vmin:  
                  most_critical_lines_vmin.append(l)
                  min_voltage.append(net.res_bus.vm_pu.min())
                

             if net.res_line.loading_percent.max() > max_ll:
                  most_critical_lines_ll.append(l)
                  line_utilization.append(net.res_line.loc[l, "loading_percent"])
                  
                  
                  index_max_ll = net.res_line.loading_percent.idxmax()
                  
                  
                  while net.res_line.loading_percent[index_max_ll] > max_ll:
                      net.line.parallel[index_max_ll] += 1
                      pp.runpp(net,numba=True)

                      
                      
                      

         
             net.line.loc[l, "in service"] = True   

         print("The most critical lines according to line loadings:", most_critical_lines_ll)
         print("One has to add ", net.line.parallel[index_max_ll]-1 , "new parallel cables to the line ", index_max_ll, " to secure (n-1) safety")
         print("The most critical lines according to maximum voltages:", most_critical_lines_vmax)
         print("The most critical lines according to minimum voltages:", most_critical_lines_vmin)

         

         plt.figure()   
         plt.scatter(most_critical_lines_ll, line_utilization)


         plt.figure()
         plt.scatter(most_critical_lines_vmax, max_voltage)
         plt.scatter(most_critical_lines_vmin, min_voltage)
         plt.show()

    #Feed-in case
    elif case_input == '2':
      net.line.in_service = True
      net.sgen.scaling = 0.8 
      net.load.scaling = 0.1


      #Limits
      vmax =  1.03
      vmin = 0.975
      max_ll = 100

      lines = net.line.index
      most_critical_lines_vmax = list()
      most_critical_lines_vmin = list()
      most_critical_lines_ll = list()
      line_utilization = list()
      max_voltage = list()
      min_voltage = list()

      for l in lines:
         net.line.loc[l, "in_service"] = False
         pp.runpp(net,numba=True)
   
         if net.res_bus.vm_pu.max() > vmax:
               most_critical_lines_vmax.append(l)
               max_voltage.append(net.res_bus.vm_pu.max())
               
               
          
         if  net.res_bus.vm_pu.min() < vmin:  
                most_critical_lines_vmin.append(l)
                min_voltage.append(net.res_bus.vm_pu.min())
                

         if net.res_line.loading_percent.max() > max_ll:
              most_critical_lines_ll.append(l)
              line_utilization.append(net.res_line.loc[l, "loading_percent"])

              index_max_ll = net.res_line.loading_percent.idxmax()
                  
                  
              while net.res_line.loading_percent[index_max_ll] > max_ll:
                    net.line.parallel[index_max_ll] += 1
                    pp.runpp(net,numba=True)

         net.line.loc[l, "in service"] = True   

      print("The most critical lines according to line loadings:", most_critical_lines_ll)
      print("One has to add ", net.line.parallel[index_max_ll]-1 , "new parallel cable(s) to the line ", index_max_ll, " to secure (n-1) safety")
      print("The most critical lines according to maximum voltages:", most_critical_lines_vmax)
      print("The most critical lines according to minimum voltages:", most_critical_lines_vmin)

      plt.figure()   
      plt.scatter(most_critical_lines_ll, line_utilization)


      plt.figure()
      plt.scatter(most_critical_lines_vmax, max_voltage)
      plt.scatter(most_critical_lines_vmin, min_voltage)
      plt.show()

    
    
    #Heavy-load case
    elif case_input == '3':
      net.line.in_service = True
      net.sgen.scaling = 0
      net.load.scaling = 0.6


      #Limits
      vmax =  1.03
      vmin = 0.975
      max_ll = 100

      lines = net.line.index
      most_critical_lines_ll = list()
      most_critical_lines_vmax = list()
      most_critical_lines_vmin = list()
      line_utilization = list()
      max_voltage = list()
      min_voltage = list()

      for l in lines:
         net.line.loc[l, "in_service"] = False
         pp.runpp(net,numba=True)
   
         if net.res_bus.vm_pu.max() > vmax:
               most_critical_lines_vmax.append(l)
               max_voltage.append(net.res_bus.vm_pu.max())
               
               
          
         if  net.res_bus.vm_pu.min() < vmin:  
                most_critical_lines_vmin.append(l)
                min_voltage.append(net.res_bus.vm_pu.min())
                

         if net.res_line.loading_percent.max() > max_ll:
              most_critical_lines_ll.append(l)
              line_utilization.append(net.res_line.loc[l, "loading_percent"])

              index_max_ll = net.res_line.loading_percent.idxmax()
                  
                  
              while net.res_line.loading_percent[index_max_ll] > max_ll:
                    net.line.parallel[index_max_ll] += 1
                    pp.runpp(net,numba=True)

   

         net.line.loc[l, "in service"] = True   

      print("The most critical lines according to line loadings:", most_critical_lines_ll)
      print("One has to add ", net.line.parallel[index_max_ll]-1 , "new parallel cables to the line ", index_max_ll, " to secure (n-1) safety")
      print("The most critical lines according to maximum voltages:", most_critical_lines_vmax)
      print("The most critical lines according to minimum voltages:", most_critical_lines_vmin)

      plt.figure()   
      plt.scatter(most_critical_lines_ll, line_utilization)


      plt.figure()
      plt.scatter(most_critical_lines_vmax, max_voltage)
      plt.scatter(most_critical_lines_vmin, min_voltage)
      plt.show()
   
   
       

