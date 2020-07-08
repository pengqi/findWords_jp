#!/usr/bin/env python

'''
@file: find_disunderstanding_words.py
@time: 2020/1/28 15:12
@function: 导入文章，找出不会的单词
注意：这里没有词形还原
'''
import shutil
import os
import re
from datetime import datetime
from janome.tokenizer import Tokenizer


def merge():
    # 读取文件夹里的所有文件
    module_path = os.path.dirname(__file__)   
    root = module_path + '\data'
    files = all_files_path(root)
    # 分词
    olds = []
    for i in files:
        olds.append(split_words(i))
        try:
            olds = [i for j in olds for i in j]
        except Exception:
            olds = [k for i in olds for j in i for k in j]
    olds = list(set(olds))  
    # 去重————去掉会的
    the_real_olds = split_words('understanding_words.txt')
    olds =list(set(olds) - set(the_real_olds))
    # 合并
    path1 = r'understanding_words.txt'
    with open(path1, 'a', encoding='utf-8') as f:
        for i in range(len(olds)):
            s = str(olds[i]).replace('[', '').replace(']', '')
            s = s.replace("'", '').replace(",", '') + ' '
            f.write(s)
    print('词库合并完成\n')


def split_words(filename):
    """
    将英文文章进行分词
    :param filename: 文章路径，且文件为txt格式
    :return: 单词列表，有重复，单词全部小写化
    """
    # 日语分词
    fileName = filename  
    # try:
    #     f = open(fileName, 'r', encoding='utf-8')
    # except:
    #     f = open(fileName, 'r', encoding='gbk')
    # text0 = f.readlines()
    # f.close()
    try:
        with open(fileName, 'r', encoding='utf-8', errors='ignore') as f:
            text0 = f.readlines()
    except:
        with open(fileName, 'r', encoding='gbk', errors='ignore') as f:
                text0 = f.readlines()
    # 分词
    t = Tokenizer()
    words = []
    for line in text0:
        content = line
        ls = list(t.tokenize(content, stream=True, wakati=True))
        words.append(ls)
    #  去除标点 （停用词可以不去，反正到时候一相减也没了） english_stopwords = stopwords.words("english")
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*', '‘',
                            '’', '】', '【', '[', ']', '"', '“', '”', '/', '\\'] 
    words = [i for j in words for i in j]  
    words2 = words.copy()
    for i in words2:
        # 去除数字，如果字符串中有数字，则去除
        pat = "[1-9]+"
        if re.match(pat, i) and (i in words):
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
        s = s.replace("'", '').replace(",", '') + '\n'
        f.write(s)
    f.close()
    print(f'文件保存成功\n位置：{filename}')


def all_files_path(rootDir):
    filepaths = []
    for root, dirs, files in os.walk(rootDir):     
        for file in files:                         
            file_path = os.path.join(root, file)   
            filepaths.append(file_path)            
        for dir in dirs:                           
            dir_path = os.path.join(root, dir)     
            all_files_path(dir_path)               
    return filepaths


def mymovefile(file, dstfile = r'articles_recycle'):
    if not os.path.isfile(file):
        print("%s not exist!" % (file))
    else:
        # fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        fpath, fname = os.path.split(file)
        if not os.path.exists(dstfile):
            os.makedirs(dstfile)  
        dstfile = dstfile + '\\' + fname
        shutil.move(file, dstfile)  
        print("move %s -> %s" % (file, dstfile))


def get_useful_words(filepath):
    words = split_words(filepath)  
    words = list(set(words))  
    # 去会的
    understanding_txt = r'understanding_words.txt'
    understanding_words = split_words(understanding_txt)  
    words = list(set(words) - set(understanding_words) )
    return words


if __name__ == '__main__':

    start_time = datetime.now()  
    print(f'开始时间：{start_time}')
    merge()
    time2 = datetime.now()  
    # 读取所有文件
    module_path = os.path.dirname(__file__)   
    path = module_path + "/article"  
    # files = os.listdir(path)  
    files = all_files_path(path)
    # 无文件则终止
    if len(files) == 0:
        print(f'article文件夹中无文件，请放入文件。路径：{path}')
        os._exit(0)
    for file in files:
        words = get_useful_words(file)
        try:
            words.sort()
        except:
            pass
        # 写入文件中
        if len(words) != 0:
            filename = os.path.split(file)[1]
            filename = os.path.splitext(filename)[0]  
            number = 1
            while True:
                output_txt = module_path + "/output/" + filename + '.txt'
                if not os.path.exists(output_txt):
                    break
                output_txt = module_path + "/output/" + filename + '_' + str(number) + '.txt'
                if not os.path.exists(output_txt):
                    break
                number += 1
            text_save(output_txt, words)
        print(f"最后总共有：{len(words)}个单词\n")
        print(f'个数： {len(words)}  \n{words}')
        mymovefile(file)
        # 时间计算
        time3 = datetime.now()  
        print(f'结束时间：{time3}\n该文件用时：{time3 - time2}')
        time2 = time3  
    end_time = datetime.now()
    print(f'结束时间：{end_time}\n总计时间：{end_time - start_time}')




