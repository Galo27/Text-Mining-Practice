######################
#!/usr/bin/python
# -*- coding: utf-8 -*-
# By Galo
######################
import os
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer #词性还原
from nltk.tokenize import sent_tokenize #分句
from nltk.tokenize import word_tokenize #分词
from nltk.corpus import stopwords       #去停用词
from nltk.stem import SnowballStemmer   #词干提取
from sklearn.feature_extraction.text import TfidfVectorizer #TFIDF
import chardet                          #检测编码格式
import re                               #匹配去标点符号，特殊字符

#nltk.download()    #下载nltk的语料库
cachedStopWords = stopwords.words("english")    #选用英文停用词词典


def read_files(path):
    # 读取语料文件夹下所有文件内容（此处为二进制文件）
    # 所有文件内文本组合成一个string存入all_text
    files= os.listdir(path)  # 得到文件夹下的所有文件名称
    all_text = ""
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            with open(path+"/"+file, "rb") as f:  # 二进制格式文件参数为rb
                text = f.read()
            encode_type = chardet.detect(text)  # 检测编码格式
            if encode_type['encoding'] != None:  # 排除不能解码的情况
                text = text.decode(encode_type['encoding'])  # 进行相应解码，赋给原标识符（变量）
                print(file,'done.')  # 标识文件读取完毕
                all_text = all_text + text
    return all_text


'''
#这一部分先分句后分词，后来实测没啥用好像，因为数据结构变复杂，所以舍弃了

sentences = sent_tokenize(atheism)
#分句,将文本拆分成句子级别
with open('C:\\Users\\Administrator\\Desktop\\Preprocessing\\sentences_atheism_sent_tokenize.txt', 'w',encoding='utf-8') as f:
    for sentence in sentences:
        f.write(str(sentence))
print('Sentences written.')

words = []
for sentence in sentences:
    sentence = re.sub("[+:\.\!\/_,$%^*(+\"\'<>]+|[+——！，。？、~@#￥%……&*（）]+", " ", sentence)
    #去标点
    words.append(word_tokenize(sentence))
    #分词，对句子进行分词，tokenize的分词是句子级别的，需要对文本先进行分句，否则效果会很差？？？没看出效果有差啊
with open('C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize.txt', 'w',encoding='utf-8') as f:
    for word in words:
        f.write(str(word))
print('Words written.')

wordStoped = []
for word in words:  #去停用词
    filtered = [w.lower() for w in word if (w.lower() not in cachedStopWords and len(w) > 2)]
    #去停用词+去长度小于3的单词+小写化
    wordStoped.append(filtered)
with open('C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped.txt', 'w',encoding='utf-8') as f:
    for wordSt in wordStoped:
        f.write(str(wordSt))
print('WordsStopped written.')
'''


def word_tokenize_stopwords_removal(all_text):
    # 对整个文本进行分词，这里为不分句直接分词,并去停用词、标点、特殊字符、带符号单词
    # 返回处理结果list：word_stopped
    # atheism = re.sub("[+:\.\!\/_,$%^*(+\"\'<>=]+|[+——！，。？、~@#￥%……&*（）]+", " ", atheism)
    # words = word_tokenize(atheism)
    # 分词前去掉符号标点和特殊字符，转化为空格，也可以先分词再去掉含标点的词，后者去掉的东西更多，这里采取后一种

    words = [word for word in word_tokenize(all_text) if (str.isalpha(word) is not False)]
    # 分词，同时直接去掉所有带符号的词，如邮箱后缀、hyphen连词、缩写等
    path_word_tokenize = 'C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize.txt'
    # 存放上述分词处理结果的文本路径
    with open(path_word_tokenize, 'w',encoding='utf-8') as f:
        f.write(str(words))
    print('Words written.')

    word_stopped = [w.lower() for w in words if (w.lower() not in cachedStopWords and len(w) > 2 and str.isalpha(w) is not False)]
    # 小写化后去停用词+去长度小于3的单词+去数字和包含符号的单词如 2-year
    path_word_tokenize_stopped = 'C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped.txt'
    # 存放上述去停用词处理结果的文本路径
    with open(path_word_tokenize_stopped, 'w', encoding='utf-8') as f:
        f.write(str(word_stopped))
    print('WordsStopped written.')

    return word_stopped


def word_pos_tags(word_stopped):
    # 词性标注,返回以单词+词性标注为元组的list: pos_tags
    pos_tags = nltk.pos_tag(word_stopped)
    path_word_tokenize_stopped_pos_tag = \
        'C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped_postag.txt'
    # 存放词性标注处理结果的文本路径
    with open(path_word_tokenize_stopped_pos_tag, 'w', encoding='utf-8') as f:
        f.write(str(pos_tags))
    print('Pos_tags written.')
    return pos_tags


def get_wordnet_pos(treebank_tag):
    # 词性标注提取
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_string(pos_tags):
    # 词形还原后词干提取函数，返回还原后的单词list: res
    res = []
    lemmatizer = WordNetLemmatizer()  # 初始化词形还原对象
    stemmer = SnowballStemmer("english")  # 选择语言，初始化词干提取对象
    for word, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(stemmer.stem(lemmatizer.lemmatize(word, pos=wordnet_pos)))
    return res


def do_lemma_stemmer(pos_tags):
    # 进行词形还原和词干提取,并输出记录结果
    # 返回仅由空格分隔单词的纯文本，即一个string的list: wordLemmatizedStemmeredWordOnly
    word_lemmatized_stemmered = lemmatize_string(pos_tags)
    path_word_tokenize_stopped_postag_lemmatized_stemmered_wordonly = \
        'C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped_postag_lemmatized_stemmered_wordonly.txt'
    # 存放词形还原和词干提取处理结果的文本路径
    with open(path_word_tokenize_stopped_postag_lemmatized_stemmered_wordonly, 'w', encoding='utf-8') as f:
        for word in word_lemmatized_stemmered:
            #sklearn中TFIDF计算需要的格式是仅由空格分隔单词的纯文本
            f.write(str(word))
            f.write(str(' '))
    print("WordLemmatized&Stemmered written.")

    word_lemmatized_stemmered_wordonly = []  # 重读出所需格式文本
    with open('C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped_postag_lemmatized_stemmered_wordonly.txt', 'r',encoding='utf-8') as f:
        word_lemmatized_stemmered_wordonly.append(f.read())

    return word_lemmatized_stemmered_wordonly


def TFIDF(word_lemmatized_stemmered_wordonly):
    # TFIDF计算
    tf_idf = TfidfVectorizer()  # 初始化对象
    tf_data = tf_idf.fit_transform(word_lemmatized_stemmered_wordonly)  # 计算TFIDF值
    words = tf_idf.get_feature_names()  # 取出所统计单词项
    TFIDF = dict()  # 创建空字典
    path_TFIDF = 'C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped_postag_lemmatized_stemmered_TFIDF.txt'
    path_TFIDF_sorted = 'C:\\Users\\Administrator\\Desktop\\Preprocessing\\words_atheism_word_tokenize_Stopped_postag_lemmatized_stemmered_TFIDF_sorted.txt'

    with open(path_TFIDF, 'w', encoding='utf-8') as f:
        # 向文件写入TFIDF值
        for i in range(len(word_lemmatized_stemmered_wordonly)):
            for j in range(len(words)):
                if tf_data[i, j] > 1e-5:
                    f.write(words[j] + ':' + str(tf_data[i, j]))
                    f.write('\n')
                    TFIDF[str(words[j])] = tf_data[i, j]
        print("TFIDF written.")

    TFIDFSorted = sorted(TFIDF.items(), key=lambda e: e[1], reverse=True)
    # 按TFIDF值大小排序

    with open(path_TFIDF_sorted, 'w', encoding='utf-8') as f:
        # 向文件写入排序后的TFIDF值
        for key in TFIDFSorted:
            f.write(str(key))
            f.write('\n')
    print("TFIDF sorted written.")

    return


if __name__ == '__main__':
    path = "C:\\Users\\Administrator\\Desktop\\Preprocessing\\20news-19997\\20_newsgroups\\alt.atheism"
    # 待处理语料文件夹目录
    atheism = read_files(path)
    stopped_words = word_tokenize_stopwords_removal(atheism)
    pos_tags_word = word_pos_tags(stopped_words)
    TFIDF(do_lemma_stemmer(pos_tags_word))