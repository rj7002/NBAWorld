# import streamlit as st
# import pandas as pd

# df = pd.read_csv('/Users/ryan/Downloads/NBAPlayerLocationWebApp/locations.csv')

# # Display a title
# st.title('Map of Locations')

# # Display the map using st.map
# st.map(df)
# cities = df['City'].unique()
# st.selectbox('city',cities)
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import datetime
import requests
def display_player_image(player_id, width2, caption2):
    # Construct the URL for the player image using the player ID
    image_url = f"https://www.basketball-reference.com/req/202106291/images/headshots/{player_id}.jpg"
    
    # Check if the image URL returns a successful response
    response = requests.head(image_url)
    
    if response.status_code == 200:
        # If image is available, display it
        st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{image_url}" style="width: {width2}px;">'
        f'<p style="text-align: center;">{caption2}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
        # st.image(image_url, width=width2, caption=caption2)
    else:
        image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/fallback.png"
        st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{image_url}" style="width: {width2}px;">'
        f'<p style="text-align: center;">{caption2}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

currentyear = datetime.now().year
# # Read the CSV file
df = pd.read_csv('player_data2.csv')

st.set_page_config(page_title='NBA World',page_icon='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3I6B-gj9HiNSibn8u1eZpgegXRQDnIy_Fkw&s')
st.markdown("<h2 style='text-align: center; font-size: 80px;'>NBA World</h2>", unsafe_allow_html=True)
st.subheader('View the birthplaces of every NBA player from 1947 to 2020')

# Display a title
filter = st.selectbox('Filter by:',['','USA','World'])
if filter:
    year = st.slider('Select year',1947,2020,2020)
    df = df[df['start_year']<=year]
    if filter == 'USA':
        df=df[df['Country']=='USA']
        type = st.selectbox('Filter by:',['City','State'])
        if type == 'City':
            df_agg = df.groupby('City').agg({'Latitude': 'first', 'Longitude': 'first','State':'first', 'Player': lambda x: ', '.join(x)}).reset_index()
            df_agg['NumPlayers'] = df.groupby('City')['Player'].nunique().values
            # Create a Plotly figure with scattermapbox
            fig = px.scatter_mapbox(df_agg, 
                                    lat='Latitude', 
                                    lon='Longitude', 
                                    hover_name=df_agg.apply(lambda row: f"{row['City']},  {row['State']}<br>Number of players: {row['NumPlayers']}<br>Players:<br>{row['Player'].replace(', ', ', <br>')}", axis=1),
                                    zoom=4,color='State',size_max=15,width=1000,height=700)

            # Customize the map layout
            fig.update_layout(mapbox_style="carto-darkmatter",
                            mapbox_zoom=3.5,
                            mapbox_center={"lat": 40, "lon": -98})
            st.plotly_chart(fig)
            df_agg2 = df.groupby('City').agg({'Latitude': 'first', 'Longitude': 'first','State':'first', 'Player': lambda x: ', '.join(x)}).reset_index()
            df_agg2['NumPlayers'] = df.groupby('City')['Player'].nunique().values

            fig2 = px.scatter(df_agg2, x='City', y='NumPlayers',
                    title='Number of NBA Players by City',
                    labels={'NumPlayers': 'Number of Players', 'City': 'City'},
                    color='NumPlayers',  # Color bars based on number of players
                    color_continuous_scale='Hot'  # Color scale for bars
                    )

            # Customize layout
            fig2.update_layout(
                xaxis_title='City',
                yaxis_title='Number of Players',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                bargap=0.1,  # Gap between bars
                margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
            )
            st.plotly_chart(fig2)
            cities = df['City'].unique()
            st.markdown(f"<h2 style='text-align: center; font-size: 40px;'>{cities.size} different cities</h2>", unsafe_allow_html=True)
            city = st.selectbox('Select city',cities)
            citydf = df[df['City']==city]
            for index, row in citydf.iterrows():
                playerid = row['bbref_id']
                # display_player_image(playerid,100,'')
                # st.markdown(f'<div style="text-align: center;"><a href="{row["bbref_link"]}" target="_blank">{row["Player"]}</a>', unsafe_allow_html=True)
                display_player_image(playerid, 100, f'<a href="{row["bbref_link"]}" target="_blank">{row["Player"]}</a>')

        # Render the map using st.plotly_chart
        df_agg = df.groupby('State').agg({'Latitude': 'first', 'Longitude': 'first', 'Player': lambda x: ', '.join(x)}).reset_index()
        df_agg['NumPlayers'] = df.groupby('State')['Player'].nunique().values
        fig1 = px.bar(df_agg, x='State', y='NumPlayers',
                    title='Number of NBA Players by State',
                    labels={'NumPlayers': 'Number of Players', 'State': 'State'},
                    color='NumPlayers',  # Color bars based on number of players
                    color_continuous_scale='Hot'  # Color scale for bars
                    )

        # Customize layout
        fig1.update_layout(
            xaxis_title='State',
            yaxis_title='Number of Players',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.1,  # Gap between bars
            margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
        )

        

        

            
        df2 = df[df['Country'] == 'USA']
        df_agg5 = df2.groupby('birth_location').agg({'Latitude': 'first', 'Longitude': 'first', 'State':'first','Player': lambda x: ', '.join(x)}).reset_index()
        df_agg5['NumPlayers'] = df2.groupby('birth_location')['Player'].nunique().values
        
        if type == 'State':
            fig3 = px.choropleth(df_agg5, locations='State', locationmode='USA-states', color='NumPlayers',

                            color_continuous_scale='Hot')  # Update layout settings
            fig3.update_layout(
                geo=dict(
                    showland=True,
                    landcolor='black',  # Color of land areas
                    lakecolor='lightblue',  # Color of water areas
                    countrycolor='green',scope="usa"# Color of country borders
                ),
            )
            st.plotly_chart(fig3,use_container_width=True)
            st.plotly_chart(fig1)
            states = df['State'].unique()

            st.markdown(f"<h2 style='text-align: center; font-size: 40px;'>{states.size} different states/districts</h2>", unsafe_allow_html=True)
            state = st.selectbox('Select state',states)
            statedf = df[df['State']== state]
            for index, row in statedf.iterrows():
                playerid = row['bbref_id']
                display_player_image(playerid,100,'')
                st.markdown(f'<div style="text-align: center;"><a href="{row["bbref_link"]}" target="_blank">{row["Player"]}</a>', unsafe_allow_html=True)

        

    # elif filter == 'State':
    #     df_agg = df.groupby('State').agg({'Latitude': 'first', 'Longitude': 'first','G': 'sum', 'Player': lambda x: ', '.join(x)}).reset_index()
    #     df_agg['NumPlayers'] = df.groupby('State')['Player'].nunique().values
    #     # Create a Plotly figure with scattermapbox
    #     fig = px.scatter_mapbox(df_agg, 
    #                         lat='Latitude', 
    #                         lon='Longitude', 
    #                         hover_name=df_agg.apply(lambda row: f"{row['State']}<br>Number of players: {row['NumPlayers']}<br>Players: {row['Player'].replace(', ', ', <br>')}", axis=1),
    #                         zoom=3,  # Adjust zoom level as needed
    #                         color='State', 
    #                         size='NumPlayers', 
    #                         size_max=15,  # Adjust maximum marker size
    #                         width=1000, 
    #                         height=600)

    #     # Add a state-level marker (using an average central point for the map)
    #     # Adjust the latitude and longitude as per your need
    #     fig.add_scattermapbox(
    #         lat=[df_agg['Latitude'].mean()], 
    #         lon=[df_agg['Longitude'].mean()], 
    #         text=df_agg['State'].unique(),  # Text to display on hover
    #         mode='markers',
    #         marker=dict(size=10, color='black', opacity=0.5),
    #         hoverinfo='text'
    #     )

    #     # Customize the map layout
    #     fig.update_layout(
    #         mapbox_style="carto-darkmatter",
    #         mapbox_zoom=3,  # Adjust initial zoom level
    #         mapbox_center={"lat": df_agg['Latitude'].mean(), "lon": df_agg['Longitude'].mean()},  # Center of the map
    #     )

    #     # Render the map using st.plotly_chart
        # st.plotly_chart(fig)
    elif filter == 'World':
        type = st.selectbox('Filter by:',['State','Country'])
        st.write('This graph shows country of birth, this might not be the same nationality (US not included)')
        df = pd.read_csv('player_data2.csv')
        df = df[df['start_year']<=year]
        df_agg = df.groupby('City').agg({'Latitude': 'first', 'Longitude': 'first','State':'first', 'Country': 'first','Player': lambda x: ', '.join(x)}).reset_index()
        df_agg['NumPlayers'] = df.groupby('City')['Player'].nunique().values
        # Initialize the figure with Scattergeo
        fig = go.Figure(go.Scattergeo())

        # Add markers for each city
        for index, row in df_agg.iterrows():
            if row['State'] == None:
                    r = row['Country']
            else:
                r = row['State']
            fig.add_trace(go.Scattergeo(
                lon=[row['Longitude']],  # Longitude of the city
                lat=[row['Latitude']],   # Latitude of the city
                text=f"{row['City']}, {r}<br>Number of players: {row['NumPlayers']}<br>Players: {row['Player'].replace(', ', ', <br>')}",  # Hover text
                marker=dict(
            # Marker size based on the number of players
                    color='red',               # Marker color
                    line=dict(width=1, color='rgb(40,40,40)')  # Marker border settings
                ),fill='none',fillcolor='blue',
                name=row['City'],locationmode='country names',showlegend=False,  # Name of the trace (city name)
            ))

        # Update layout of the figure
        fig.update_geos(projection_type="orthographic",showsubunits=True, subunitcolor="Black",showocean=True,oceancolor='#3399FF',showcoastlines=True,coastlinecolor='black')
        fig.update_layout(
            geo=dict(
                showland=True,
                landcolor='green',
                countrycolor='green',
            ),
            height=600,  # Adjust figure height
            margin={"r":0,"t":0,"l":0,"b":0}  # Adjust margins
        )
        if type == 'State':
            st.plotly_chart(fig)
        countries = df['Country'].unique()
        df_agg2 = df.groupby('Country').agg({'Latitude': 'first', 'Longitude': 'first', 'Player': lambda x: ', '.join(x)}).reset_index()
        df_agg2['NumPlayers'] = df.groupby('Country')['Player'].nunique().values
        df_agg2 = df_agg2[df_agg2['Country'] != 'USA']
        fig2 = px.bar(df_agg2, x='Country', y='NumPlayers',
                    title='Number of NBA Players by Country',
                    labels={'NumPlayers': 'Number of Players', 'Country': 'Country'},
                    color='NumPlayers',  # Color bars based on number of players
                    color_continuous_scale='Hot'  # Color scale for bars
                    )

        # Customize layout
        fig2.update_layout(
            xaxis_title='Country',
            yaxis_title='Number of Players',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.1,  # Gap between bars
            margin=dict(l=50, r=50, t=50, b=50) # Adjust margins
        )
        # Create a choropleth map using Plotly Express
        df_agg3 = df.groupby('Country').agg({'Latitude': 'first', 'Longitude': 'first', 'Player': lambda x: ', '.join(x)}).reset_index()
        df_agg3['NumPlayers'] = df.groupby('Country')['Player'].nunique().values
        fig3 = px.choropleth(df_agg2, locations='Country', locationmode='country names', color='NumPlayers',

                            color_continuous_scale='Hot')

        # Update layout settings
        fig3.update_layout(
            geo=dict(
                showland=True,
                showocean=True,
                landcolor='green',  # Color of land areas
                oceancolor='#3399FF',  # Color of water areas
                countrycolor='green', projection_type="orthographic" # Color of country borders
            ),height=600
        )

        # Center the plot in Streamlit using layout options
        if type == 'Country':
            st.plotly_chart(fig3)
        st.plotly_chart(fig2,use_container_width=True)

        st.markdown(f"<h2 style='text-align: center; font-size: 40px;'>{countries.size} different countries</h2>", unsafe_allow_html=True)
        country = st.selectbox('Select country',countries)
        countrydf = df[df['Country']==country]
        countrydf = countrydf[countrydf['Country']!='USA']
        for index, row in countrydf.iterrows():
            playerid = row['bbref_id']
            display_player_image(playerid,100,'')
            st.markdown(f'<div style="text-align: center;"><a href="{row["bbref_link"]}" target="_blank">{row["Player"]}</a>', unsafe_allow_html=True)

else:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3I6B-gj9HiNSibn8u1eZpgegXRQDnIy_Fkw&s",width=800)



    # Show the figure



