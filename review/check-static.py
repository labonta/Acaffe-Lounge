"""Необязательная проверка готовых файлов стандартной библиотекой Python."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent
void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.assets=[]; self.errors=[]; self.stack=[]; self.h1=0; self.cards=[]; self.meta={}
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag not in void: self.stack.append(tag)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='h1': self.h1+=1
        if tag=='a': self.links.append(attrs.get('href',''))
        if tag in ('img','script') and attrs.get('src'): self.assets.append(attrs['src'])
        if tag=='link' and attrs.get('href'): self.assets.append(attrs['href'])
        if tag=='meta': self.meta[attrs.get('name','')]=attrs.get('content','')
        if tag=='article' and 'dish' in attrs.get('class','').split(): self.cards.append(attrs)
        if tag=='img' and 'alt' not in attrs: self.errors.append('Изображение без alt')
    def handle_endtag(self,tag):
        if not self.stack or self.stack[-1]!=tag: self.errors.append('Нарушено закрытие тега '+tag)
        else: self.stack.pop()

page=Page(); page.feed((root/'index.html').read_text(encoding='utf-8'))
assert not page.errors, page.errors
assert not page.stack, page.stack
assert page.h1==1
assert len(page.ids)==len(set(page.ids))
assert page.meta['robots']=='noindex, nofollow'
for link in page.links:
    if link.startswith('#'): assert link[1:] in page.ids, link
for asset in page.assets:
    assert not urlsplit(asset).scheme and not asset.startswith('/'), asset
    assert (root/unquote(urlsplit(asset).path)).is_file(), asset
    assert '/example-project/' in urljoin('https://example.invalid/example-project/index.html',asset),asset
    assert (root/unquote(urlsplit(asset).path)).stat().st_size>0,asset
assert (root/'.nojekyll').is_file() and (root/'.nojekyll').stat().st_size==0
source=json.loads((root/'review/menu-source.json').read_text(encoding='utf-8'))
assert len(page.cards)==len(source)==22
for category,name,price,weight,image,description in source:
    found=[c for c in page.cards if c['data-search']==name+' '+description]
    assert len(found)==1,name
    assert found[0]['data-category']==category,name
photos=json.loads((root/'review/menu-photo-sources.json').read_text(encoding='utf-8'))
assert len(photos)==22
for photo in photos:
    assert (root/photo['file']).is_file(),photo['file']
    assert photo['file'] in [urlsplit(asset).path for asset in page.assets],photo['file']

def luminance(hex_value):
    c=[int(hex_value[i:i+2],16)/255 for i in (0,2,4)]
    c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c]
    return sum(v*w for v,w in zip(c,(.2126,.7152,.0722)))
def contrast(a,b):
    x,y=sorted([luminance(a),luminance(b)])
    return round((y+.05)/(x+.05),2)
ratios={name:contrast(fg,bg) for name,fg,bg in [('Основной текст / кремовый','29130f','fff4dc'),('Вторичный текст / кремовый','71594c','fff4dc'),('Красный текст / кремовый','b83124','fff4dc'),('Кремовый / бордовый','fff4dc','2b0504'),('Кремовый / красная кнопка','fff4dc','b83124')]}
assert min(ratios.values())>=4.5
result={'результат':'успешно','h1':page.h1,'уникальных_id':len(page.ids),'локальных_подключений':len(page.assets),'блюд':len(page.cards),'проверка_пути_подкаталога':'статически, без публичной публикации','контраст':ratios}
(root/'review/static-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
