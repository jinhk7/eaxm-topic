# src/saver.py

def save2html(content, file_path):
    # 将内容保存到HTML文件中
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)
    print('追加文件成功')

def save2text(content, file_path):
    # 将内容保存到文本文件中
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)
