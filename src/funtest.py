# -*- coding: utf-8 -*-
import requests
from lxml import etree

url = 'http://cstc.hrbeu.edu.cn/bzrgz/list.htm'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}
page = requests.get(url=url, headers=headers)
page.encoding = 'utf-8'
page = page.text

tree = etree.HTML(page)  # 创建一个etree实例对象

tableText = tree.xpath('//table//text()')
tableStr = ",".join(tableText)
# print(tableStr)


ele = tree.xpath('//script | //noscript | //style | //footer | //head | //table')
for e in ele:
    e.getparent().remove(e)

content = tree.xpath('string(.)')
content = content + tableStr

content = content.replace('\n', '')
content = content.replace('\r', '')
content = content.replace('\t', '')
content = content.replace('\xa0', '')
content = content.replace('\u3000', '')
content = content.replace(' ', '')

print(content)
