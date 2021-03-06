import base64
import json
import socket
import urllib.parse
import urllib.request

# v2ray订阅地址
subscribe_url = ''
hostname = 'pull.free.video.10010.com'
servername = ''
vmesscode = ''
pathname = '/v2ray'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def main():
    global vmesscode
    socket.setdefaulttimeout(5)  # 请求超时设置为5s
    req = urllib.request.Request(url=subscribe_url, headers=headers)
    return_content = urllib.request.urlopen(req).read()
    if len(return_content) % 3 == 1:
        return_content += b"="
    elif len(return_content) % 3 == 2:
        return_content += b"=="
    base64Str = base64.b64decode(return_content, '-_')
    share_links = base64Str.splitlines()  # \r\n进行分行
    add = ""
    for share_link in share_links:
        share_link = bytes.decode(share_link)  # 转换类型
        if share_link.find("vmess://") == -1:
            pass
        else:
            shar = share_link.split("ss://")
            jj = base64.urlsafe_b64decode(shar[1]).decode('UTF-8')  # 解析VMESS参数得到josn字符串 后面解析unicode
            par = json.loads(jj)  # 转换成字典
            par["ps"] = servername + par["ps"]
            par["host"] = hostname
            par["path"] = pathname
            dic = json.dumps(par)  # 转换成json
            dic1 = base64.b64encode(dic.encode('UTF-8'))  # 转换成base64字符串
            dic2 = 'vmess://' + bytes.decode(dic1) + "\r\n"  # 拼接vmess头
            add = add + dic2
    dic3 = base64.b64encode(add.encode('UTF-8'))
    vmesscode = dic3
    print(dic3.decode('utf8'))


if __name__ == '__main__':
    main()