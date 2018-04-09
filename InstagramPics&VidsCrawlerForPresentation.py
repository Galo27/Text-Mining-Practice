import os
import requests
import json
import re
from contextlib import closing

# 起个名字
user_name = 'Galo'
# HTTP请求中找的
user_id = 2158725
media_after = 'AQCN46TlLBVMhGaf7xrr_i4Jc4KaqbzH2IN_-EM0j-XbSjmYpByx_kpMPVHyoQV2t64sXopRP_zX0LMr83ufqr4rvKRksXp1IDRaSSpLptUEnw'
query_id = 1521636438

img_links = []
video_links = []
i = 1
j = 1
k = 1

headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/yuyanpeng/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
    "Host": "www.instagram.com"}

# 先创建两个文件夹
if os.path.isdir(user_name + '_images'):
    print('已有images文件夹')
else:
    os.makedirs(user_name + '_images')
    print('创建了images文件夹')

if os.path.isdir(user_name + '_videos'):
    print('已有videos文件夹')
else:
    os.makedirs(user_name + '_videos')
    print('创建了videos文件夹')


# # 保存链接的函数，不要了，直接写在下边吧。
# # 这样一行行的写入，底下是直接报links列表组合一下，一起写
# def save_image_links(links):
#     with open('images.txt', 'w') as f:
#         for link in links:
#             f.write(link + '\n')
#     print('共保存了' + str(len(links)) + '张图片。')


# def save_video_links(links):
#     with open('videos.txt', 'w') as f:
#         for link in links:
#             f.write(link + '\n')
#     print('共保存了' + str(len(links)) + '个视频。')


def find_video_url(video_code):
    # 通过node的code先生成查找视频的HTTP请求url
    # 貌似video_code对了就行了，后边跟的查询字符不是必须的。爬梅西的视频时忘改了，但还是正确的爬下来了
    query_video_url = 'https://www.instagram.com/p/'+ video_code +'/?taken-by=yuyanpeng'
    # 发送请求，get方法
    video_r = requests.get(query_video_url, headers=headers)
    # 返回的数据仍是json格式的，与下边整体数据的加载类似
    #返回不是json！！！！正则匹配下载链接
    videoReg = re.compile(r'content="(https://scon.+?/vp/.+?\.mp4)"')
    videoSource = re.findall(videoReg,video_r.text)
    # 视频的链接就在media下的video_url中
    #video_json_data_media = video_json_data['media']
    return videoSource[0]

res = requests.get('https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%7B%22id%22%3A%222158725%22%2C%22first%22%3A12%2C%22after%22%3A%22AQBjhIn0c9Aukpi7CZcidt81XmdjGDeIQKkvGUhLErS0ne-Ds-TG5IjH__DKhtjH7E1xR1kqZwXGZ1xLdrftI7ciT43sbGj-VkN-hYYmWzO1Xw%22%7D', headers=headers)
dic =json.loads(res.text)
data = dic['data']['user']['edge_owner_to_timeline_media']['edges']
cnt = 0
nodes = []
while cnt<=len(data)-1:
    nodes.append(data[int(cnt)]['node'])
    cnt+=1
end_cursor = dic['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
has_next_page = dic['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
lee_id = nodes[0]["owner"]["id"]  # '313386162'

for node in nodes:
    if not node['is_video']:
        link = node['display_url']
        if link and link not in img_links:
            print('找到了第' + str(i) + '张新的图。')
            img_links.append(node['display_url'])
            i = i + 1
    else:
        video_code = node['shortcode']
        # 根据若是视频，根据node的code去生成视频链接的HTTP请求url
        # 写成了函数find_video_url
        video_link = find_video_url(video_code)
        if video_link and video_link not in video_links:
            print('找到了第' + str(j) + '个新的视频。')
            video_links.append(video_link)
            j = j + 1
print('加载')



# 查询的url，不同数据的查询并不是通过url的不同来体现
url = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%7B%22id%22%3A%222158725%22%2C%22first%22%3A12%2C%22after%22%3A%22AQBjhIn0c9Aukpi7CZcidt81XmdjGDeIQKkvGUhLErS0ne-Ds-TG5IjH__DKhtjH7E1xR1kqZwXGZ1xLdrftI7ciT43sbGj-VkN-hYYmWzO1Xw%22%7D'

# query_video_url = 'https://www.instagram.com/p/2KrdZNpIxk/?taken-by=yejinhand&__a=1'



# 通过form data 来进行不同数据的查询。不同在after后的一串数字。
#query_data = {
#    'q': 'ig_user(' + str(user_id) + '){media.after(' + media_after + ', 12){nodes{code,display_src,id,is_video},page_info}}',
#    'ref': 'users::show',
#    'query_id': str(query_id)
#}


# 首先读取文件中的video_links和img_links，加入上边两个List中
# 打开文件时 只读方式 r
# 不对，应该用r+，读写，若文件不存在，创建文件
with open(user_name + '_videos' + '/videos.txt', 'r+') as f:
    for line in f.readlines():
        video_links.append(line.strip('\n'))

with open(user_name + '_images' + '/images.txt', 'r+') as f:
    for line in f.readlines():
        img_links.append(line.strip('\n'))

# 已经有的视频、图像连接
print('已有' + str(len(video_links)) + '个视频链接。')
print('已有' + str(len(img_links)) + '个图片链接。')

#while True:
while i<=2170:
    # 进行post请求。注意有个data项。即HTTP请求中的form data项。
    r = requests.get(url,headers=headers)
    # 返回的数据是json格式。用json库来解析。
    dic = json.loads(r.text)
    # dic现在就是一个字典，dict，有键有值。
    data = dic['data']['user']['edge_owner_to_timeline_media']['edges']
    cnt = 0
    nodes = []
    while cnt <= len(data)-1:
        nodes.append(data[int(cnt)]['node'])
        cnt += 1
    end_cursor = dic['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    has_next_page = dic['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
#    lee_id = nodes[0]["owner"]["id"]  # '313386162'

    for node in nodes:
        if not node['is_video']:
            link = node['display_url']
            if link and link not in img_links:
                print('找到了第' + str(i) + '张新的图。')
                img_links.append(node['display_url'])
                i = i + 1
        else:
            video_code = node['shortcode']
            # 根据若是视频，根据node的code去生成视频链接的HTTP请求url
            # 写成了函数find_video_url
            video_link = find_video_url(video_code)
            if video_link and video_link not in video_links:
                print('找到了第' + str(j) + '个新的视频。')
                video_links.append(video_link)
                j = j + 1

    # 有关下一页的信息在'json_data_media'中的page_info中
#    json_data_page_info = json_data_media['page_info']
    # 根据其中的has_next_page，可以判断有无下一页，更多的数据
    if has_next_page:
        # 下一页的HTTP请求url就是根据json_data_page_info中的end_cursor生成的
#        end_cursor = json_data_page_info['end_cursor']
#        new_q = 'ig_user(' + str(user_id) + '){media.after('+ end_cursor +', 12){nodes{code,display_src,id,is_video},page_info}}'
        # 修改成为查询下一页
        url = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%7B"id"%3A"2158725"%2C"first"%3A12%2C"after"%3A%22'+end_cursor+'%22%7D'
        print('######又加载了一页######')
        k = k + 1
    else:
        print('已经到头了。')
        break

# save_image_links(img_links)
# save_video_links(video_links)

# 此时写入是用的w，不能用a+否则就重复了
# 怎样一些写入一个列表
with open(user_name + '_images' + '/images.txt', 'w') as f:
    f.write('\n'.join(img_links) + '\n')

with open(user_name + '_videos' + '/videos.txt', 'w') as f:
    f.write('\n'.join(video_links) + '\n')

def downloadJPG(imgUrl,fileName):
    # 可自动关闭请求和响应的模块
    with closing(requests.get(imgUrl,stream = True)) as resp:
        with open(fileName,'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)

def downloadVID(vidUrl,fileName):
    # 可自动关闭请求和响应的模块
    with closing(requests.get(vidUrl,stream = True)) as resp:
        with open(fileName,'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)

cnt = 1
for imgurl in img_links:
    if imgurl != '':
        downloadJPG(imgurl, ''.join(['./Galo_images/', '{0}.jpg'.format(cnt)]))
    cnt+=1

cnt = 1
for vidurl in video_links:
    if vidurl != '':
        downloadVID(vidurl, ''.join(['./Galo_videos/', '{0}.MP4'.format(cnt)]))
    cnt+=1

print('完成！')
print('共进行了' + str(k) + '次的查询。')
print('共新增了视频' + str(j - 1) + '个。')
print('共新增了图片' + str(i - 1) + '张。')
# print(video_links)
print('现在共有' + str(len(video_links)) + '个视频。')
# print(img_links)
print('现在共有' + str(len(img_links)) + '张图片。')