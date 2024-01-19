import os
from django.conf import settings

import pandas as pd
import matplotlib.pyplot as plt


# python manage.py runscript top_skills_img -v2
def run():
    # Создание DataFrame из данных
    df = pd.read_csv('all_skils_graph.csv')

    # Построение графика
    plt.figure(figsize=(10, 6))

    # Группировка данных по навыку для каждого года
    grouped = df.groupby(['Year', 'Skill']).sum().unstack()
    lines = grouped.plot(kind='line', marker=None, linestyle='-')

    # Настройка отображения
    plt.title('Рост самых популярных навыков 2023 года')
    plt.xlabel('Год')
    plt.ylabel('Количество упоминаний')

    # Установка собственных названий для легенды
    lines.legend(title='Навык', labels=grouped.columns.get_level_values('Skill'))

    plt.tight_layout()

    # Сохранение графика как изображение
    plt.savefig(os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img','top_skills_graph.png'))
