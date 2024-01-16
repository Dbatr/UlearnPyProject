import pandas as pd
from dateutil import parser
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def parse_date(date_str):
    try:
        return parser.parse(date_str)
    except:
        return pd.Na

def process_skills(df):
    df['key_skills'] = df['key_skills'].str.replace(',', '\n')
    df['key_skills'] = df['key_skills'].str.split('[\n]+')
    df = df.explode('key_skills')  # Разделение строк с массивами в отдельные строки
    df['key_skills_str'] = df['key_skills'].str.strip()
    df['published_at'] = df['published_at'].apply(parse_date)
    df['year'] = df['published_at'].dt.year
    return df

# python manage.py runscript parse_skills -v2
def run():
    df = pd.read_csv('vacancies.csv')
    df = df.dropna(subset=['key_skills'])

    num_processes = multiprocessing.cpu_count()  # Используйте количество доступных ядер процессора
    chunks = [df.iloc[i::num_processes, :] for i in range(num_processes)]

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        processed_dfs = list(executor.map(process_skills, chunks))

    df_processed = pd.concat(processed_dfs)
    df_filtered = df_processed[(df_processed['year'] >= 2003) & (df_processed['year'] <= 2023)]

    skills_count_by_year = df_filtered.groupby(['year', 'key_skills_str']).size().reset_index(name='count')
    top_skills_by_year = skills_count_by_year.groupby('year').apply(lambda x: x.nlargest(20, 'count')).reset_index(
        drop=True)

    top_skills_by_year.to_csv('top_skills_by_year.csv', index=False)
    print(top_skills_by_year)