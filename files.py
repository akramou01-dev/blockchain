test = [1,2,3,4,('name',"Akram"),('age',21)]
with open('demo.txt',mode='w') as f:

    # # test = f.read()
    # # f.write('this is a test \n abt the line break')
    # file_content= f.readlines() 

    # for line in file_content:
    #     print(line[1])

    # f.close()

    f.write(str(test))

print('Done')
