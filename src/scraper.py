# src/formatter.py
import json
from bs4 import BeautifulSoup
from .http_requests import http_requests
from .utils import abc2num


def format_question(url):
    # 格式化问题并返回格式化后的文本
    bs1 = BeautifulSoup(http_requests(url).text, "html.parser")
    soup = bs1.select('[class="discussion-header-container"]')
    question_num = soup[0].find('div', class_='question-discussion-header').find('div').get_text(separator='\n',strip=True)
    img_tags = soup[0].find_all('img')
    for img_tag in img_tags:
        img_tag.replace_with(img_tag['src'])
    voted_answers = json.loads(soup[0].find('div', class_='voted-answers-tally').find('script').get_text())
    correct_answer = soup[0].find('span', class_='correct-answer').get_text()
    if not voted_answers:
        finally_answer = correct_answer
    else:
        finally_answer = voted_answers[0]['voted_answers']
    question_element = soup[0].find('div', class_='question-body')
    question_text = question_element.find('p', class_='card-text').get_text()
    options_elements = question_element.find_all('li', class_='multi-choice-item')
    options_text = [option.get_text(strip=True) for option in options_elements]
    question_text = '\n'.join(line.strip() for line in question_text.split('\n'))

    # 构建格式化后的问题文本
    result = f'{question_num}'
    result += f'{question_text}'
    result += f'选项：\n'
    for option in options_text:
        formatted_option = f'{option[0]} {option[1:]}'
        result += f'{formatted_option}\n'

    result += f'答案： {finally_answer}\n'
    result += f'\n\n\n'
    return result


def format_question_anki(url):
    # 格式化问题以适应Anki，并返回格式化后的文本
    bs1 = BeautifulSoup(http_requests(url).text, "html.parser")
    soup = bs1.select('[class="discussion-header-container"]')
    voted_answers = json.loads(soup[0].find('div', class_='voted-answers-tally').find('script').get_text())
    correct_answer = soup[0].find('span', class_='correct-answer').get_text()
    if not voted_answers:
        finally_answer = correct_answer
    else:
        finally_answer = voted_answers[0]['voted_answers']
    answer_num = abc2num(finally_answer)
    question_num = soup[0].find('div', class_='question-discussion-header').find('div').get_text(separator='\n',strip=True)
    question_element = soup[0].find('div', class_='question-body')
    question_text = question_element.find('p', class_='card-text')
    question_text = question_text.prettify()
    options_elements = question_element.find_all('li', class_='multi-choice-item')
    options_text = [option.get_text(strip=True) for option in options_elements]
    for i in range(len(options_elements)):
        if options_elements[i-1].find_all('img'):
            options_text[i-1] =  options_text[i-1] + str(options_elements[i-1].find_all('img')[0])
    result = ''
    result = '*' + question_num + question_text + '**'
    for option in options_text:
        formatted_option = f'{option[2:]}'
        result += formatted_option + '\n'
    result += '***'
    result += answer_num + '\n'
    result += '****' + url
    result += '\n\n'
    return result