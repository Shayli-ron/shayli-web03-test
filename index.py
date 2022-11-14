# from inspect import trace
# from distutils.log import debug
# from gc import callbacks
# from time import strftime
# from timeit import main
# from turtle import color, width
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input , Output, State
import plotly.graph_objs as go
import pandas as pd
import datetime

# app downnloads yipit data
add_downloads = pd.read_csv('U.S. App Downloads Yipit Oct29 - Sheet1.csv')

add_downloads_df = add_downloads.set_index('Time').T
add_downloads_df = add_downloads_df.reset_index()
add_downloads_df['Time column'] = add_downloads_df['index']
add_downloads_df = add_downloads_df.drop('index' , axis = 1)

add_downloads_df['Affirm - App Downloads - Indexed'] = add_downloads_df['Affirm - App Downloads - Indexed'].str.replace(',','')
add_downloads_df['Affirm - App Downloads - Indexed'] = add_downloads_df['Affirm - App Downloads - Indexed'].astype(float)

add_downloads_df['Affirm - % of Total'] = add_downloads_df['Affirm - % of Total'].str.replace('%','')
add_downloads_df['Affirm - % of Total'] = add_downloads_df['Affirm - % of Total'].astype(float)

add_downloads_df['Affirm - Y/Y Growth'] = add_downloads_df['Affirm - Y/Y Growth'].str.replace('%','')
add_downloads_df['Affirm - Y/Y Growth'] = add_downloads_df['Affirm - Y/Y Growth'].astype(float)

add_downloads_df['Time column'] = add_downloads_df['Time column'].str.replace('-','-20')
add_downloads_df['Time column'] = pd.to_datetime(add_downloads_df['Time column'])

# app downloads from ms data
app_download_ms = pd.read_csv('U.S App Downloads (Graph) MS - App Metrics (Graph) - U.S App Downloads (Graph) MS - App Metrics (Graph).csv')

app_download_ms_df = app_download_ms.set_index('Time').T
app_download_ms_df = app_download_ms_df.reset_index()
app_download_ms_df['Time column'] = app_download_ms_df['index']
app_download_ms_df = app_download_ms_df.drop('index' , axis = 1)

app_download_ms_df['Time column'] = pd.to_datetime(app_download_ms_df['Time column'])

#GMV Yipit
gmv_yipit_data = pd.read_csv('GMV YipitData - Sheet1.csv')

gmv_yipit_df = gmv_yipit_data.set_index('Time').T
gmv_yipit_df = gmv_yipit_df.reset_index()
gmv_yipit_df['Time column'] = gmv_yipit_df['index']
gmv_yipit_df = gmv_yipit_df.drop('index' , axis = 1)

gmv_yipit_df['GMV ($K)'] = gmv_yipit_df['GMV ($K)'].str.replace('$','')
gmv_yipit_df['GMV ($K)'] = gmv_yipit_df['GMV ($K)'].str.replace(',','')
gmv_yipit_df['GMV ($K)'] = gmv_yipit_df['GMV ($K)'].astype(float)

gmv_yipit_df['Time column'] = gmv_yipit_df['Time column'].str.replace('-','-20')
gmv_yipit_df['Time column'] = pd.to_datetime(gmv_yipit_df['Time column'])

gmv_yipit_df['M/M (Q/Q) Growth'] = gmv_yipit_df['M/M (Q/Q) Growth'].str.replace('%','')
gmv_yipit_df['M/M (Q/Q) Growth'] = gmv_yipit_df['M/M (Q/Q) Growth'].astype(float)

gmv_yipit_df['Y/Y Growth'] = gmv_yipit_df['Y/Y Growth'].str.replace('%','')
gmv_yipit_df['Y/Y Growth'] = gmv_yipit_df['Y/Y Growth'].astype(float)

#gmv ms data:
gmv_ms_data = pd.read_csv('GMV MS  - Sheet 1.csv')

gmv_ms_df = gmv_ms_data.set_index('Time').T
gmv_ms_df = gmv_ms_df.reset_index()
gmv_ms_df['Time column'] = gmv_ms_df['index']
gmv_ms_df = gmv_ms_df.drop('index' , axis = 1)

gmv_ms_df['Total '] = gmv_ms_df['Total '].str.replace(',','')
gmv_ms_df['Total '] = gmv_ms_df['Total '].astype(float)

gmv_ms_df['m/m'] = gmv_ms_df['m/m'].str.replace('%','')
gmv_ms_df['m/m'] = gmv_ms_df['m/m'].astype(float)

gmv_ms_df['Y/Y'] = gmv_ms_df['Y/Y'].str.replace('%','')
gmv_ms_df['Y/Y'] = gmv_ms_df['Y/Y'].astype(float)

gmv_ms_df['Time column'] = pd.to_datetime(gmv_ms_df['Time column'])

#corr gmv data:
corr_yipit_gmv = gmv_yipit_df['M/M (Q/Q) Growth'][27:]
corr_yipit_gmv = corr_yipit_gmv.reset_index()
corr_yipit_gmv = corr_yipit_gmv.drop('index', axis = 1)

corr_ms_gmv = gmv_ms_df['m/m'][1:]
corr_ms_gmv = corr_ms_gmv.reset_index()
corr_ms_gmv = corr_ms_gmv.drop('index', axis = 1)



app = dash.Dash(__name__ )

app.layout = html.Div([
    html.Div([
            html.H4('AFRM Dashboard', style={'color' : 'white'}, className='title_afrm')
        ], style={'verticalAlign':'top', 'padding-left' : '45%'}),
    
    html.Div([
    dcc.Graph(
             id='appdownloads_afrm',
         figure={
            'data': 
            [go.Scatter(
                x=app_download_ms_df['Time column'],
                y=app_download_ms_df['Downloads']*100,
                name=f'M Science',
                mode='markers+lines',
                line=dict(color="orange")
           
            # fill="tonexty"
            )
                ,go.Scatter(
                x=add_downloads_df['Time column'],
                y=add_downloads_df['Affirm - App Downloads - Indexed'],
                name=f'YipitData',
                mode='markers+lines',
                line=dict(color="#05f8fc")
           
            # fill="tonexty"
            )]
                
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Numeric App Downloads', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(
                # title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Value</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
            }
            ,style={'width': '100%', 'height': '80vh'})
  
        ], className= 'create_container twelve columns'),

        html.Div([
    dcc.Graph(
             id='percentage_afrm',
         figure={
            'data': 
            [go.Scatter(
                x=add_downloads_df['Time column'],
                y=add_downloads_df['Affirm - Y/Y Growth'],
                name=f'Y/Y Growth YipitData',
                mode='markers+lines',
                line=dict(color="#b4f285", width = 7)
           
            # fill="tonexty"
            )
            ,go.Scatter(
                x=add_downloads_df['Time column'],
                y=add_downloads_df['Affirm - % of Total'],
                name=f'% of Total YipitData',
                mode='markers+lines',
                line=dict(color="#d285f2")
           
            # fill="tonexty"
            ),
            go.Scatter(
                x=app_download_ms_df['Time column'],
                y=app_download_ms_df['Downloads Y/Y Growth']*100,
                name=f'Y/Y Growth M Science',
                mode='markers+lines',
                line=dict(color="#799df2")
           
            # fill="tonexty"
            )]
                
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Percentage App Downloads', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(
                # title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Percentage</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
            }
            ,style={'width': '100%', 'height': '80vh'})
  
        ], className= 'create_container twelve columns'),


        html.Div([
    dcc.Graph(
             id='gmv_afrm',
         figure={
            'data': 
            [
            go.Scatter(
                x=gmv_yipit_df['Time column'],
                y=gmv_yipit_df['GMV ($K)'],
                name=f'GMV YipitData',
                mode='markers+lines',
                line=dict(color="#05f8fc")
           
            # fill="tonexty"
            ),
            go.Scatter(
                x=gmv_ms_df['Time column'],
                y=gmv_ms_df['Total '],
                name=f'GMV M Science',
                mode='markers+lines',
                line=dict(color="orange")
           
            # fill="tonexty"
            )]
                
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': ' GMV ', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(
                # title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Value</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
            }
            ,style={'width': '100%', 'height': '80vh'})
  
        ], className= 'create_container twelve columns'),

        html.Div([
    dcc.Graph(
             id='gmv_percentage_afrm',
         figure={
            'data': 
            [
            go.Scatter(
                x=gmv_yipit_df['Time column'],
                y=gmv_yipit_df['M/M (Q/Q) Growth'],
                name=f'M/M  Growth	YipitData',
                mode='markers+lines',
                line=dict(color="#05f8fc")
           
            ),
            go.Scatter(
                x=gmv_ms_df['Time column'],
                y=gmv_ms_df['m/m'],
                name=f'M/M Growth M Science',
                mode='markers+lines',
                line=dict(color="orange")
           
            ),
            go.Scatter(
                x=gmv_yipit_df['Time column'],
                y=gmv_yipit_df['Y/Y Growth'],
                name=f'Y/Y Growth YipitData',
                mode='markers+lines',
                line=dict(color="#799df2")
           
            ),
            go.Scatter(
                x=gmv_ms_df['Time column'],
                y=gmv_ms_df['Y/Y'],
                name=f'Y/Y Growth M Science',
                mode='markers+lines',
                line=dict(color="#edcc7e")
           
            )
            ]
                
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': ' GMV Growth', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(
                # title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Percentage</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
            }
            ,style={'width': '100%', 'height': '80vh'}),

            html.H6(f"The Correlation between YipitData & M Science is: {corr_yipit_gmv['M/M (Q/Q) Growth'].astype(float).corr(corr_ms_gmv['m/m'].astype(float)).astype(str)}",
                     style={'color' : 'white'})
        ], className= 'create_container twelve columns')
],id = 'mainContainer', style={'display':'flex', 'flex-direction': 'colum'})





if __name__ =='__main__':
    app.run_server(debug=True)