from pathlib import Path
import shutil
root=Path(__file__).resolve().parent.parent
docs=root/'docs';docs.mkdir(exist_ok=True)
for name in ['menu-source.json','menu-photo-sources.json']:
    shutil.copyfile(root/'review'/name,docs/name)
p=root/'CONTENT_SOURCES.md';s=p.read_text(encoding='utf-8')
s=s.replace('review/menu-source.json','docs/menu-source.json').replace('review/menu-photo-sources.json','docs/menu-photo-sources.json')
p.write_text(s,encoding='utf-8')
p=root/'README.md';s=p.read_text(encoding='utf-8')
s=s.replace('Публичная публикация не выполнялась.','Репозиторий демонстрации: https://github.com/labonta/Acaffe-Lounge .')
s=s.replace('review/menu-source.json','docs/menu-source.json')
s=s.replace('## Позднее размещение на GitHub Pages','## Размещение на GitHub Pages')
s=s.replace('Публикация — отдельный шаг, после вашего явного разрешения и выбора репозитория.','Публикация выполняется по запросу пользователя в репозиторий `labonta/Acaffe-Lounge`. Источник GitHub Pages — ветка `main`, папка `/ (root)`. Установка зависимостей и компиляция не требуются.')
s=s.replace('В корень будущего репозитория поместить','В корне репозитория находятся')
s=s.replace('Пути относительные и рассчитаны на адрес вида `https://<владелец>.github.io/<репозиторий>/`. Учётная запись, домен и репозиторий в коде не зафиксированы.','Пути относительные и работают под каталогом проекта GitHub Pages. Учётная запись, домен и репозиторий в коде страницы не зафиксированы. Последующие изменения публикуются обновлением файлов в ветке `main`.')
s=s.replace('См. `review/VERIFICATION.md`.','Пройдены статические проверки разметки, локальных путей, 22 блюд и синтаксиса JavaScript. В браузере проверены категории, раскрытие блюд, галерея, мобильное меню и раскладки 375, 768, 1440 пикселей. Отчёты и скриншоты хранятся локально и в репозиторий не включены.')
s=s.replace('`review/responsive.html` — служебная страница проверки ширин 375, 768 и 1440 пикселей. Для просмотра основного сайта она не требуется.','Архив названий, цен, весов и точные источники фотографий находятся в `docs/`. Служебные страницы проверки и первоначальное задание исключены из публикации.')
p.write_text(s,encoding='utf-8')
