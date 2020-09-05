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

# import collections 

# my_dict = {'name':'Akram','age':21}
# print(collections.OrderedDict([('name','akram')]))

test = [{"index": 0, "previous_hash": "", "timestamp": 0, "proof": 100, "transactions": []}, {"index": 1, "previous_hash": "c775ae7455f086e2fc68520d31bfebfdb18ffeaceb933085c510d5f8d2177813", "timestamp": 1599149254.3720157, "proof": 92, "transactions": [{"sender": "Mining", "recipient": "Akram", "amount": 10}]}]

test1 = test.__dict__
print("akrampou "+ test1)