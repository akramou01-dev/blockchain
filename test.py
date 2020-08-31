# # test = ["test"]
# # if test[0]==test[-1]:
# #     print("Yes")
# # else : 
# #     print("No")

# # for i in range(-20 ,-10): 
# #     print(i)

# # test = 1 
# # test1 = "1"
# # print(test is test1)
# # simple_list = [1,2,3,4,5]
# # list_doublé = []
# # for element in simple_list: 
# #     list_doublé.append(element * 2)

# # print(list_doublé)

# # double_list = [element *2 for element in simple_list]
# # print(dou     ble_list)

# stats = [('age',21),('height',180),('width',89)]
# print(stats)
# dict_stats = {key:value for (key, value) in stats }
# print(dict_stats)
# simple_list = [1,2,3,4,5]
# simple_list.extend([6,7])
# print(simple_list)

# print(simple_list)

# d ={'name':'akram', 'age':21}
# print(d.items())

# for k, v in d.items():
#     print(k,v)

# t = ('akram',21,'age')
# print(t.index(21))

# s = {'akram',"melissa", "marouan"}
# s.discard('akram')
# print(s)


# def unlimited_arguments(*args, **keyword_args): 
#     print(keyword_args)
#     for (key, value) in keyword_args.items():
#         print("{} : {} ".format(key,value ))


# unlimited_arguments([1,2,"akram",True,5,6,7,8,9], name ="akram", age  = 21)
# import json

# my_dict = [1,2,3,4]
# print(json.dumps(my_dict).encode())

import collections 

my_dict = {'name':'Akram','age':21}