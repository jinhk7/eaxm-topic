import requests
import os
from bs4 import BeautifulSoup
import json
import argparse
from datetime import datetime

def http_requests(url):
    headers = {
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(url, headers=headers)
    return response

def save2html(str, file_path):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(str)
    print('追加文件成功')

def save2text(str, file_path):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(str)

def abc2num(str):
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

def format_question(url):
    bs1 = BeautifulSoup(http_requests(url).text, "html.parser")
    soup = bs1.select('[class="discussion-header-container"]')
    question_num = soup[0].find('div', class_='question-discussion-header').find('div').get_text(separator='\n',strip=True)
    img_tags = soup[0].find_all('img')
    for img_tag in img_tags:
        img_tag.replace_with(img_tag['src'])
    answer = json.loads(soup[0].find('div', class_='voted-answers-tally').find('script').get_text())
    question_element = soup[0].find('div', class_='question-body')
    question_text = question_element.find('p', class_='card-text').get_text()
    options_elements = question_element.find_all('li', class_='multi-choice-item')
    options_text = [option.get_text(strip=True) for option in options_elements]
    question_text = '\n'.join(line.strip() for line in question_text.split('\n'))

    result = f'{question_num}'
    result += f'{question_text}'
    result += f'选项：\n'
    for option in options_text:
        formatted_option = f'{option[0]} {option[1:]}'
        result += f'{formatted_option}\n'
    result += f'答案： {answer[0]["voted_answers"]}\n'
    result += f'\n\n\n'
    return result


def format_question_anki(url):
    bs1 = BeautifulSoup(http_requests(url).text, "html.parser")
    soup = bs1.select('[class="discussion-header-container"]')
    answer_abc = json.loads(soup[0].find('div', class_='voted-answers-tally').find('script').get_text())[0]['voted_answers']
    answer_num = abc2num(answer_abc)
    question_num = soup[0].find('div', class_='question-discussion-header').find('div').get_text(separator='\n',strip=True)
    question_element = soup[0].find('div', class_='question-body')
    question_text = question_element.find('p', class_='card-text')
    question_text = question_text.prettify()
    options_elements = question_element.find_all('li', class_='multi-choice-item')
    options_text = [option.get_text(strip=True) for option in options_elements]
    for i in range(len(options_elements)):
        if options_elements[i-1].find_all('img'):
            options_text[i-1] =  options_text[i-1] + str(options_elements[i-1].find_all('img')[0])
    question_all = ''
    question_all = '*' + question_num + question_text + '**'
    for option in options_text:
        formatted_option = f'{option[2:]}'
        question_all += formatted_option + '\n'
    question_all += '***'
    question_all += answer_num + '\n'
    question_all += '****' + url
    question_all += '\n\n'
    return question_all

def help_message():
    print("Usage:")
    print("python script.py -u URL_FILE [--output OUTPUT_FILE] [-m MODE]")
    print("Modes:")
    print("  text     : Output questions and answers in text mode.")
    print("  anki     : Output questions and answers in Anki mode.")

def main():
    parser = argparse.ArgumentParser(description='Scraping Questions and Answers from URLs in a file')
    parser.add_argument('-u', '--url_file', metavar='URL_FILE', type=str, help='Path to the file containing URLs', required=True)
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('-m', '--mode', choices=['txt', 'anki'], default='anki', help='Output mode (default: anki)')
    args = parser.parse_args()

    if not os.path.exists(args.url_file):
        print("Error: URL file does not exist.")
        return

    urls = []
    with open(args.url_file, 'r') as f:
        for line in f:
            urls.append(line.strip())

    if args.output:
        output_file = args.output
    else:
        today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"output_{today}.html"

    count = 0
    for url in urls:
        count += 1
        if args.mode == 'anki':
            save2html(format_question_anki(url), output_file)
        elif args.mode == 'txt':
            output_text_file = f"output_text_{today}.txt"
            save2text(format_question(url), output_text_file)
        print(f'完成第 {count} 个题目收集，地址为：{url}')

if __name__ == "__main__":
    main()
