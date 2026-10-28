from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
p=root/'index.html'
s=p.read_text(encoding='utf-8')
social=''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{label}"><img src="assets/icons/{icon}.svg" alt="" width="40" height="40"></a>' for icon,label,url in [('telegram','Телеграм','https://t.me/acaffe2022'),('whatsapp','WhatsApp','https://wa.me/79519308831'),('vk','ВКонтакте','https://vk.ru/acaffeperm2023'),('maps','Яндекс Карты','https://yandex.com/maps/org/acaffe_lounge/69147270460/')])
s=s.replace('Контакты</a></nav>',f'Контакты</a><div class="nav-social" aria-label="Социальные сети и карта">{social}</div></nav>',1)
s=s.replace('<span class="spark" aria-hidden="true">✳</span> Ресторан · Пермь','Acaffe Lounge · Ресторан · Пермь')
s=s.replace('Хороший вечер.<br>В хорошей<br><em>компании.</em>','РЕСТОРАН<br>И ЛАУНЖ-БАР<br><em>В ЦЕНТРЕ ПЕРМИ</em>')
s=s.replace('Ресторан и лаунж-бар в центре Перми.<br>Европейская и японская кухня — для обеда,<br class="desktop-break"> ужина и встреч с близкими.','Европейская и японская кухня.<br>Обеды, ужины и встречи с близкими.')
s=re.sub(r'    <div class="shortcuts wrap".*?</div>\s*','',s,count=1,flags=re.S)
s=s.replace('У вечера есть<br><em>своё настроение.</em>','Пространство<br><em>Acaffe Lounge</em>')
card='<figure class="gallery-card"><a href="assets/images/exterior.webp" data-gallery data-caption="Фасад Acaffe Lounge и озеленённая летняя веранда" aria-label="Увеличить фото: Фасад и летняя веранда"><img src="assets/images/exterior.webp" alt="Фасад Acaffe Lounge и озеленённая летняя веранда" width="853" height="1280" loading="lazy"><span class="photo-open" aria-hidden="true">↗</span></a><figcaption><span>04</span>Летняя веранда</figcaption></figure>'
s=s.replace('03</span>Вечер в Acaffe</figcaption></figure></div>','03</span>Вечер в Acaffe</figcaption></figure>'+card+'</div>')
s=s.replace('Разговор начинается<br><em>с хорошего ужина.</em>','Наше <em>меню</em>')
s=s.replace('<span class="tag">Планы на вечер</span><p class="section-index">04 / Бронирование</p>','<p class="section-index">04 / Бронирование</p>')
s=s.replace('Осталось выбрать<br><em>компанию.</em>','ВАШ СТОЛ<br><em>В ACAFFE</em>')
s=s.replace('<a class="booking-phone" href="tel:+79519308831">+7 (951) 930-88-31</a>','<p class="booking-note">Выберите день. Пригласите близких.<br>Остальное обсудим по телефону.</p>')
s=s.replace('<section class="services wrap" aria-labelledby="services-title"><div class="services-intro"><span class="tag">Ещё один повод</span><h2 id="services-title">Для вашей встречи</h2><p class="services-note">Собирайте тех,<br>с кем хорошо.</p></div>','<section class="services wrap" aria-label="Услуги ресторана">')
s=s.replace('В ресторане предусмотрен банкетный зал. Вместимость и условия вашего события уточните по телефону.','Семейный праздник, встреча с коллегами или корпоратив — в ресторане предусмотрен банкетный зал. Вместимость и условия обсудим по телефону.')
start=s.index('      <div class="section-top">',s.index('id="contacts"'))
end=s.index('      <div class="map-panel">',start)
old=s[start:end]
hours=re.search(r'<div class="hours-block">.*?</div>',old,re.S).group().replace('Время для встречи','Часы работы')
links=re.search(r'<div class="social-block">.*?</div>',old,re.S).group().replace('<span class="mini-label">Остаёмся на связи</span>','').replace('Ватсап','WhatsApp')
s=s[:start]+'''      <div class="section-heading"><h2 id="contacts-title">Контакты</h2><span class="section-index">05 / Acaffe Lounge</span></div>
      '''+links+'''
      <div class="contact-details"><div class="address-block"><span class="mini-label">Наш адрес</span><address>Пермь,<br>улица Газеты Звезда, 24</address><a class="text-link" href="https://yandex.com/maps/org/acaffe_lounge/69147270460/" target="_blank" rel="noopener noreferrer">Построить маршрут ↗</a></div>'''+hours+'</div>\n'+s[end:]
s=re.sub(r'  <footer.*?</footer>','  <a class="back-to-top" href="#home" aria-label="Вернуться наверх" hidden><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M12 19V5m-6 6 6-6 6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>',s,flags=re.S)
p.write_text(s,encoding='utf-8')
p=root/'js/main.js'
s=p.read_text(encoding='utf-8').replace("  const footer = document.querySelector('footer');\n",'').replace('    footer.inert = open;','    document.querySelector(\'.back-to-top\').inert = open;')
s=s.replace("const target = document.getElementById(link.getAttribute('href').slice(1));","const href = link.getAttribute('href');\n      const target = href.startsWith('#') ? document.getElementById(href.slice(1)) : null;")
s=s.replace('more.hidden = !selected || groupCards.length <= limit;','more.hidden = !selected || groupCards.length <= 4;')
s=s.replace("more.textContent = `Посмотреть все ${categoryLabels[name] || name.toLocaleLowerCase('ru')} (${groupCards.length})`;","more.textContent = expandedCategories.has(name) ? 'Показать меньше' : `Посмотреть все ${categoryLabels[name] || name.toLocaleLowerCase('ru')} (${groupCards.length})`;")
s=s.replace('    expandedCategories.add(group.dataset.menuCategory);','    const name = group.dataset.menuCategory;\n    const collapsing = expandedCategories.has(name);\n    if (collapsing) expandedCategories.delete(name);\n    else expandedCategories.add(name);')
s=s.replace('    if (firstNewCard) {','    if (collapsing) group.querySelector(\'.menu-more\').focus();\n    if (!collapsing && firstNewCard) {')
s=s.replace('  filterMenu();\n\n  const gallery', '''  filterMenu();

  const backToTop = document.querySelector('.back-to-top');
  function updateBackToTop() { backToTop.hidden = window.scrollY < 400; }
  window.addEventListener('scroll', updateBackToTop, {passive:true});
  backToTop.addEventListener('click', () => {
    const home = document.querySelector('#home');
    home.tabIndex = -1;
    home.focus({preventScroll:true});
  });
  updateBackToTop();

  const gallery''')
p.write_text(s,encoding='utf-8')
