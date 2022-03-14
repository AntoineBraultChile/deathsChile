import numpy as np
import pandas as pd
import json

data = pd.read_csv(
    'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones.csv')

years = [i for i in list(set(pd.to_datetime(
    data.iloc[:, 4:].columns, format='%Y-%m-%d').year)) if i > 2014]
years.sort()

dataSum = data.iloc[:, 4:].sum(axis=0)
deathsChile = pd.DataFrame({'date': dataSum.index, 'deaths': dataSum.values})

deathsChile['date'] = pd.to_datetime(deathsChile['date'], format='%Y-%m-%d')

deathsByYears = pd.pivot_table(deathsChile, index=deathsChile.date.dt.strftime(
    '%m-%d'), columns=deathsChile.date.dt.year, values='deaths')
deathsByYearsFrom2015 = deathsByYears.iloc[:, 5:].reset_index()

# # fill Febrary 29
# deathsByYearsFrom2015.loc[deathsByYearsFrom2015['date'] == '02-29', [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]] = deathsByYearsFrom2015.loc[deathsByYearsFrom2015['date'] == '02-28', [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]].values

output = {'Chile': {}}
for y in years:
    output['Chile'][y] = {'labels': (str(y)+'-'+deathsByYearsFrom2015['date']).values.tolist(
    ), 'values': deathsByYearsFrom2015[y].values.astype(str).tolist()}

with open('output/deathsChileFrom2015.json', 'w') as json_file:
    json.dump(output, json_file)
# deathsByYearsFrom2015.to_csv('./output/deathsChileFrom2015.csv', index=False)

region = data.Region.unique()
outputR = {}
for r in region:
    outputR[r] = {}
    dataSum = data[data['Region'] == r].iloc[:, 4:].sum(axis=0)
    deathsR = pd.DataFrame({'date': dataSum.index, 'deaths': dataSum.values})
    deathsR['date'] = pd.to_datetime(deathsR['date'], format='%Y-%m-%d')
    deathsRByYears = pd.pivot_table(deathsR, index=deathsR.date.dt.strftime(
        '%m-%d'), columns=deathsR.date.dt.year, values='deaths')
    deathsRByYearsFrom2015 = deathsRByYears.iloc[:, 5:].reset_index()
    for y in years:
        outputR[r][y] = {'labels': (str(y)+'-'+deathsRByYearsFrom2015['date']).values.tolist(
        ), 'values': deathsRByYearsFrom2015[y].values.astype(str).tolist()}


with open('output/deathsRegionsFrom2015.json', 'w') as json_file:
    json.dump(outputR, json_file)

deisComunaConfirmed = pd.read_csv(
    'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto50/DefuncionesDEIS_confirmadosPorComuna.csv')
deisRegionConfirmed = deisComunaConfirmed.groupby('Region').sum().iloc[:, 3:]

deisComunaSuspected = pd.read_csv(
    'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto50/DefuncionesDEIS_sospechososPorComuna.csv')
deisRegionSuspected = deisComunaSuspected.groupby('Region').sum().iloc[:, 3:]

deisRegionConfirmed.to_csv('output/deisRegionConfirmedDeaths.csv')
deisRegionSuspected.to_csv('output/deisRegionSuspectedDeaths.csv')

# print(deisRegionConfirmed)
# print(deisRegionSuspected)
# print(deisRegionConfirmed+deisRegionSuspected)

data.to_csv('./input/deathsByComunaInChile.csv')
