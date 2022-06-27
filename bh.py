import browserhistory as bh

dict_obj = bh.get_browserhistory()

my_arr = list(dict_obj['chrome'][0:10][0:10])

for history in my_arr:
    print(str(history))