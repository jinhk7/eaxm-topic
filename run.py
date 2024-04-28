# run.py
import os
import argparse
from datetime import datetime
from time import sleep
from src import  saver, scraper

def help_message():
    # 打印帮助信息
    print("Usage:")
    print("python run.py -u URL_FILE [--output OUTPUT_FILE] [-m MODE]")
    print("Modes:")
    print("  text     : Output questions and answers in text mode.")
    print("  anki     : Output questions and answers in Anki mode.")

def main():
    # 主函数，解析命令行参数并执行相应操作
    parser = argparse.ArgumentParser(description='Scraping Questions and Answers from URLs in a file')
    parser.add_argument('-u', '--url_file', metavar='URL_FILE', type=str, help='Path to the file containing URLs', required=True)
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('-m', '--mode', choices=['text', 'anki'], default='anki', help='Output mode (default: anki)')
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
            formatted_question = scraper.format_question_anki(url)
            saver.save2html(formatted_question, output_file)
        elif args.mode == 'text':
            output_text_file = f"output_text_{today}.txt"
            formatted_question = scraper.format_question(url)
            saver.save2text(formatted_question, output_text_file)
        print(f'完成第 {count} 个题目收集，地址为：{url}')
        sleep(1)

if __name__ == "__main__":
    main()
