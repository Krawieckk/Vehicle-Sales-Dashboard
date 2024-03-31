from dash import Dash, html, dcc, callback, Output, Input, ctx
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]

df = pd.read_csv('car_prices.csv').dropna()
df['state'] = df['state'].apply(lambda x: x.upper())


best_sellers = px.bar(df.make.value_counts()[0:10], title='Best selling manufacturers', labels=dict(make = 'Manufacturer', value='Sales')).update_layout(template='plotly_dark', title_x=.5, showlegend=False)
price_hist = px.histogram(df, x='sellingprice', title='Sale Price Histogram', labels=dict(sellingprice = 'Selling Price', count='Sales')).update_layout(template='plotly_dark', title_x=.5)
transmission_bar = px.bar(df, 'transmission')



app = Dash(
    __name__,
    external_scripts=external_script,
)

app.layout = html.Div(
    className='family-serif text-white text-sm bg-[#111111] overflow-hidden',
    children=[
        html.Div(
            children = [
                html.Div(
                    className='bg-[#222222] text-center p-6 flex flex-col gap-2',
                    children=[
                        html.H1(children='Vehicle Sales in USA', className='text-lg xl:text-xl'),
                        html.P(children='Dashboard by Kacper Krawiec', className='text-white/[.8] lg:text-base')
                    ]
                ),
                html.Div(
                    className='flex flex-col pb-6 lg:pb-8 justify-center items-center bg-[#222222]'
                              ' text-center gap-2',
                    children=[
                        html.P(children=f'Created with Vehicle Sales dataset:'),
                        html.A(href='https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data', children='https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data', className='text-white/[.8]')
                    ]
                ),
                html.Div(
                    className='flex flex-col items-center gap-2 2xl:gap-24',
                    children=[
                        # MAP GRAPH
                        html.Div(
                            className='flex flex-col w-full gap-4 lg:gap-20 bg-[#111111] 2xl:w-1/2 text-center py-10 text-black',
                            children=[
                                html.H4(children='Number of vehicle sales in different states by year of production', className='text-base md:text-lg lg:text-xl text-white px-6'),
                                dcc.Graph(id='map-content'),
                                html.Div(
                                    className='w-full flex flex-col gap-4 items-center',
                                    children=[
                                        html.P('Select year of production', className='text-white text-center pl-6 lg:text-base xl:text-lg'),
                                        dcc.Dropdown(df.year.unique(), className='text-black px-6 w-full w-[350px]', value=2015, id='map-dropdown')
                                    ]
                                ),
                            ]
                        ),

                        html.Div(
                            className='flex flex-col xl:flex-row justify-evenly 2xl:justify-center gap-4 '
                                      'lg:gap-10 w-full',
                            children=[
                                dcc.Graph(figure=best_sellers, className='xl:max-w-[610px]'),
                                dcc.Graph(figure=price_hist, className=' xl:max-w-[610px]'),
                            ]
                        ),



                        # FILTER
                        html.Div(
                            className='bg-[#111111] w-full',
                            children=[
                                html.Div(
                                    className='flex flex-col gap-4 items-center bg-[#222222]',
                                    children=[
                                        html.Div(
                                            className='w-full flex flex-col md:max-w-[500px] px-6 pt-6 gap-3 md:text-base',
                                            children=[
                                                html.H3(children='Specific search',
                                                        className='text-base pb-4 md:py-6 lg:text-lg 2xl:text-xl'),
                                                html.Div([
                                                    html.P(children='Manufacturer', className='text-bold mb-1'),
                                                    dcc.Dropdown(
                                                        id='manufacturer-name',
                                                        options=df.make.unique(),
                                                        className='text-black',
                                                        value='Ford',
                                                        clearable=False,
                                                    )
                                                ]),
                                                html.Div([
                                                    html.P(children='Model', className='text-bold mb-1'),
                                                    dcc.Dropdown(
                                                        id='model-name',
                                                        className='text-black',
                                                    )
                                                ]),
                                                html.Div([
                                                    html.P(children='Year of Production', className='text-bold mb-1', ),
                                                    dcc.Dropdown(options=df.year.unique(), id='year-of-production',
                                                                 className='text-black', placeholder='Any'),
                                                ]),
                                            ]
                                        ),

                                        html.P(
                                            className='text-center py-6 md:py-8 text-lg 2xl:text-xl font-bold',
                                            id='manufacturer-name-p',
                                        ),
                                        html.Div(
                                            className='w-full max-w-[700px] pb-6 md:pb-12 lg:pb-16',
                                            children=[
                                                dcc.Graph(id='filtered-table'),
                                            ]
                                        ),

                                        html.Div(
                                            className='w-full flex flex-col bg-[#111111] pt-6 md:pt-12 lg:pt-16',
                                            children=[
                                                html.P(
                                                    className='text-center text-lg md:text-xl lg:text-xl font-bold pb-6 md:pb-12 lg:pb-16',
                                                    children='Filtered data plots'
                                                ),
                                                html.Div(
                                                    className='w-full flex flex-col xl:flex-row xl:justify-center xl:gap-12',
                                                    children=[
                                                        dcc.Graph(id='manufacturer-sales-graph'),
                                                        dcc.Graph(id='transmission-distribution')
                                                    ]

                                                ),
                                                html.Div(
                                                    className='w-full flex flex-col xl:flex-row xl:justify-center md:pb-12',
                                                    children=[
                                                        dcc.Graph(id='best-selling-states')
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)

@callback(
    Output('map-content', 'figure'),
    Input('map-dropdown', 'value')
)
def update_map(value):
    dff = df.copy()
    dff = dff[dff.year==value].state.value_counts()
    dff = dff.rename_axis('state_code').reset_index(name='sales')

    fig_map = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='sales',
        template='plotly_dark',
    ).update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig_map

@callback(
    [Output('manufacturer-name-p', 'children'),
     Output('manufacturer-sales-graph', 'figure'),
     Output('transmission-distribution', 'figure'),
     Output('model-name', 'options'),
     Output('filtered-table', 'figure'),
     Output('best-selling-states', 'figure')],
    [Input('manufacturer-name', 'value'),
     Input('year-of-production', 'value'),
     Input('model-name', 'value')],
)
def update_manufacturer_sales(name, year, model_name):
    dff = df.copy()
    dff = dff[dff['make']==name]


    if ctx.triggered_id=='manufacturer-name':
        if model_name is not None:
            model_name = None

    if year is not None:
        dff = dff[dff['year']==year]
    else:
        dff = df.copy()
        dff = dff[dff['make'] == name]
        if model_name is not None:
            dff = dff[dff['model'] == model_name]

    if model_name is not None:
        dff = dff[dff['model']==model_name]
    else:
        dff = df.copy()
        dff = dff[dff['make'] == name]
        if year is not None:
            dff = dff[dff['year'] == year]


    manufacturer_sales = px.box(
        data_frame=dff,
        x=dff['sellingprice'],
        template='plotly_dark',
        title='Selling price distribution'
    ).update_layout(title_x=.5)

    transmission_dis = px.pie(
        data_frame=dff,
        names = dff['transmission'],
        template='plotly_dark',
        title='Transmission'
    ).update_layout(title_x=.5)

    p = f'Data on {name} sales'

    models = dff['model'].unique()

    if len(dff) > 0:
        data_row = [name, len(dff), round(dff['sellingprice'].mean()), round(dff['odometer'].mean())]
    else:
        data_row = ['no data' for _ in range(4)]

    table_data = [
        ['Manufacturer', 'Sold Cars', 'Avg Price', 'Avg Odometer'],
        data_row
    ]
    table = ff.create_table(table_data)

    best_states = px.bar(dff['state'].value_counts(), template='plotly_dark', title='Best Selling States').update_layout(title_x=.5)

    return p, manufacturer_sales, transmission_dis, models, table, best_states


if __name__ == '__main__':
    app.run(debug=True)