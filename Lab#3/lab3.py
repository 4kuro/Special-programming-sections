from spyre import server
import os
import glob

import pandas as pd
import matplotlib.pyplot as plt

#допоміжна функція для додавання індексу регіона у фрейм
def get_region_idex(full_path, directory_path):
    fragment = full_path[len(directory_path) + 8:]
    return int(fragment[:fragment.index('_')])

#функція читання даних
def read_data(directory_path='data'):
    dfs = []
    for path in glob.glob(os.path.join(os.path.dirname(__file__), directory_path, '*.csv')):
        df = pd.read_csv(path, index_col=False)
        df['region_index'] = get_region_idex(path, os.path.join(os.path.dirname(__file__), directory_path))
        df.rename(columns={' SMN': 'SMN', ' VHI': 'VHI'}, inplace=True)
        df = df[df['VHI'] != -1]
        dfs.append(df)
    return pd.concat(dfs)

#читаємо дані
df = read_data()

# об'єкт, де ключами є номера областей, а значеннями - їх назви
indexes_to_names = {
    1: 'Черкаська',
    2: 'Чернігівська',
    3: 'Чернівецька',
    4: 'Республіка Крим',
    5: 'Дніпропетровська',
    6: 'Донецька',
    7: 'Івано-Франківська',
    8: 'Харківська',
    9: 'Херсонська',
    10: 'Хмельницька',
    11: 'Київська',
    12: 'Місто Київ',
    13: 'Кіровоградська',
    14: 'Луганська',
    15: 'Львівська',
    16: 'Миколаївська',
    17: 'Одеська',
    18: 'Полтавська',
    19: 'Рівенська',
    20: 'Севастополь',
    21: 'Сумська',
    22: 'Тернопільська',
    23: 'Закарпатська',
    24: 'Вінницька',
    25: 'Волинська',
    26: 'Запорізька',
    27: 'Житомирська',
}

#функція, що додає назви областей
def add_region_names(df, names_obj):
    df['region_name'] = df['region_index'].map(lambda id: names_obj[id])

#додаємо назви областей
add_region_names(df, indexes_to_names)

#функція вибірки даних за заданими параметрами
def filter(params):
    return df[params['index']][(df['region_name'] == params['region_name']) & (df['week'] >= int(params['first_week'])) & (df['week'] <= int(params['last_week']))]

class MyApp(server.App):
    title = 'Лабораторна робота 2'

    inputs = [{
        'type': 'dropdown',
        'label': 'Індекс',
        'options': [{'label': column, 'value': column} for column in df.columns[2:7]],
        'key': 'index',
        'id': 'updateAll',
        'action_id': 'text_output'
    },
    {
        'type': 'dropdown',
        'label': 'Область',
        'options': [{'label': region_name, 'value': region_name} for region_name in df['region_name'].unique()],
        'key': 'region_name',
        'id': 'updateAll',
        'action_id': 'text_output'
    },
    {
        'type': 'text',
        'label': 'Тижні з',
        'value': '1',
        'key': 'first_week',
        'id': 'updateAll',
        'action_id': 'text_output'
    },
    {
        'type': 'text',
        'label': 'по',
        'value': '10',
        'key': 'last_week',
        'id': 'updateAll',
        'action_id': 'text_output'
    },]

    controls = [{
        'type': 'hidden',
        'id': 'text_output'
    }]

    outputs = [{
        'type': 'html',
        'control_id': 'text_output',
        'id': 'updateAll',
        'tab': 'Table'
    },
    {
        'type': 'table',
        'id': 'table_id',
        'control_id': 'text_output',
        'tab': 'Table'
    },
    {
        "type" : "plot",
        "id" : "plot",
        "control_id" : "text_output",
        "tab" : "Plot"
    }]

    tabs = ['Table', 'Plot']

    def updateAll(self, params):
        data = filter(params)
        return f'<P>Максимальне значення: {data.max()}</P><P>Мінімальне значення: {data.min()}</P>'
    
    def getData(self, params):
        return pd.DataFrame(filter(params))
    
    def getPlot(self, params):
        data = self.getData(params)
        _, ax = plt.subplots()
        ax.plot(range(len(data)), data)
        return ax

app = MyApp()
app.launch(port=9092)