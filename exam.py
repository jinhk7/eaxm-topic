import requests
import os
from bs4 import BeautifulSoup
import json

def http_requests(url):
    url=url
    headers = {
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(url,headers=headers)
    return response

def save2html(str,file_path):
    with open(file_path,'a',encoding='utf-8') as f:
        f.write(str)
    print('追加文件成功')



def format_question(url):

    bs1 = BeautifulSoup(http_requests(url).text,"html.parser")

    soup=bs1.select('[class="discussion-header-container"]')



    img_tags = soup[0].find_all('img')
    for img_tag in img_tags:
        img_tag.replace_with(img_tag['src'])
    # 提取题干
    answer=soup[0].find('div', class_='voted-answers-tally').find('script').get_text()
    answer_dict=soup[0].find('div', class_='voted-answers-tally').find('script').get_text()
    answer = json.loads(answer_dict)

    question_element = soup[0].find('div', class_='question-body')

    question_text = question_element.find('p', class_='card-text').get_text()

    # 提取选项
    options_elements = question_element.find_all('li', class_='multi-choice-item')
    options_text = [option.get_text(strip=True) for option in options_elements]
    question_text = '\n'.join(line.strip() for line in question_text.split('\n')) # 去掉前后的制表符和空格
    # 打印题干和选项内容




    print('题干：', question_text)
    #print('选项：', options_text)
    for option in options_text:
        formatted_option = f'{option[0]} {option[1:]}'  # 使用切片操作将第一个字符（字母）和后面的内容分开
        print(formatted_option)

    print('答案：',answer[0]['voted_answers'])

# for https://ankimemory.com/
def format_question_anki(url):

    bs1 = BeautifulSoup(http_requests(url).text,"html.parser")

    soup=bs1.select('[class="discussion-header-container"]')

    # img_tags = soup[0].find_all('img')
    # for img_tag in img_tags:
    #     img_tag.replace_with(img_tag['src'])
    #提取答案

    answer=soup[0].find('div', class_='voted-answers-tally').find('script').get_text()
    answer_dict=soup[0].find('div', class_='voted-answers-tally').find('script').get_text()
    answer = json.loads(answer_dict)


    # 提取题干
    question_element = soup[0].find('div', class_='question-body')

    question_text = question_element.find('p', class_='card-text')
    #question_text = question_element.find('p', class_='card-text').get_text()
    # 提取选项
    options_elements = question_element.find_all('li', class_='multi-choice-item')
    options_text = [option.get_text(strip=True) for option in options_elements]
    #question_text = '\n'.join(line.strip() for line in question_text.split('\n')) # 去掉前后的制表符和空格
    # 打印题干和选项内容




    print('*', question_text.prettify())
    print('**',end='')
    for option in options_text:
        formatted_option = f'{option[1:]}'  # 使用切片操作将第一个字符（字母）和后面的内容分开
        print(formatted_option)

    print('***',answer[0]['voted_answers'])
    print('****')
    print()

# 59 69



# save2html(bs[0],'example.html')
# print(type(dis_cont))


url='https://www.examtopics.com/discussions/amazon/view/127046-exam-aws-certified-security-specialty-scs-c02-topic-1/'   #无图
url1='https://www.examtopics.com/discussions/amazon/view/127041-exam-aws-certified-security-specialty-scs-c02-topic-1/'  #选项图片
url2='https://www.examtopics.com/discussions/amazon/view/122814-exam-aws-certified-security-specialty-scs-c02-topic-1/'  #题目含图片

#format_question(url2)


format_question_anki(url2)