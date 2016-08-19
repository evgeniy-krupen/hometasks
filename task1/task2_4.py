# import regexp
import re
from collections import Counter

f = open('access_log')
data = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', f.read())
f.close()
for k in Counter(data).most_common(10):
 print("IP: "+str(k[0])+" has "+str(k[1])+" requests")

