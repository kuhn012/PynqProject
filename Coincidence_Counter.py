
from pynq import Overlay
ol = Overlay("./design_1.bit")
from pynq import GPIO
import time
import psutil
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import *
from time import sleep
import pandas as pd
from IPython.display import clear_output 
get_ipython().magic('matplotlib notebook')
plt.rcParams['animation.html'] = 'jshtml'


# Assign variable to GPIO pins to send and recieve data
enable = GPIO(GPIO.get_gpio_pin(0), 'out')
clear = GPIO(GPIO.get_gpio_pin(1), 'out')
RAM_add0 = GPIO(GPIO.get_gpio_pin(2), 'out')
RAM_add1 = GPIO(GPIO.get_gpio_pin(3), 'out')
RAM_add2 = GPIO(GPIO.get_gpio_pin(4), 'out')
RAM_add3 = GPIO(GPIO.get_gpio_pin(5), 'out')
RAM_add4 = GPIO(GPIO.get_gpio_pin(6), 'out')
RAM_WR_EN = GPIO(GPIO.get_gpio_pin(7), 'out')
Output0 = GPIO(GPIO.get_gpio_pin(8), 'in')
Output1 = GPIO(GPIO.get_gpio_pin(9), 'in')
Output2 = GPIO(GPIO.get_gpio_pin(10), 'in')
Output3 = GPIO(GPIO.get_gpio_pin(11), 'in')
Output4 = GPIO(GPIO.get_gpio_pin(12), 'in')
Output5 = GPIO(GPIO.get_gpio_pin(13), 'in')
Output6 = GPIO(GPIO.get_gpio_pin(14), 'in')
Output7 = GPIO(GPIO.get_gpio_pin(15), 'in')
Output8 = GPIO(GPIO.get_gpio_pin(16), 'in')
Output9 = GPIO(GPIO.get_gpio_pin(17), 'in')
Output10 = GPIO(GPIO.get_gpio_pin(18), 'in')
Output11 = GPIO(GPIO.get_gpio_pin(19), 'in')
Output12 = GPIO(GPIO.get_gpio_pin(20), 'in')
Output13 = GPIO(GPIO.get_gpio_pin(21), 'in')
Output14 = GPIO(GPIO.get_gpio_pin(22), 'in')
Output15 = GPIO(GPIO.get_gpio_pin(23), 'in')
Output16 = GPIO(GPIO.get_gpio_pin(24), 'in')
Output17 = GPIO(GPIO.get_gpio_pin(25), 'in')
Output18 = GPIO(GPIO.get_gpio_pin(26), 'in')
Output19 = GPIO(GPIO.get_gpio_pin(27), 'in')

# Variables needed to run graph
coincidence=[]
x_values = []
inc_rate_1 =[]
inc_rate_2 =[]
co_rate = []
RAM_ADDS = []

# Global variables used in program
coinc_12 = 0
coinc_13 = 0
coinc_14 = 0
coinc_23 = 0
coinc_24 = 0
coinc_34 = 0
coinc_123 = 0
coinc_124 = 0
coinc_134 = 0
coinc_234 = 0
coinc_1234 = 0
inc_1 = 0
inc_2 = 0
inc_3 = 0
inc_4 = 0

# Placeholders used for dataframes
variables = [[] for _ in range(19)]

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s = variables

aa = bb = cc = dd = ee = ff = gg = hh = ii = jj = kk = ll = mm = nn = oo = pp = qq = rr = ss = tt = 0

# Widgets Used for Graph
Run_Graph = widgets.Button(description='Run Graph')
Data_to_CSV = widgets.Button(description='CSV')
Graph_Output = widgets.Output()
Graph_time = widgets.IntSlider( min=15, max=150, step=1, value=30,description='Seconds to Run Graph:',style={'description_width': 'initial'})
Rate_1 = widgets.Checkbox(value=False, description='Rate of Detector 1 (Black)')
Rate_2 = widgets.Checkbox(value=False, description='Rate of Detector 2 (Blue)')
Rate_3 = widgets.Checkbox(value=False, description='Rate of Detector 3 (Green)')
Rate_4 = widgets.Checkbox(value=False, description='Rate of Detector 4 (Maroon)')
Co_1 = widgets.Checkbox(value=False, description='Rate of Coincidences (Yellow)')
Incorrect_Data = widgets.Output()

# Widgets used to export CSV
Num_Detectors = widgets.Dropdown(options=[("Detectors 1 and 2", 1), ("Detectors 1, 2 and 3", 2), ("Detectors 1, 2, 3 and 4", 3)])
Run_Exp = widgets.Button(description='Run')
Store_Data = widgets.Button(description='View Data')
Clear_Lst = widgets.Button(description='Clear All Data')
Export_Data = widgets.Button(description='Export CSV')
Output = widgets.Output()
progress = widgets.Output()
Exp_run_time = widgets.IntSlider(value= 20, min=0, max=60, continous_update=True,  description="Experiment Run Time: ",style={'description_width': 'initial'})
Angle_1 = widgets.IntText(value=0, description="Angle 1: ")
Angle_2 = widgets.IntText(value=0, description="Angle 2: ")
Angle_3 = widgets.IntText(value=0, description="Angle 3: ")
Angle_4 = widgets.IntText(value=0, description="Angle 4: ")
warning = widgets.Output()
clear_warning = widgets.Output()

# Empty dictionaries used to initialize the dataframes
# 2 Detectors
detect_12 = {}
df_12 = pd.DataFrame(detect_12)

# 3 Detectors
detect_123 = {}
df_123 = pd.DataFrame(detect_123)

# 4 Detectors
detect_1234 = {}
df_1234 = pd.DataFrame(detect_1234)

# DataFrame to show user data collected from single run of experiment, 2 detectors
detect_int_12 = {
            'Angle Detector 1': aa,
            'Angle Detector 2': bb,
            'Coincidence 12' : ee,
            'Incidence 1' : pp,
            'Incidence 2' : qq
          }
df_int_12 = pd.DataFrame(detect_int_12, index=[0])

# DataFrame to show user data collected from single run of experiment, 3 detectors
detect_int_123 = {
            'Angle Detector 1': aa,
            'Angle Detector 2': bb,
            'Angle Detector 3': cc,
            'Coincidence 12' : ee,
            'Coincidence 13' : ff,
            'Coincidence 23' : hh,
            'Coincidence 123' : kk,
            'Incidence 1' : pp,
            'Incidence 2' : qq,
            'Incidence 3' : rr
          }
df_int_123 = pd.DataFrame(detect_int_123, index=[0])

# DataFrame to show user data collected from single run of experiment, 4 detectors
detect_int_1234 = {
            'Angle Detector 1': aa,
            'Angle Detector 2': bb,
            'Angle Detector 3': cc,
            'Angle Detector 4': dd,
            'Coincidence 12' : ee,
            'Coincidence 13' : ff,
            'Coincidence 14' : gg,
            'Coincidence 23' : hh,
            'Coincidence 24' : ii,
            'Coincidence 34' : jj,
            'Coincidence 123' : kk,
            'Coincidence 124' : ll,
            'Coincidence 134' : mm,
            'Coincidence 234' : nn,
            'Coincidence 1234' : oo,
            'Incidence 1' : pp,
            'Incidence 2' : qq,
            'Incidence 3' : rr,
            'Incidence 4' : ss
          }
df_int_1234 = pd.DataFrame(detect_int_1234, index=[0])

#def Progress_Bar():
 #   Progress = widgets.IntProgress(value=0, min=0, max=(((Exp_run_time.value)*4)-1), description='Collecting Data:', style={'description_width': 'initial'})

#Progress = Progress_Bar()

# Function to clear data
def Clear_Data(btn):
    RAM_WR_EN.write(1)
    clear.write(1)
    sleep(0.01)
    RAM_WR_EN.write(0)
    clear.write(0)

# Function to Run Experiment
def Run_Experiment(btn):
    start_time = time.time()
    elapsed_time = 0
    with progress:
        clear_output()
        print('*** Collecting Data ***')
    while elapsed_time < Exp_run_time.value:
        RAM_WR_EN.write(1)
        enable.write(1)
        sleep (0.25)
        elapsed_time = time.time() - start_time  
    with progress:
        clear_output()
        print("*** Done ***")
    RAM_WR_EN.write(0)
    enable.write(0)

# Function used that returns an int from reading outputs from FPGA
def read_data_from_FPGA():
    global Output0, Output1, Output2, Output3, Output4, Output5, Output6, Output7, Output8, Output9 
    global Output10, Output11, Output12, Output13, Output14, Output15, Output16, Output17, Output18, Output19
    
    data_out = [Output0.read(), Output1.read(), Output2.read(), Output3.read(), Output4.read(), Output5.read(), 
            Output6.read(), Output7.read(), Output8.read(), Output9.read(), Output10.read(), Output11.read(), 
            Output12.read(), Output13.read(), Output14.read(), Output15.read(), Output16.read(), Output17.read(), 
            Output18.read(), Output19.read()]
    
    join_string = ''.join(str(num) for num in reversed(data_out))
    int_out = int(join_string,2)
    return int_out

# Function that stores data to variables and updates dataframe for viewing
def Store_Data_to_Variable(btn):
    global aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, coinc_12, coinc_13, coinc_14 
    global coinc_23, coinc_24, coinc_34, coinc_123, coinc_124, coinc_134, coinc_234, coinc_1234, inc_1, inc_2, inc_3, inc_4
    
    #Coincidences 12, Send address to FPGA for RAM
    set_to_ram_addresses(0, 0, 1, 0, 0)
        
    #Read outputs from RAM
    coinc_12 = read_data_from_FPGA()
        
    #Save output to global variable and update dataframe
    ee = coinc_12
    df_int_12['Coincidence 12'] = [ee]
    df_int_123['Coincidence 12'] = [ee]
    df_int_1234['Coincidence 12'] = [ee]

    #Slight delay to prevent overlapping outputs
    sleep(0.01)
    
    #Coincidences 13
    set_to_ram_addresses(1, 0, 1, 0, 0)
       
    coinc_13 = read_data_from_FPGA()
    ff = coinc_13
    df_int_123['Coincidence 13'] = [ff]
    df_int_1234['Coincidence 13'] = [ff]
        
    sleep(0.01)
    
    #Coincidences 14
    set_to_ram_addresses(0, 1, 1, 0, 0);
        
    coinc_14 = read_data_from_FPGA()
    gg = coinc_14
    df_int_1234['Coincidence 14'] = [gg]
        
    sleep(0.01)
    
    #Coincidences 23
    set_to_ram_addresses(1, 1, 1, 0, 0)
        
    coinc_23 = read_data_from_FPGA()
    hh = coinc_23
    df_int_123['Coincidence 23'] = [hh]
    df_int_1234['Coincidence 23'] = [hh]
        
    sleep(0.01)
    
    #Coincidences 24
    set_to_ram_addresses(0, 0, 0, 1, 0)
       
    coinc_24 = read_data_from_FPGA()
    ii = coinc_24
    df_int_1234['Coincidence 24'] = [ii]
        
    sleep(0.01)

    
    #Coincidences 34
    set_to_ram_addresses(1, 0, 0, 1, 0)
       
    coinc_34 = read_data_from_FPGA()
    jj = coinc_34
    df_int_1234['Coincidence 34'] = [jj]
        
    sleep(0.01)
    
    #Coincidences 123
    set_to_ram_addresses(0, 1, 0, 1, 0)
        
    coinc_123 = read_data_from_FPGA()
    kk = coinc_123
    df_int_123['Coincidence 123'] = [kk]
    df_int_1234['Coincidence 123'] = [kk]
        
    sleep(0.01)
    
    #Coincidences 124
    set_to_ram_addresses(1, 1, 0, 1, 0)
        
    coinc_124 = read_data_from_FPGA()
    ll = coinc_124
    df_int_1234['Coincidence 124'] = [ll]
        
    sleep(0.01)
    
    #Coincidences 134
    set_to_ram_addresses(0, 0, 1, 1, 0)
        
    coinc_134 = read_data_from_FPGA()
    mm = coinc_134
    df_int_1234['Coincidence 134'] = [mm]
        
    sleep(0.01)
    
    #Coincidences 234
    set_to_ram_addresses(1, 0, 1, 1, 0)
        
    coinc_234 = read_data_from_FPGA()
    nn = coinc_234
    df_int_1234['Coincidence 234'] = [nn]
        
    sleep(0.01)
    
    #Coincidences 1234
    set_to_ram_addresses(0, 1, 1, 1, 0)
        
    coinc_1234 = read_data_from_FPGA()
    oo = coinc_1234
    df_int_1234['Coincidence 1234'] = [oo]
        
    sleep(0.01)
    
    #Total Incidence 1
    set_to_ram_addresses(1, 1, 1, 1, 0)
       
    inc_1 = read_data_from_FPGA()
    pp = inc_1
    df_int_12['Incidence 1'] = [pp]
    df_int_123['Incidence 1'] = [pp]
    df_int_1234['Incidence 1'] = [pp]
        
    sleep(0.01)
    
    #Total Incidence 2
    set_to_ram_addresses(0, 0, 0, 0, 1)
        
    inc_2 = read_data_from_FPGA()
    qq = inc_2
    df_int_12['Incidence 2'] = [qq]
    df_int_123['Incidence 2'] = [qq]
    df_int_1234['Incidence 2'] = [qq]
        
    sleep(0.01)
    
    #Total Incidence 3
    set_to_ram_addresses(1, 0, 0, 0, 1)
        
    inc_3 = read_data_from_FPGA()
    rr = inc_3
    df_int_123['Incidence 3'] = [rr]
    df_int_1234['Incidence 3'] = [rr]
        
    sleep(0.01)
    
    #Total Incidence 4
    set_to_ram_addresses(0, 1, 0, 0, 1)
        
    inc_4 = read_data_from_FPGA()
    ss = inc_4
    df_int_1234['Incidence 4'] = [ss]

    #Update Angle of Detectors
    aa = Angle_1.value
    bb = Angle_2.value
    cc = Angle_3.value
    dd = Angle_4.value
    df_int_12['Angle Detector 1'] = [aa]
    df_int_12['Angle Detector 2'] = [bb]
    df_int_123['Angle Detector 1'] = [aa]
    df_int_123['Angle Detector 2'] = [bb]
    df_int_123['Angle Detector 3'] = [cc]
    df_int_1234['Angle Detector 1'] = [aa]
    df_int_1234['Angle Detector 2'] = [bb]
    df_int_1234['Angle Detector 3'] = [cc]
    df_int_1234['Angle Detector 4'] = [dd]
        
# Function to view Dataframe/Row of CSV
def View_Extracted_Data(btn):
    with Output:
        clear_output()
        if Num_Detectors.value == 1:
            print(df_int_12) 
        elif Num_Detectors.value == 2:
            print(df_int_123)
        else:
            print(df_int_1234)

# Button to Extract Data and View
Store_Data.on_click(View_Extracted_Data)

# Function that creates a list of extracted data
def Append_Extracted_Data(btn):
    global a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, coinc_12, coinc_13, coinc_14, coinc_23 
    global coinc_24, coinc_34, coinc_123, coinc_124, coinc_134, coinc_234, coinc_1234, inc_1, inc_2, inc_3, inc_4

    a.append(Angle_1.value)
    b.append(Angle_2.value)
    c.append(Angle_3.value)
    d.append(Angle_4.value)
    e.append(coinc_12)
    f.append(coinc_13)
    g.append(coinc_14)
    h.append(coinc_23)
    i.append(coinc_24)
    j.append(coinc_34)
    k.append(coinc_123)
    l.append(coinc_124)
    m.append(coinc_134)
    n.append(coinc_234)
    o.append(coinc_1234)
    p.append(inc_1)
    q.append(inc_2)
    r.append(inc_3)
    s.append(inc_4)
        
# Function that saves the appended lists onto the dataframes
def Save_Extracted_Data(btn):
    global a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s
    global df_12, df_123, df_1234
    
    detect_12 = {
            'Angle Detector 1': a,
            'Angle Detector 2': b,
            'Coincidence 12' : e,
            'Incidence 1' : p,
            'Incidence 2' : q
          }
    
    detect_123 = {
            'Angle Detector 1': a,
            'Angle Detector 2': b,
            'Angle Detector 3': c,
            'Coincidence 12' : e,
            'Coincidence 13' : f,
            'Coincidence 23' : h,
            'Coincidence 123' : k,
            'Incidence 1' : p,
            'Incidence 2' : q,
            'Incidence 3' : r
          }
    
    detect_1234 = {
            'Angle Detector 1': a,
            'Angle Detector 2': b,
            'Angle Detector 3': c,
            'Angle Detector 4': d,
            'Coincidence 12' : e,
            'Coincidence 13' : f,
            'Coincidence 14' : g,
            'Coincidence 23' : h,
            'Coincidence 24' : i,
            'Coincidence 34' : j,
            'Coincidence 123' : k,
            'Coincidence 124' : l,
            'Coincidence 134' : m,
            'Coincidence 234' : n,
            'Coincidence 1234' : o,
            'Incidence 1' : p,
            'Incidence 2' : q,
            'Incidence 3' : r,
            'Incidence 4' : s
          }
    
    df_12 = pd.DataFrame(detect_12)
    df_123 = pd.DataFrame(detect_123)
    df_1234 = pd.DataFrame(detect_1234)

# Function that Exports CSV
def Export_CSV(btn):
    if Num_Detectors.value == 1:
        df_12.to_csv('CSUSM_Physics.csv')
    elif Num_Detectors.value == 2:
        df_123.to_csv('CSUSM_Physics.csv')
    else:
        df_1234.to_csv('CSUSM_Physics.csv')

# Button to Save Data and Export CSV
Export_Data.on_click(Save_Extracted_Data)
Export_Data.on_click(Export_CSV)

#Function to Clear the data
def Clear_List(btn):
    global a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s
    global aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss
    global df_12, df_123, df_1234
    
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s = [[] for i in range(19)]
    aa = bb = cc = dd = ee = ff = gg = hh = ii = jj = kk = ll = mm = nn = oo = pp = qq = rr = ss = 0
    
    detect_12 = {
            'Angle Detector 1': [],
            'Angle Detector 2': [],
            'Coincidence 12' : [],
            'Incidence 1' : [],
            'Incidence 2' : []
          }
    df_12 = pd.DataFrame(detect_12)
    
    detect_123 = {
            'Angle Detector 1': [],
            'Angle Detector 2': [],
            'Angle Detector 3': [],
            'Coincidence 12' : [],
            'Coincidence 13' : [],
            'Coincidence 23' : [],
            'Coincidence 123' : [],
            'Incidence 1' : [],
            'Incidence 2' : [],
            'Incidence 3' : []
          }
    df_123 = pd.DataFrame(detect_123)
    
    detect_1234 = {
            'Angle Detector 1': [],
            'Angle Detector 2': [],
            'Angle Detector 3': [],
            'Angle Detector 4': [],
            'Coincidence 12' : [],
            'Coincidence 13' : [],
            'Coincidence 14' : [],
            'Coincidence 23' : [],
            'Coincidence 24' : [],
            'Coincidence 34' : [],
            'Coincidence 123' : [],
            'Coincidence 124' : [],
            'Coincidence 134' : [],
            'Coincidence 234' : [],
            'Coincidence 1234' : [],
            'Incidence 1' : [],
            'Incidence 2' : [],
            'Incidence 3' : [],
            'Incidence 4' : []
          }
    df_1234 = pd.DataFrame(detect_1234)
    
#Button to Clear Data, Run Experiment, Store data  
Run_Exp.on_click(lambda btn: [Clear_Data(btn), Run_Experiment(btn) , Store_Data_to_Variable(btn), Append_Extracted_Data(btn)])
    
# Button to Clear Data
Clear_Lst.on_click(Clear_List)

#set addresses
def set_to_ram_addresses(add1, add2, add3, add4, add5):
    RAM_add0.write(add1)
    RAM_add1.write(add2)
    RAM_add2.write(add3)
    RAM_add3.write(add4)
    RAM_add4.write(add5)
    
#function to turn on enable    
def enable_set(en, wr, clc):
    enable.write(en)
    RAM_WR_EN.write(wr)
    clear.write(clc)
    
# Function that enables Circuit and runs graph for selected time seconds
def Run_RTG(btn):
    #global Graph_time.value
    #Clear the axis, create a start time, and clear list
    ax.clear() 
    start_time = time.time()
    elapsed_time = 0
    Out_4 = 0
    i = 0
    x_values, inc_rate_1, inc_rate_2, co_rate = [], [], [], []
    clear.write(1)
    
    # Conditional to display graph based off data checked
    if (Rate_1.value == True) and (Rate_2.value == False) and (Rate_3.value == False) and (Rate_4.value == False) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        #While time is less than 60 seconds, graph will be updated
        while elapsed_time < Graph_time.value:
            
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ##set the title and labels
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.05)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == True) and (Rate_3.value == False) and (Rate_4.value == False) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
            
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)       

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            line1 = ax.plot(x_values, inc_rate_2, color='b', label='Rate 2')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.05)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == False) and (Rate_3.value == True) and (Rate_4.value == False) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)       

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_2, color='g', label='Rate 3')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.05)
            i += 0.65
            elapsed_time = time.time() - start_time
    elif (Rate_1.value == False) and (Rate_2.value == False) and (Rate_3.value == False) and (Rate_4.value == True) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)       

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.set_title("Coincidences/ Incidence rate")
            ax.legend( loc='lower right')
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.05)
            i += 0.65
            elapsed_time = time.time() - start_time
    elif (Rate_1.value == True) and (Rate_2.value == True) and (Rate_3.value == False) and (Rate_4.value == False) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
            
            RAM_add4.write(0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ax.plot(x_values, inc_rate_2, color='b', label='Rate 2')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == True) and (Rate_2.value == True) and (Rate_3.value == False) and (Rate_4.value == False) and (Co_1.value == True):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 1)
    
            Out_3 = read_data_from_FPGA()
            co_rate.append(Out_3)
            
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)
                co_rate.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ax.plot(x_values, inc_rate_2, color='b', label='Rate 2')
            ax.plot(x_values, co_rate, color='y', label='Coincidence')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == True) and (Rate_2.value == False) and (Rate_3.value == True) and (Rate_4.value == False) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ax.plot(x_values, inc_rate_2, color='g', label='Rate 3')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == True) and (Rate_2.value == False) and (Rate_3.value == True) and (Rate_4.value == False) and (Co_1.value == True):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            sleep(.001)
        
            set_to_ram_addresses(0, 0, 1, 0, 1)
    
            Out_3 = read_data_from_FPGA()
            co_rate.append(Out_3)
            
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)
                co_rate.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ax.plot(x_values, inc_rate_2, color='g', label='Rate 3')
            ax.plot(x_values, co_rate, color='y', label='Coincidence')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == True) and (Rate_2.value == False) and (Rate_3.value == False) and (Rate_4.value == True) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == True) and (Rate_2.value == False) and (Rate_3.value == False) and (Rate_4.value == True) and (Co_1.value == True):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            sleep(.001)
        
            set_to_ram_addresses(1, 0, 1, 0, 1)
    
            Out_3 = read_data_from_FPGA()
            co_rate.append(Out_3)
            
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)
                co_rate.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='k', label='Rate 1')
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.plot(x_values, co_rate, color='y', label='Coincidence')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == True) and (Rate_3.value == True) and (Rate_4.value == False) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
            
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='b', label='Rate 2')
            ax.plot(x_values, inc_rate_2, color='g', label='Rate 3')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == True) and (Rate_3.value == True) and (Rate_4.value == False) and (Co_1.value == True):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            sleep(.001)
        
            set_to_ram_addresses(0, 1, 1, 0, 1)
    
            Out_3 = read_data_from_FPGA()
            co_rate.append(Out_3)
            
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)
                co_rate.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='b', label='Rate 2')
            ax.plot(x_values, inc_rate_2, color='g', label='Rate 3')
            ax.plot(x_values, co_rate, color='y', label='Coincidence')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == True) and (Rate_3.value == False) and (Rate_4.value == True) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
            
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='b', label='Rate 2')
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == True) and (Rate_3.value == False) and (Rate_4.value == True) and (Co_1.value == True):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(1, 0, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            sleep(.001)
        
            set_to_ram_addresses(0, 0, 0, 1, 1)
    
            Out_3 = read_data_from_FPGA()
            co_rate.append(Out_3)
            
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)
                co_rate.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='b', label='Rate 2')
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.plot(x_values, co_rate, color='y', label='Coincidence')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == False) and (Rate_3.value == True) and (Rate_4.value == True) and (Co_1.value == False):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='g', label='Rate 3')
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
            
    elif (Rate_1.value == False) and (Rate_2.value == False) and (Rate_3.value == True) and (Rate_4.value == True) and (Co_1.value == True):
        with Incorrect_Data:
            clear_output()
        while elapsed_time < Graph_time.value:
            x_values.append(i)

            enable_set(1, 1, 0)
        
            set_to_ram_addresses(0, 1, 0, 0, 0)
    
            Out_1 = read_data_from_FPGA()
            inc_rate_1.append(Out_1)
        
            sleep(.001)
        
            set_to_ram_addresses(1, 1, 0, 0, 0)
    
            Out_2 = read_data_from_FPGA()
            inc_rate_2.append(Out_2)

            sleep(.001)
        
            set_to_ram_addresses(1, 0, 0, 1, 1)
    
            Out_3 = read_data_from_FPGA()
            co_rate.append(Out_3)
            
            if len(x_values) > 10:
                x_values.pop(0)  # Remove the oldest data point
                inc_rate_1.pop(0)
                inc_rate_2.pop(0)
                co_rate.pop(0)

            ax.clear()  # Clear the previous plot
            ax.plot(x_values, inc_rate_1, color='g', label='Rate 3')
            ax.plot(x_values, inc_rate_2, color='m', label='Rate 4')
            ax.plot(x_values, co_rate, color='y', label='Coincidence')
            ax.legend( loc='lower right')
            ax.set_title("Coincidences/ Incidence rate")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
            fig.canvas.draw()

            sleep(0.001)
            i += 0.65
            elapsed_time = time.time() - start_time
    else:
        ax.clear()  # Clear the previous plot
        fig.canvas.draw()
        with Incorrect_Data:
            clear_output()
            print('*** Please Select Valid Data ***')

    # Disable circuit
    enable.write(0)
    RAM_WR_EN.write(0)
    
# Button to Run Graph
Run_Graph.on_click(Run_RTG)

#display graph
##create a figure and subplot
fig = plt.figure()
ax = fig.add_subplot(111)
##set the title and labels
ax.set_title("Coincidences/ Incidence rate")
ax.set_xlabel("Time (sec)")
ax.set_ylabel("Count")
ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

#Printed Warnings
with clear_warning:
    print("*** Clicking on this button will clear all data collected up to this point. Export and save CSV if needed ***")
with warning:
    print("***** Warning! This will overwrite previous CSV file. Save CSV file if needed *****")

# Format Widgets
Run_widgets = [ 
    widgets.VBox([Num_Detectors, Exp_run_time, Angle_1, Angle_2, Angle_3, Angle_4, Run_Exp, progress]), 
    widgets.VBox([Store_Data, Output]),
    widgets.VBox([Export_Data, warning ]),
    widgets.VBox([Clear_Lst,clear_warning])
              ]

graph_widgets = widgets.VBox([Run_Graph, Graph_time, Rate_1, Rate_2, Rate_3, Rate_4, Co_1, Incorrect_Data])

data_widgets = widgets.Accordion(children=Run_widgets)
data_widgets.set_title(0, 'Experiment Parameters')
data_widgets.set_title(1, 'View Data')
data_widgets.set_title(2, 'Export CSV')
data_widgets.set_title(3, 'Clear Data')

tab = widgets.Tab()
tab.children = [graph_widgets, data_widgets]
tab.set_title(0, 'Align Detectors')
tab.set_title(1, 'Run Experiment')

display(tab)

