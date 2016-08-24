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
def totxtfile():
    """write to txt file"""
    # define variables
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    vmemory = psutil.virtual_memory()
    memory = psutil.swap_memory()
    cpu_load = psutil.cpu_percent(interval=1, percpu=True)
    disk_io = psutil.disk_usage('/')
    network = psutil.net_io_counters(pernic=False)
    global counter
    # write to file
    file = open("output.txt", "a")
    file.write("\n###Snapshot {0}: TimeStamp {1}\n".format(counter, timestamp))
    file.write("CPU load (%): {0}\n".format(cpu_load))
    file.write("Memory usage (Mb): used {0}, free {1}\n".format((vmemory[4] / (1024 ** 2)).__round__(2),
                                                                (vmemory[5] / (1024 ** 2)).__round__(2)))
    file.write("Swap Memory stat (Mb): total {0}, used {1}\n".format((memory[0] / (1024 ** 2)).__round__(2),
                                                                     (memory[1] / (1024 ** 2)).__round__(2)))
    file.write("Disk usage (Mb): total {0}, free {1}\n".format((disk_io[0] / (1024 ** 2)).__round__(2),
                                                               (disk_io[2] / (1024 ** 2)).__round__(2)))
    file.write("Network stats: \n{0}\n".format(network))
    file.write("\n============================================\n")
    counter += 1
    file.close()


# function logging to Json
def tojsonfile():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    vmemory = psutil.virtual_memory()
    memory = psutil.swap_memory()
    cpu_load = psutil.cpu_percent(interval=1, percpu=True)
    disk_io = psutil.disk_usage('/')
    network = psutil.net_io_counters(pernic=False)
    json_file = open("outputdata.json", "a")
    global counter
    snapshot = {
        'Timestamp': timestamp,
        'CPU_load': cpu_load,
        'Vmemory': vmemory,
        'Memory': memory,
        'IO_info': disk_io,
        'Network_info': network
    }
    data = ['SNAPSHOT' + str(counter) + ": " + str(timestamp) + ": ", snapshot]
    json.dump(data, json_file, indent=3, sort_keys=True)
    counter += 1
    json_file.close()


# condition (type file)
if file_type == "txt":
    print('Output file type = ' + file_type + ', interval = ' + interval + ' minutes')
    schedule.every(int(interval)).minutes.do(totxtfile)
elif file_type == "json":
    print('Output filetype = ' + file_type + ', interval = ' + interval + ' minutes')
    schedule.every(int(interval)).seconds.do(tojsonfile)
else:
    print("Bad filetype in config file")
    quit()
while True:
    schedule.run_pending()
