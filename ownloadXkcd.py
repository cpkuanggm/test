#! python3
# downloadXkcd.py - Downloads every single XKCD comic.
import requests, os, bs4
'''
利用requests 模块下载页面。
• 利用Beautiful Soup 找到页面中漫画图像的URL。
• 利用iter_content()下载漫画图像，并保存到硬盘。
• 找到前一张漫画的链接URL，然后重复。
'''
url = 'https://www.fzdm.com/manhua/132//173/' # starting url
os.makedirs('fzdm', exist_ok=True) # store comics in ./xkcd
while not url.endswith('#'):
    '''
    漫画图像文件的URL，由一个<img>元素的href 属性给出。
    • <img>元素在<div id="comic">元素之内。
    • Prev 按钮有一个rel HTML 属性，值是prev。
    • 第一张漫画的Prev 按钮链接到http://xkcd.com/# URL，表明没有前一个页面了
    '''
    # TODO: Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    # TODO: Find the URL of the comic image.
    comicElem = soup.select('#mhimg0')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = comicElem[0].get('src')
        print(comicUrl)
    # Download the image.
    print('Downloading image %s...' % (comicUrl))
    res = requests.get(comicUrl)
    res.raise_for_status()
    # TODO: Save the image to ./xkcd.
    imageFile = open(os.path.join('fzdm', os.path.basename(comicUrl)), 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    # TODO: Get the Prev button's url.
    nextLink = soup.select('a[class="pure-button pure-button-primary"]')[0]
    url = 'https://www.fzdm.com/manhua/132//173/' + nextLink.get('href')
print("done")