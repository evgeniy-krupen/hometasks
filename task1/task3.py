import configparser
import datetime
import json
import psutil
import schedule
Config = configparser.ConfigParser()
Config.read("config3.ini")
file_type = Config.get('common', 'output')
interval = Config.get('common', 'interval')

counter = 1
# function logging to TXT
def ToTxtFile():
    '''write to txt file'''
    #define variables
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    VMEMORY = psutil.virtual_memory()
    MEMORY = psutil.swap_memory()
    CPU_LOAD = psutil.cpu_percent(interval=1, percpu=True)
    DISK_IO = psutil.disk_usage('/')
    NETWORK = psutil.net_io_counters(pernic=False)
    global counter
    #write to file
    file = open("output.txt", "a")
    file.write("\n###Snapshot {0}: TimeStamp {1}\n".format(counter,timestamp))
    file.write("CPU load (%): {0}\n".format(CPU_LOAD))
    file.write("Memory usage (Mb): used {0}, free {1}\n".format((VMEMORY[4]/(1024**2)).__round__(2),(VMEMORY[5]/(1024**2)).__round__(2)))
    file.write("Swap Memory stat (Mb): total {0}, used {1}\n".format((VMEMORY[0]/(1024**2)).__round__(2),(VMEMORY[1]/(1024**2)).__round__(2)))
    file.write("Disk usage (Mb): total {0}, free {1}\n".format((DISK_IO[0]/(1024**2)).__round__(2),(DISK_IO[2]/(1024**2)).__round__(2)))
    file.write("Network stats: \n{0}\n".format(NETWORK))
    file.write("\n============================================\n")
    counter += 1
    file.close()

# function logging to Json
def ToJsonFile():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    VMEMORY = psutil.virtual_memory()
    MEMORY = psutil.swap_memory()
    CPU_LOAD = psutil.cpu_percent(interval=1, percpu=True)
    DISK_IO = psutil.disk_usage('/')
    NETWORK = psutil.net_io_counters(pernic=False)
    json_file = open("outputdata.json", "a")
    global counter
    snapshot = {
        'Timestamp': timestamp,
        'CPU_load' : CPU_LOAD,
        'Vmemory' : VMEMORY,
        'Memory' : MEMORY,
        'IO_info': DISK_IO,
        'Network_info': NETWORK
    }
    data = ['SNAPSHOT' + str(counter) + ": " + str(timestamp) + ": ", snapshot]
    json.dump(data, json_file, indent=3, sort_keys=True)
    counter += 1
    json_file.close()

# condition (type file)
if file_type == "txt":
    print('Output file type = ' + file_type + ', interval = ' + interval + ' minutes')
    schedule.every(int(interval)).minutes.do(ToTxtFile)
elif file_type == "json":
    print('Output filetype = ' + file_type + ', interval = ' + interval + ' minutes')
    schedule.every(int(interval)).seconds.do(ToJsonFile)
else:
    print("Bad filetype in config file")
    quit()
while True:
	schedule.run_pending()
