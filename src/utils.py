# src/utils.py

def abc2num(str):
    # 将选项字母转换为数字形式
    str = str.replace('A', '1')
    str = str.replace('B', '2')
    str = str.replace('C', '3')
    str = str.replace('D', '4')
    str = str.replace('E', '5')
    str = str.replace('F', '6')
    str_num = ''
    for i in list(str):
        str_num += i + ','
    str_num = str_num[:-1]
    return str_num
