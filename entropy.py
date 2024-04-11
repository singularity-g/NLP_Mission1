import PyPDF2
import jieba
import math
import os
import re
from collections import Counter
def calculate_entropy_1(unigram_tf):
    entropy = 0.0
    word_len = sum([item[1] for item in unigram_tf.items()])
    for word in unigram_tf.items():
        entropy -= word[1]/word_len * math.log2(word[1]/word_len)
    return entropy

def calculate_entropy_2(unigram_tf,bigram_tf):
    entropy = 0.0
    word_len = sum([item[1] for item in bigram_tf.items()])
    for word in bigram_tf.items():
        p_xy = word[1]/word_len
        p_x_y = word[1]/unigram_tf[word[0][0]]
        entropy -= p_xy * math.log2(p_x_y)
    return entropy

def calculate_entropy_3(bigram_tf,trigram_tf):
    entropy = 0.0
    word_len = sum([item[1] for item in trigram_tf.items()])
    for word in trigram_tf.items():
        p_xy = word[1]/word_len
        p_x_y = word[1]/bigram_tf[word[0][0],word[0][1]]
        entropy -= p_xy * math.log2(p_x_y)
    return entropy
def read_txt_files(directory):
    txt_contents = {}
    corpus_text = ""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith('.txt'):
            with open(filepath, 'r', errors='ignore') as file:
                file_content = file.read()
                file_content = file_content.replace(
                '本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com', '')
                txt_contents[filename] = file_content
                corpus_text += file_content + " "
    return corpus_text

def get_unigram_tf(word):
    unigram_tf = {}
    for w in word:
        unigram_tf[w] = unigram_tf.get(w, 0) + 1
    return unigram_tf

def get_bgram_tf(word):
    bgram_tf = {}
    for i in range(len(word) - 1):
        bgram_tf[(word[i], word[i + 1])] = bgram_tf.get(
            (word[i], word[i + 1]), 0) + 1
    return bgram_tf

def get_trigram_tf(word):
    trigram_tf = {}
    for i in range(len(word) - 2):
        trigram_tf[(word[i], word[i + 1], word[i+2])] = trigram_tf.get(
            (word[i], word[i + 1], word[i+2]), 0) + 1
    return trigram_tf
def stop_word():
    with open('cn_stopwords.txt', encoding='utf-8') as f:
        con = f.readlines()
        stop_words = set()  # 集合可以去重
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)
    return stop_words

def remove_stopwords(text,stopwords):
    words = jieba.cut(text)  # jieba分词是二元分词
    filtered_words = [word for word in words if word not in stopwords]
    return " ".join(filtered_words), "".join(filtered_words)
def main():
    current_directory = os.getcwd()
    print(current_directory)
    # 读取PDF文件
    file_path = 'D:\mission1\Data'  # 文件所在路径
    # pathname = os.path.join(current_directory, file_path)
    stop_words = stop_word()
    data = read_txt_files(file_path)
    # 分词
    text = "".join(re.findall('[\u4e00-\u9fa5]+', data, re.S))
    words,char_data = remove_stopwords(text,stop_words) #连接去除了无用部分的语料
    words = words.split()
    # 计算信息熵
    unigram_tf = get_unigram_tf(words)
    bgram_tf = get_bgram_tf(words)
    trigram_tf = get_trigram_tf(words)
    unigram_word_entropy = calculate_entropy_1(unigram_tf)
    bigram_word_entropy = calculate_entropy_2(unigram_tf,bgram_tf)
    trigram_word_entropy = calculate_entropy_3(bgram_tf,trigram_tf)
    print("一元词的信息熵:", unigram_word_entropy)
    print("二元词的信息熵:", bigram_word_entropy)
    print("三元词的信息熵:", trigram_word_entropy)
    unigram_tf = get_unigram_tf(char_data)
    bgram_tf = get_bgram_tf(char_data)
    trigram_tf = get_trigram_tf(char_data)
    unigram_word_entropy = calculate_entropy_1(unigram_tf)
    bigram_word_entropy = calculate_entropy_2(unigram_tf,bgram_tf)
    trigram_word_entropy = calculate_entropy_3(bgram_tf,trigram_tf)
    print("一元字的信息熵:", unigram_word_entropy)
    print("二元字的信息熵:", bigram_word_entropy)
    print("三元字的信息熵:", trigram_word_entropy)
if __name__ == "__main__":
    main()
