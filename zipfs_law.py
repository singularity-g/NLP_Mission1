# -*- coding: utf-8 -*-
import re
import os
import math
import jieba
import logging
import numpy as np
import matplotlib.pyplot as plt
import glob
from collections import Counter
def read_txt_files(directory):
    txt_contents = {}
    corpus_text = ""
    with open('cn_stopwords.txt', encoding='utf-8') as f:
        con = f.readlines()
        stop_words = set()  # 集合可以去重
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith('.txt'):
            with open(filepath, 'r', errors='ignore') as file:
                file_content = file.read()
                txt_contents[filename] = file_content
                corpus_text += file_content + " "
    return corpus_text, stop_words

def count_frequency(text, stop_words):
    text = "".join(re.findall('[\u4e00-\u9fa5]+', text, re.S))
    words = jieba.lcut(text)
    word_list = []
    for word in words:
        if word not in stop_words:
            word_list.append(word)
    word_f = Counter(word_list)
    return word_f

def draw_zipf(word_f):
    sorted_f = sorted(word_f.items(),key=lambda x: x[1], reverse=True)
    ranks = np.arange(1,len(word_f)+1)
    words = [word for word, freq in sorted_f]
    freqs = [freq for word, freq in sorted_f]
    with open('words.txt', 'w') as file:
        for word in words:
            file.write(word + '\n')
    plt.figure()
    plt.plot(ranks, freqs, 'b-')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Zipf\'s Law Verification')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig('zipf.png')
    plt.show()




if __name__ == "__main__":
    file_path = 'D:\mission1\Data'  # 文件所在路径
    current_directory = os.getcwd()
    print(current_directory)
    # pathname = os.path.join(current_directory, file_path)
    # print(file_path)
    data, stop_words = read_txt_files(file_path)
    word_freq = count_frequency(data,stop_words)
    draw_zipf(word_freq)
    print("ok")