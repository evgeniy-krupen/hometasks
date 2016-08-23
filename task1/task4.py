import configparser
import datetime
import json
import psutil
import schedule
import time

# parser config file
Config = configparser.ConfigParser()
Config.read("config3.ini")
file_type = Config.get('common', 'output')
interval = Config.get('common', 'interval')

#class with my variables
class myvar:
    counter = 1
    'this is my parent class'
    def __init__(self):
         self.timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
         self.counter = 1
         self.VMEMORY = psutil.virtual_memory()
         self.MEMORY = psutil.swap_memory()
         self.CPU_LOAD = psutil.cpu_percent(interval=1, percpu=True)
         self.DISK_IO = psutil.disk_usage('/')
         self.NETWORK = psutil.net_io_counters(pernic=False)

#class for txt to file (with Inheritance)
class TXTClass(myvar):
    'class for TXT-TO-FILE'
    def ToTxtFile(self):
        '''write to txt file'''
        file = open("output.txt", "a")
        file.write("\n###Snapshot {0}: TimeStamp {1}\n".format(myvar.counter, self.timestamp))
        file.write("CPU load (%): {0}\n".format(self.CPU_LOAD))
        file.write("Memory usage (Mb): used {0}, free {1}\n".format((self.VMEMORY[4] / (1024 ** 2)).__round__(2),
                                                                    (self.VMEMORY[5] / (1024 ** 2)).__round__(2)))
        file.write("Swap Memory stat (Mb): total {0}, used {1}\n".format((self.VMEMORY[0] / (1024 ** 2)).__round__(2),
                                                                         (self.VMEMORY[1] / (1024 ** 2)).__round__(2)))
        file.write("Disk usage (Mb): total {0}, free {1}\n".format((self.DISK_IO[0] / (1024 ** 2)).__round__(2),
                                                                   (self.DISK_IO[2] / (1024 ** 2)).__round__(2)))
        file.write("Network stats: \n{0}\n".format(self.NETWORK))
        file.write("\n============================================\n")
        file.close()
        myvar.counter += 1

#class for txt to json (with Inheritance)
class JSONclass(myvar):
    def ToJsonFile(self):
       json_file = open("outputdata.json", "a")
       snapshot = {
           'Timestamp': self.timestamp,
           'CPU_load': self.CPU_LOAD,
           'Vmemory': self.VMEMORY,
           'Memory': self.MEMORY,
           'IO_info': self.DISK_IO,
           'Network_info': self.NETWORK
       }
       data = ['SNAPSHOT ' + str(myvar.counter) + ": " + str(self.timestamp) + ": ", snapshot]
       json.dump(data, json_file, indent=3, sort_keys=True)
       json_file.close()
       myvar.counter += 1

# initialization with condition
def run():
    if file_type == "txt":
       txt_obj = TXTClass()
       txt_obj.ToTxtFile()

    elif file_type == "json":
       txt_obj = JSONclass()
       txt_obj.ToJsonFile()

schedule.every(int(5)).seconds.do(run)
while True:
    schedule.run_pending()



