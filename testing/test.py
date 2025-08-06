# initialising _dictionary
ini_dict = {'a': 'akshat', 'b': 'bhuvan', 'c': 'chandan'}
 
# printing initial_dictionary
print("intial_dictionary", str(ini_dict))
 
# split dictionary into keys and values
keys = []
values = []
items = ini_dict.items()
for item in items:
    keys.append(item[0]), values.append(item[1])
 
# printing keys and values separately
print("keys : ", str(keys))
print("values : ", str(values))