# 酷狗音乐下载器
# 下载酷狗音乐能够在线播放的音乐
"""
搜索的链接：
    http://songsearch.kugou.com/song_search_v2?keyword={（我们需要搜索的数据）}&page=1&pagesize=30

    http://songsearch.kugou.com/song_search_v2?callback=jQuery112409354210535219736_1540378164582&keyword=%E7%A9%BA%E7%A9%BA%E5%A6%82%E4%B9%9F&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1
下载的链接
    http://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19106161310636088968_1540379305130&hash=5C1BB55CCD20F85AA9816DAA7649BDEF&album_id=8114346&_=1540379305131
    
    http://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={需要我们传入hash值,不能手动添加}
    # 5C1BB55CCD20F85AA9816DAA7649BDEF
    
"""
import requests
import json
import re
import os


class Download():
    def __init__(self):
        self.search_url = 'http://songsearch.kugou.com/song_search_v2?keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1'
        self.hash_url = 'http://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }

    def run(self,keyword,num=1):
        result = requests.get(self.search_url.format(keyword),headers = self.headers)
        # print(result.text)
        # print(result)
        dic = json.loads(result.text)
        # print(dic)
        songlist = dic['data']['lists']
        # print(songlist[0])
        if num > len(songlist):
            print('歌曲数量为%d'%len(songlist))
            num = len(songlist)
        # 获取hash
        filehash = re.findall('"FileHash":"(.*?)"',result.text)
        # print(filehash[0])
        # 获取歌曲名
        songname = re.findall('"SongName":"(.*?)"',result.text)
        # print(songname)

        # 保存的路径
        if not os.path.exists('./MP3'):
            os.mkdir('./MP3')
        # 歌曲的名字
        names = []
        for n in range(num):
            name = songname[n].replace("<\\/em>","").replace("<em>","")+'.mp3'
            if name in names:
                name = str(n)+name
                names.append(name)
            
        content = requests.get(self.hash_url.format(filehash[num-1]))
        url = re.findall('"play_url":"(.*?)"',content.text)[0]
        # 真正的下载地址
        dowload_url = url.replace("\\","")
        # print(dowload_url)
        # 写入文件
        with open('./MP3/{}'.format(name),'wb') as f:
            f.write(requests.get(dowload_url).content)
        print('歌曲已经下载完成')

keyword = input('请输入歌曲的名字:')
songnum = int(input('输入需要下载的歌曲序号:'))
loader = Download()
loader.run(keyword,songnum)
