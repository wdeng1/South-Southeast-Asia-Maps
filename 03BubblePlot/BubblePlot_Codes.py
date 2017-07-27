import plotly.plotly as py
from plotly.grid_objs import Grid, Column
from plotly.tools import FigureFactory as figure_factory

import pandas as pd
import time

import plotly
import json
import requests
from requests.auth import HTTPBasicAuth

username = '...' # Replace with YOUR USERNAME
api_key = '...' # Replace with YOUR API KEY

auth = HTTPBasicAuth(username, api_key)
headers = {'Plotly-Client-Platform': 'python'}

plotly.tools.set_credentials_file(username=username, api_key=api_key)
dataset = pd.read_excel("SLA_electoral.xls")

dataset.head()
table = figure_factory.create_table(dataset.head(10))
py.iplot(table, filename='animations-gapminder-data-preview')

years_from_col = set(dataset['year'])
years_ints = sorted(list(years_from_col))
years = [str(year) for year in years_ints]

# make list of continents
provinces = []
for province in dataset['province']:
    if province not in provinces:
        provinces.append(province)

columns = []
# make grid
for year in years:
    for province in provinces:
        dataset_by_year = dataset[dataset['year'] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[dataset_by_year['province'] == province]
        for col_name in dataset_by_year_and_cont:
            # each column name is unique
            column_name = '{year}_{province}_{header}_gapminder_grid'.format(
                year=year, province=province, header=col_name
            )
            a_column = Column(list(dataset_by_year_and_cont[col_name]), column_name)
            columns.append(a_column)

# upload grid
grid = Grid(columns)
url = py.grid_ops.upload(grid, 'gapminder_grid'+str(time.time()), auto_open=False)
url

figure = {
    'data': [],
    'layout': {},
    'frames': [],
    'config': {'scrollzoom': True}
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': [-10, 150], 'title': 'SLA Fatalities', 'gridcolor': '#FFFFFF'}
figure['layout']['yaxis'] = {'range': [-10, 100], 'title': 'Electoral Turnout (%)', 'gridcolor': '#FFFFFF'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['plot_bgcolor'] = 'rgb(223, 232, 243)'

figure['layout']['slider'] = {
    'args': [
        'slider.value', {
            'duration': 400,
            'ease': 'cubic-in-out'
        }
    ],
    'initialValue': 'first-value-for-slider',
    'plotlycommand': 'animate',
    'values': [1988, 1989, 1994, 1999],
    'visible': True
}

figure['layout']['slider'] = {
    'args': [
        'slider.value', {
            'duration': 400,
            'ease': 'cubic-in-out'
        }
    ],
    'initialValue': '1988',
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}

figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

figure['layout']['sliders'] = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'text-before-value-on-display',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': [{
    'args': [
        [1988],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
         'transition': {'duration': 300}}
    ],
    'label': "Year: 1988",
    'method': 'animate'
}]
}

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

custom_colors = {
    'Eastern': 'rgb(51, 153, 255)',
    'Central': 'rgb(255, 51, 255)',
    'Northern': 'rgb(153, 51, 255)',
    'North Central': 'rgb(102, 178, 255)',
    'Western': 'rgb(204, 153, 255)',
    'Sabaragamuwa': 'rgb(255, 153, 255)',
    'North Western': 'rgb(255, 102, 255)',
    'Southern': 'rgb(178, 102, 255)',
    'Uva': 'rgb(153, 204, 255)'
}

col_name_template = '{year}_{province}_{header}_gapminder_grid'
year = 1988
for province in provinces:
    data_dict = {
        'xsrc': grid.get_column_reference(col_name_template.format(
            year=year, province=province, header='deaths'
        )),
        'ysrc': grid.get_column_reference(col_name_template.format(
            year=year, province=province, header='turnout'
        )),
        'mode': 'markers',
        'textsrc': grid.get_column_reference(col_name_template.format(
            year=year, province=province, header='district'
        )),
        'marker': {
            'sizemode': 'area',
            'sizeref': 1.5,
            'sizesrc': grid.get_column_reference(col_name_template.format(
                 year=year, province=province, header='regvoter'
            )),
            'color': custom_colors[province]
        },
        'name': province
    }
    figure['data'].append(data_dict)

frame = {'data': [], 'name': "1988"}

figure['layout']['sliders'] = [sliders_dict]

for year in years:
    frame = {'data': [], 'name': str(year)}
    for province in provinces:
        data_dict = {
            'xsrc': grid.get_column_reference(col_name_template.format(
                year=year, province=province, header='deaths'
            )),
            'ysrc': grid.get_column_reference(col_name_template.format(
                year=year, province=province, header='turnout'
            )),
            'mode': 'markers',
            'textsrc': grid.get_column_reference(col_name_template.format(
                year=year, province=province, header='district'
                )),
            'marker': {
                'sizemode': 'area',
                'sizeref': 1.5,
                'sizesrc': grid.get_column_reference(col_name_template.format(
                    year=year, province=province, header='regvoter'
                )),
                'color': custom_colors[province]
            },
            'name': province
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': year,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

figure['layout']['sliders'] = [sliders_dict]

graph = py.icreate_animations(figure, 'SLA_fatalities_turnout'+str(time.time()))
graph
