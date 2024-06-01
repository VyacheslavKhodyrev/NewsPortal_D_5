import requests
import lxml.html

url1 = 'https://ria.ru/20240509/putin-1944879815.html'
path1 = '//*[@id="endless"]/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div/text()'
head1 = '/html/head/title/text()'

url2 = 'https://ria.ru/20240510/kandidaty-1945057620.html'
path2 = '//*[@id="endless"]/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[3]/div[1]/div/text()'
head2 = '/html/head/title/text()'

url3 = 'https://ria.ru/20240510/burya-1945058169.html?rcmd_alg=COL6&rcmd_id=1945057620'
path3 = '//*[@id="endless"]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/div[3]/div[1]/div/text()'
head3 = '/html/head/title/text()'


def content(url, path, head):
    response = requests.get(url).content
    tree = lxml.html.document_fromstring(response)
    title = tree.xpath(head)
    text = tree.xpath(path)
    return title, text

title1, text1 = content(url1, path1, head1)

title2, text2 = content(url2, path2, head2)

title3, text3 = content(url3, path3, head3)

print(*title3)