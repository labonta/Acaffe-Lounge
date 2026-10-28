from pathlib import Path
import re
r=Path(__file__).resolve().parent.parent
p=r/'index.html'
s=p.read_text(encoding='utf-8')
def arrow(path):
    return '<svg class="arrow-icon" aria-hidden="true" focusable="false" width="20" height="20" viewBox="0 0 24 24"><path d="'+path+'" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
s=s.replace('↗',arrow('M6 18 18 6M6 6h12v12')).replace('↓',arrow('M12 5v14m-6-6 6 6 6-6'))
start=s.index('      <div class="map-panel">')
end=s.index('</div>',start)+len('</div>')
map_html=s[start:end].strip().replace('width="1200" height="430"','width="520" height="300"')
s=s[:start]+s[end:]
address_start=s.index('<div class="contact-details">')
address_end=s.index('</a></div><div class="hours-block">',address_start)
s=s[:address_end]+s[address_end:].replace('</a></div><div class="hours-block">','</a>'+map_html+'</div><div class="hours-block">',1)
s=s.replace('css/refinements.css?v=4','css/refinements.css?v=5')
p.write_text(s,encoding='utf-8')
with (r/'css/refinements.css').open('a',encoding='utf-8') as f:
    f.write('''

/* SVG-стрелки не зависят от системного набора эмодзи. */
.arrow-icon { display:inline-block; width:20px; height:20px; flex:0 0 20px; vertical-align:middle; }
.button>span[aria-hidden],.hero-bottom a>span[aria-hidden],.about .text-link>span[aria-hidden],.social-block a>span[aria-hidden] { display:inline-flex; align-items:center; justify-content:center; line-height:1; }
.social-block .arrow-icon { width:16px; height:16px; }
.photo-open .arrow-icon { width:22px; height:22px; }
.contacts { padding-bottom:72px; }
.address-block .map-panel { width:100%; max-width:520px; margin:28px 0 0; border-radius:18px; }
.address-block .map-panel iframe { width:100%; height:300px; }
.contact-details { align-items:start; }
@media(max-width:650px) {
  .contacts { padding-bottom:44px; }
  .address-block .map-panel { max-width:100%; margin-top:24px; border-radius:16px; }
  .address-block .map-panel iframe { height:260px; }
}
''')
with (r/'README.md').open('a',encoding='utf-8') as f:
    f.write('\nВ пятой редакции текстовые стрелки заменены встроенными SVG: оформление не зависит от шрифта эмодзи устройства. Карта находится внутри адресного блока, ограничена шириной 520 px и высотой 300 px (на телефоне 260 px); внизу раздела добавлен отступ.\n')
