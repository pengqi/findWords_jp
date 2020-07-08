#!/usr/bin/env python
'''
@file: build_my_dictionary.py
@time: 2020/1/28 18:39
@function: 建立自己词库，该词库记录会的单词
'''
import sys
import os
import msvcrt
import re
from janome.tokenizer import Tokenizer


def all_files_path(rootDir):
    filepaths = []
    for root, dirs, files in os.walk(rootDir):     
        for file in files:                         
            file_path = os.path.join(root, file)   
            filepaths.append(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            all_files_path(dir_path)               #
    return filepaths

def split_words(filename):
    """
    将英文文章进行分词
    :param filename: 文章路径，且文件为txt格式
    :return: 单词列表，有重复，单词全部小写化
    """
    fileName = filename
    try:
        with open(fileName, 'r', encoding='utf-8', errors='ignore') as f:
            text0 = f.readlines()
    except:
        with open(fileName, 'r', encoding='gbk', errors='ignore') as f:
                text0 = f.readlines()
    t = Tokenizer()
    words = []
    for line in text0:
        content = line
        ls = list(t.tokenize(content, stream=True, wakati=True))
        words.append(ls)
    punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*', '‘',
                            '’', '】', '【', '[', ']', '"', '“', '”', '/', '\\']
    words = [i for j in words for i in j]
    words2 = words.copy()
    for i in words2:
        pat = "[1-9]+"
        if re.match(pat, i) and (i in words):
            words.remove(i)
        elif i in punctuations:
            words.remove(i)
    return words


def text_save(filename, data):
    """
    将列表写入txt文件中
    :param filename:文件名，或者文件路径
    :param data: 一维列表
    :return: None
    """
    try:
        f = open(filename, 'a', encoding='utf-8')
    except Exception:
        f = open(filename, 'a', encoding='gbk')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')
        s = s.replace("'", '').replace(",", '') + ' '
        f.write(s)
    f.close()
    print(f'文件保存成功\n位置：{filename}')


def merge():
    root = module_path + '\data'
    files = all_files_path(root)
    olds = []
    for i in files:
        olds.append(split_words(i))
    try:
        olds = [i for j in olds for i in j]
    except Exception:
        olds = [k for i in olds for j in i for k in j]
    olds = list(set(olds))
    the_real_olds = split_words('understanding_words.txt')
    olds =list(set(olds) - set(the_real_olds))
    path1 = r'understanding_words.txt'
    with open(path1, 'a', encoding='utf-8') as f:
        for i in range(len(olds)):
            s = str(olds[i]).replace('[', '').replace(']', '')
            s = s.replace("'", '').replace(",", '') + ' '
            f.write(s)
    print('词库合并完成\n')


def select_words(old_words, word):
    """
    判断该单词会不会，会的放进列表中
    :param old_words: 列表
    :param word: 要判断的单词
    :return: old_words
    """
    sys.stdout.flush()
    try:
        butto = msvcrt.getch().decode('utf-8')
    except:
        butto = '\x00'
        print('无效操作, 请继续')
    while butto == '\x00':
        try:
            butto = msvcrt.getch().decode('utf-8')
        except:
            butto = '\x00'
            print('无效操作，请继续')
    if butto == '1':
        old_words.append(word)
    elif butto == '2':
        pass
    elif butto == '3':
        number = 1
        while True:
            output_txt = module_path + "/data/old_words_" + str(number) + '.txt'
            if not os.path.exists(output_txt):
                break
            number += 1
        text_save(output_txt, old_words)
        merge()
        print('已退出')
        os._exit(0)
    else:
        print('请输入1 ，2，or 3， 23333333333333，或者看看小键盘有没有开启')
    return old_words


if __name__ == '__main__':
    sys.path.append(os.path.split(__file__)[0])
    print('加载中,请稍等...')
    module_path = os.path.dirname(__file__)
    path = module_path + "/article"
    files = all_files_path(path)
    if len(files) == 0:
        print(f'article文件夹中无文件，请放入文件。路径：{path}')
        os._exit(0)
    print("请输入 1, 2 or 3, 1代表着 会，2代表着 不会, 3代表着 保存并退出")
    for filename in files:
        merge()
        print(f'正在读取文件：{filename}')
        words = split_words(filename)
        words = list(set(words))
        understanding_txt = 'understanding_words.txt'
        understanding_words = split_words(understanding_txt)
        words = list(set(words) - set(understanding_words))
        old_words = []
        for i in range(len(words)):
            try:
                print(f"{words[i]} ({len(words) - i}个)\n")
            except:
                pass
            old_words = select_words(old_words, words[i])
        number = 1
        while True:
            output_txt = module_path + "/data/old_words_" + str(number) + '.txt'
            if not os.path.exists(output_txt):
                break
            number += 1
        text_save(output_txt, old_words)
        print(f'\n恭喜你，输入词库：{len(old_words)}个\n 词库总计：{len(understanding_words) + len(old_words)}个\n')
        other_words = list(set(words) - set(old_words))
        number = 1
        while True:
            output_txt = module_path + "/output/output_" + str(number) + '.txt'
            if not os.path.exists(output_txt):
                break
            number += 1
        text_save(output_txt, other_words)
    merge()