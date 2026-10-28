from pathlib import Path
import json
r=Path(__file__).resolve().parent.parent
p=r/'index.html'; s=p.read_text(encoding='utf-8')
start=s.index('<figure class="gallery-card"><a href="assets/images/exterior.webp"')
end=s.index('</figure>',start)+len('</figure>')
card=s[start:end].replace('exterior.webp','terrace.jpg').replace('width="853" height="1280"','width="1024" height="768"')
s=s[:start]+card+s[end:]
p.write_text(s,encoding='utf-8')
p=r/'docs/menu-photo-sources.json'; data=json.loads(p.read_text(encoding='utf-8-sig'))
for photo in data:
    if photo['file'] in ('assets/images/dish-13.jpg','assets/images/dish-14.jpg'):
        photo['source']=photo['source'].replace('/M_height','/orig')
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (r/'CONTENT_SOURCES.md').open('a',encoding='utf-8') as f:
    f.write('''

## Четвёртая редакция — 28 октября 2026 года

По просьбе пользователя удалены короткие переходы и футер, упрощены заголовки и контакты. Меню: максимум три колонки, одиночные блюда имеют ту же ширину, категории с более чем четырьмя блюдами раскрываются и сворачиваются отдельно. Бронирование сохраняет телефонную кнопку.

Повторно просмотрены обзор и фотогалерея организации 69147270460. В особенностях явно перечислены «Корпоратив», «Банкет», «Семейный ужин» и «Летняя веранда»; добавлено упоминание корпоративной встречи без обещания вместимости или условий. Завтраки не добавлены: тематические подборки и отзывы не подтверждают действующее предложение и расписание завтраков.

Новая фотография: `assets/images/terrace.jpg` — вход и озеленённая летняя веранда, просмотрена в галерее «Снаружи», снимок 5 из 11, автор «Яндекс», август 2024. Ресурс: https://avatars.mds.yandex.net/get-altay/10767436/2a00000191c4a3186fa69f07e2f05e3becc1/XXXL . Разрешение на коммерческое использование отдельно не установлено; сохраняются ограничения остальных фотографий.

Для `dish-13.jpg` и `dish-14.jpg` загружены версии `/orig` тех же фотографий блюд вместо уменьшенных `/M_height`; точные ссылки обновлены в `docs/menu-photo-sources.json`. Фотографии не генерировались и не подменялись другими блюдами.
''')
