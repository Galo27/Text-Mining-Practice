# Text-Mining-Practice
Coding Practice on Text Mining Using Python

# Part2: English Text Mining: Preprocessing 文本挖掘的数据预处理

文章主干来自下面Reference中的博客，我自己进行了增加整理，感谢所有分享知识的大佬们= =
[本文原载](https://blog.csdn.net/Galoa/article/details/79859215)

## 1. Data Collection or Assembly 数据收集

【Given.】20_newsgroups.

0. [文件读写](https://www.cnblogs.com/zywscq/p/5441145.html)
1. [文件夹下所有文件读取](https://blog.csdn.net/lzgs_4/article/details/50371030)
1. 二进制文本读取，参数问rb
2. 读取文本后遇到的问题：cannot use a string pattern on a bytes-like object。编码问题，尝试decode解码成utf-8，新错误：UnicodeDecodeError: 'gbk' codec can't decode byte 0xff in position 0: illegal multibyte sequence
3. [解决方法](https://blog.csdn.net/jieli_/article/details/70166244) chardet模块检测编码，再解码，使用方法参见代码
4. 53558编码有问题，检测不出，跳过，如下图:![编码问题](https://img-blog.csdn.net/20180408215950741?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0dhbG9h/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
5. 如果自定义了和函数/头文件重名的变量则不可调用或import，显示not callable
6. utf-8类型的str写入文件open时需指定encoding='utf-8'
7. [字典排序](https://blog.csdn.net/xsj_blog/article/details/51847831)：sorted返回的是一个list，其中每一项为key和value组成的元组

## 2. Data Preprocessing 数据预处理

### 2.1 Tokenization & Segmentation 单词化 / 语块化 分词

下面基本都是单词化分词的方法。

#### 2.1.1 Sentence Tokenize（分割句子）[1](https://blog.csdn.net/panghaomingme/article/details/55210491)

实际测试发现似乎没什么意义啊？*这里不是很明白。*

1. 直接使用sent_tokenize

        from sklearn.datasets import fetch_20newsgroups  
        news = fetch_20newsgroups(subset='train')  
        X,y = news.data,news.target  
        text = X[0]  
        from nltk.tokenize import sent_tokenize  
        sent_tokenize_list = sent_tokenize(text)  
        print(sent_tokenize_list)  

2. 使用nltk.tokenize.punkt中包含了很多预先训练好的tokenize模型。

        from sklearn.datasets import fetch_20newsgroups  
        news = fetch_20newsgroups(subset='train')  
        X,y = news.data,news.target  
        print(X[0])  
        news = X[0]  
  
#### 2.1.2 Word Tokenize(分割单词)[1](https://blog.csdn.net/panghaomingme/article/details/55210491)

    from nltk.tokenize import word_tokenize  
    text='The cat is walking in the bedroom.'  
    sent_tokenize_list = word_tokenize(text)  
    print(sent_tokenize_list)  

将句子分割成词。首先用正则表达式可以自己完成；如果要利用已有工具，Python NLTK中的word_tokenize()，这个方式就是前文提到的Penn TreeBank语料库所使用的分词方法。听起来是不是很高大上，我是不会告诉你其实它也是正则表达式实现的。分词其实主要干了这么几个事：

- 将’分开. don't -> do n't, they'll -> they 'll; 
- 将大部分标点当作单独的一个词; 
- 将后一位是逗号或者引号的词分开; 
- 单独出现在一行的句号分开。

中文分词区别比较大，可以采用斯坦福或者ICTCLAS（中科院背景）的方案。[2](https://blog.csdn.net/lanxu_yy/article/details/29002543)

可参考：[【NLP】Python NLTK处理原始文本](https://www.cnblogs.com/baiboy/p/nltk5.html)

*new york 会变成 new + york,这个是单词化而不是语块化的问题*

### 2.2 Normalization 数据标准化

#### 2.2.1 Noise Removal 非文本数据去除

【Skip.】对于自己爬虫爬下来的文本(如HTML格式)需要做非文本数据去除。

这一步主要是针对我们用爬虫收集的语料数据，由于爬下来的内容中有很多html的一些标签，需要去掉。少量的非文本内容的可以直接用Python的正则表达式(re)删除, 复杂的则可以用beautifulsoup来去除。另外还有一些特殊的非英文字符(non-alpha),也可以用Python的正则表达式(re)删除。

#### 2.2.2 Spell Check 拼写检查

【Skip.】由于英文文本中可能有拼写错误，因此一般需要进行拼写检查。如果确信我们分析的文本没有拼写问题，可以略去此步。

拼写检查，我们一般用pyenchant类库完成。pyenchant的安装很简单："pip install pyenchant"即可。

对于一段文本，我们可以用下面的方式去找出拼写错误：

    from enchant.checker import SpellChecker
    chkr = SpellChecker("en_US")
    chkr.set_text("Many peope likee to watch In the Name of People.")
    for err in chkr:
    print "ERROR:", err.word

输出是：

    ERROR: peope
    ERROR: likee

找出错误后，我们可以自己来决定是否要改正。当然，我们也可以用pyenchant中的wxSpellCheckerDialog类来用对话框的形式来交互决定是忽略，改正还是全部改正文本中的错误拼写。大家感兴趣的话可以去研究pyenchant的官方文档。

#### 2.2.3 Part-Of-Speech Tagging and POS Tagger(对词进行标注)[1](https://blog.csdn.net/panghaomingme/article/details/55210491)

lemmatization在词性标注后效果比较好。

参考：[Python自然语言处理(一)--利用NLTK自带方法完成NLP基本任务](http://www.pythontip.com/blog/post/10012/)

    from nltk.tokenize import word_tokenize  #tokens是句子分词后的结果，同样是句子级的标注
    text='The cat is walking in the bedroom.'  
    sent_tokenize_list = word_tokenize(text)  
    print(sent_tokenize_list)   
    pos_tag = nltk.pos_tag(sent_tokenize_list)  
    print(pos_tag)  

#### 2.2.4 Stemming / Lemmatization 词干提取/词形还原

Lemmas differ from stems in that a lemma is a canonical form of the word, while a stem may not be a real word.[English Stemmers and Lemmatizers](http://text-processing.com/demo/stem/)

*先词形还原后词干提取，归一化不同词性的单词*

词干提取(stemming)和词型还原(lemmatization)是英文文本预处理的特色。两者其实有共同点，即都是要找到词的原始形式。只不过词干提取(stemming)会更加激进一点，它在寻找词干的时候可以会得到不是词的词干。比如"imaging"的词干可能得到的是"imag", 并不是一个词。而词形还原则保守一些，它一般只对能够还原成一个正确的词的词进行处理。个人比较喜欢使用词型还原而不是词干提取。

在实际应用中，一般使用nltk来进行词干提取和词型还原。安装nltk也很简单，"pip install nltk"即可。只不过我们一般需要下载nltk的语料库，可以用下面的代码完成，nltk会弹出对话框选择要下载的内容。选择下载语料库就可以了。

    import nltk
    nltk.download()

在nltk中，做词干提取的方法有PorterStemmer，LancasterStemmer和SnowballStemmer。个人推荐使用SnowballStemmer。这个类可以处理很多种语言，当然，除了中文。

    from nltk.stem import SnowballStemmer
    stemmer = SnowballStemmer("english") # Choose a language
    stemmer.stem("countries") # Stem a word

输出是"countri",这个词干并不是一个词。　　　　

而如果是做词型还原，则一般可以使用WordNetLemmatizer类，即wordnet词形还原方法，Lemmatization 把一个任何形式的语言词汇还原为一般形式，标记词性的前提下效果比较好。

    from nltk.stem import WordNetLemmatizer
    wnl = WordNetLemmatizer()
    print(wnl.lemmatize('countries'))  

输出是"country",比较符合需求。在实际的英文文本挖掘预处理的时候，建议使用基于wordnet的词形还原就可以了。

在[这里](http://text-processing.com/demo/stem/)有个词干提取和词型还原的demo，如果是这块的新手可以去看看，上手很合适。

*PS：另一个demo：*[1](https://blog.csdn.net/panghaomingme/article/details/55210491)

    import nltk  
    sent1='The cat is walking in the bedroom.'  
    sent2='A dog was running across the kitchen.'  
    tokens_1=nltk.word_tokenize(sent1)  
    print (tokens_1)  
    stemmer = nltk.stem.PorterStemmer()  
    stem_1 = [stemmer.stem(t) for t in tokens_1]  
    print(stem_1) 

*又另一个demo：*[3](https://www.cnblogs.com/lemonding/p/5978946.html)

    def get_wordnet_pos(treebank_tag):
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

    def lemmatize_sentence(sentence):
        res = []
        lemmatizer = WordNetLemmatizer()
        for word, pos in pos_tag(word_tokenize(sentence)):
            wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
            res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
        return res

#### 2.2.5 Set All Characters to Lowercase 转化为小写

由于英文单词有大小写之分，我们期望统计时像“Home”和“home”是一个词。因此一般需要将所有的词都转化为小写。这个直接用python的API（.lower()）就可以搞定。

#### 2.2.6 Remove Stop Words 去除停用词

在英文文本中有很多无效的词，比如“a”，“to”，一些短词，还有一些标点符号，这些我们不想在文本分析的时候引入，因此需要去掉，这些词就是停用词。个人常用的英文停用词表下载地址在这。当然也有其他版本的停用词表，不过这个版本是我常用的。

在我们用scikit-learn做特征处理的时候，可以通过参数stop_words来引入一个数组作为停用词表。这个方法和前文讲中文停用词的方法相同，这里就不写出代码，大家参考前文即可。

    from nltk.corpus import stopwords   #去停用词
    cachedStopWords = stopwords.words("english")
    wordStoped = []
    for word in words:  #去停用词 words是分句分词后的句子级别处理结果
        filtered = [w for w in word if (w not in cachedStopWords)]
        wordStoped.append(filtered)

## 3. Data Exploration & Visualization 特征处理

现在我们就可以用scikit-learn来对我们的文本特征进行处理了，在文本挖掘预处理之向量化与Hash Trick中，我们讲到了两种特征处理的方法，向量化与Hash Trick。而向量化是最常用的方法，因为它可以接着进行TF-IDF的特征处理。在文本挖掘预处理之TF-IDF中，我们也讲到了TF-IDF特征处理的方法。


TfidfVectorizer类可以帮助我们完成向量化，TF-IDF和标准化三步。当然，还可以帮我们处理停用词。这部分工作和中文的特征处理也是完全相同的，大家参考前文即可。

## 4. Model Building & Evaluation 建立分析模型

有了每段文本的TF-IDF的特征向量，我们就可以利用这些数据建立分类模型，或者聚类模型了，或者进行主题模型的分析。此时的分类聚类模型和之前讲的非自然语言处理的数据分析没有什么两样。因此对应的算法都可以直接使用。

## Reference

[英文文本挖掘预处理流程总结][1]
[A General Approach to Preprocessing Text Data][2]

[1]: http://www.cnblogs.com/pinard/p/6756534.html/ "英文文本挖掘预处理流程总结"
[2]: https://www.kdnuggets.com/2017/12/general-approach-preprocessing-text-data.html "A General Approach to Preprocessing Text Data"

# Part3: 基于朴素贝叶斯+Python实现垃圾邮件分类

## 朴素贝叶斯原理

请参考： [贝叶斯推断及其互联网应用（二）：过滤垃圾邮件](http://www.ruanyifeng.com/blog/2011/08/bayesian_inference_part_two.html)

## Python实现

源代码主干来自： [python实现贝叶斯推断——垃圾邮件分类](https://blog.csdn.net/AlanConstantineLau/article/details/71694660?ref=myread)

我只是加了注释，然后做了对结果的分析统计的输出添加。

源码下载： [GitHub：下载NaiveBayesEmail.py](https://github.com/Galo27/Text-Mining-Practice)

本文原载： [基于朴素贝叶斯+Python实现垃圾邮件分类](https://blog.csdn.net/Galoa/article/details/79871992)
