import pandas as pd
import numpy as np

data = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones.csv')

dataSum = data.iloc[:,4:].sum(axis=0)
deathsChile=pd.DataFrame({'date':dataSum.index,'deaths':dataSum.values})

deathsChile['date'] = pd.to_datetime(deathsChile['date'], format = '%Y-%m-%d')

deathsByYears = pd.pivot_table(deathsChile, index=deathsChile.date.dt.strftime('%d-%m'), columns=deathsChile.date.dt.year, values='deaths')
deathsByYearsFrom2015 = deathsByYears.iloc[:,5:].reset_index()
deathsByYearsFrom2015.to_csv('./output/deathsChileFrom2015.csv', index=False)

data.to_csv('./input/deathsByComunaInChile.csv')