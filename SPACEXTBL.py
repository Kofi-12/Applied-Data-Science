{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5e3aee13",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import required libraries\n",
    "import pandas as pd\n",
    "import dash\n",
    "import dash_html_components as html\n",
    "import dash_core_components as dcc\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px\n",
    "\n",
    "# Read the airline data into pandas dataframe\n",
    "spacex_df = pd.read_csv(\"spacex_launch_dash.csv\")\n",
    "max_payload = spacex_df['Payload Mass (kg)'].max()\n",
    "min_payload = spacex_df['Payload Mass (kg)'].min()\n",
    "\n",
    "# Create a dash application\n",
    "app = dash.Dash(__name__)\n",
    "\n",
    "# Create an app layout\n",
    "app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',\n",
    "                                        style={'textAlign': 'center', 'color': '#503D36',\n",
    "                                               'font-size': 40}),\n",
    "                                # TASK 1: Add a dropdown list to enable Launch Site selection\n",
    "                                # The default select value is for ALL sites\n",
    "                                # dcc.Dropdown(id='site-dropdown',...)\n",
    "                                dcc.Dropdown(id='site-dropdown',\n",
    "                                            options=[\n",
    "                                                         {'label': 'ALL SITES', 'value': 'ALL'},\n",
    "                                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},\n",
    "                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},\n",
    "                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},\n",
    "                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}\n",
    "                                                    ],\n",
    "                                            value='ALL',\n",
    "                                            placeholder=\"Select a Launch Site here\", \n",
    "                                            searchable=True),\n",
    "                                html.Br(),\n",
    "\n",
    "                                # TASK 2: Add a pie chart to show the total successful launches count for all sites\n",
    "                                # If a specific launch site was selected, show the Success vs. Failed counts for the site\n",
    "                                html.Div(dcc.Graph(id='success-pie-chart')),\n",
    "                                html.Br(),\n",
    "\n",
    "                                html.P(\"Payload range (Kg):\"),\n",
    "                                # TASK 3: Add a slider to select payload range\n",
    "                                dcc.RangeSlider(id='payload-slider',\n",
    "                                                min=0,max=10000,step=1000,\n",
    "                                                value=[min_payload,max_payload],\n",
    "                                                marks={0: '0', 2500:'2500',5000:'5000',\n",
    "                                                7500:'7500', 10000: '10000'}),\n",
    "\n",
    "                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success\n",
    "                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),\n",
    "                                ])\n",
    "\n",
    "# TASK 2:\n",
    "# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output\n",
    "@app.callback(\n",
    "    Output(component_id='success-pie-chart', component_property='figure'),\n",
    "    Input(component_id='site-dropdown', component_property='value'))\n",
    "\n",
    "def build_graph(site_dropdown):\n",
    "    if site_dropdown == 'ALL':\n",
    "        piechart = px.pie(data_frame = spacex_df, names='Launch Site', values='class' ,title='Total Launches for All Sites')\n",
    "        return piechart\n",
    "    else:\n",
    "        #specific_df = spacex_df['Launch Site']\n",
    "        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]\n",
    "        piechart = px.pie(data_frame = specific_df, names='class',title='Total Launch for a Specific Site')\n",
    "        return piechart\n",
    "\n",
    "# TASK 4:\n",
    "# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output\n",
    "@app.callback(\n",
    "    Output(component_id='success-payload-scatter-chart', component_property='figure'),\n",
    "    [Input(component_id='site-dropdown', component_property='value'),\n",
    "    Input(component_id='payload-slider', component_property='value')])\n",
    "\n",
    "def update_graph(site_dropdown, payload_slider):\n",
    "    if site_dropdown == 'ALL':\n",
    "        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])\n",
    "        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]\n",
    "        scatterplot = px.scatter(data_frame=filtered_data, x=\"Payload Mass (kg)\", y=\"class\", \n",
    "        color=\"Booster Version Category\")\n",
    "        return scatterplot\n",
    "    else:\n",
    "        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]\n",
    "        filtered_data = specific_df[(specific_df['Payload Mass (kg)']>=payload_slider[0])\n",
    "        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]\n",
    "        scatterplot = px.scatter(data_frame=filtered_data, x=\"Payload Mass (kg)\", y=\"class\", \n",
    "        color=\"Booster Version Category\")\n",
    "        return scatterplot\n",
    "\n",
    "# Run the app\n",
    "if __name__ == '__main__':\n",
    "    app.run_server()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
