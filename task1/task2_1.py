# define lists
list_key = ['name', 'lastname','sex','age','married', 'child']
list_value = ['evgeniy','krupen','man', 25]
# condition
if len(list_key) > len(list_value):
  while len(list_key)>len(list_value):
    list_value.append('None')
# print
print(dict(zip(list_key,list_value)))

# function
def create_dict(key,value):
    if len(key) > len(value):
        while len(key)>len(value):
          value.append('None')
    return dict(zip(key,value))
print(create_dict(list_key,list_value))
