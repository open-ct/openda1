import ast
with open('./test.txt',"r") as f:    #设置文件对象
    str = f.read()    #可以是随便对文件的操作
print(str)
frame_list = ast.literal_eval(str)
for frame in frame_list:
    print(frame)