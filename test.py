# # import pandas as pd
# # from geopy.geocoders import Nominatim
# # from geopy.exc import GeocoderTimedOut

# # # Load your NBA player birthplaces CSV into a DataFrame
# # df = pd.read_csv('NBA Players by State.csv')

# # # Function to geocode a city to get its latitude and longitude
# # def get_lat_lon(city):
# #     geolocator = Nominatim(user_agent="MyApp")

# #     try:
# #         location = geolocator.geocode(city)
# #         if location:
# #             return location.latitude, location.longitude
# #         else:
# #             return None, None
# #     except GeocoderTimedOut:
# #         return get_lat_lon(city)  # Retry in case of timeout

# # # Apply geocoding function to each row in the DataFrame
# # # df['Latitude'], df['Longitude'] = zip(*df['City'].apply(get_lat_lon))

# # # # Save the updated DataFrame with latitude and longitude to a new CSV file
# # # df.to_csv('NBA Players by State.csv', index=False)

# # # # import pandas as pd

# # # # # Load the CSV file into a DataFrame
# # # # df = pd.read_csv('NBA Players by State.csv')

# # # # # Identify columns with 'Unnamed' and delete them
# # # # unnamed_columns = [col for col in df.columns if 'Unnamed' in col]
# # # # df = df.drop(columns=unnamed_columns, errors='ignore')

# # # # # Save the modified DataFrame back to a new CSV file
# # # # df.to_csv('NBA Players by State.csv', index=False)

# # # Import the required library
# # # from geopy.geocoders import Nominatim

# # # # Initialize Nominatim API
# # # geolocator = Nominatim(user_agent="MyApp")
# # # df = pd.read_csv('NBA Players by State.csv')
# # # df['Location'] = df['City'] + ', ' + df['State']
# # # print(df)
# # # for city in df['Location']:
# # #     location = geolocator.geocode(city)
# # #     print(f"The latitude of the {city} is: {location.latitude} and the latitude is {location.longitude}")

# import pandas as pd
# from geopy.geocoders import Nominatim

# # Initialize Nominatim API
# geolocator = Nominatim(user_agent="MyApp")

# # Read the CSV file
# df = pd.read_csv('locations.csv')
# df['Location'] = df['birth_city'] + ', ' + df['birth_location']

# # Initialize lists to store latitude and longitude values
# latitudes = []
# longitudes = []

# # Iterate through each city in the DataFrame
# count = 0

# for city in df['Location']:
#     # Use geolocator to get location (latitude, longitude) of the city
#     location = geolocator.geocode(city)
    
#     if location:
#         # Append latitude and longitude to lists
#         latitudes.append(location.latitude)
#         longitudes.append(location.longitude)
#     else:
#         # If location is not found, append NaN or some placeholder values as needed
#         latitudes.append(None)
#         longitudes.append(None)
#     count+=1
#     print(count)

# # Add latitude and longitude columns to the DataFrame
# df['Latitude'] = latitudes
# df['Longitude'] = longitudes

# # Print or display the updated DataFrame (for verification)
# print(df)

# # Save the updated DataFrame back to a CSV file
# df.to_csv('player_data2.csv', mode='a',index=False,header=False)

# import pandas as pd
# from geopy.geocoders import Nominatim

# # Initialize Nominatim API
# geolocator = Nominatim(user_agent="MyApp")

# # Read the CSV file
# df = pd.read_csv('player_data.csv')
# df['Location'] = df['birth_city'] + ', ' + df['birth_location']

# # Define a function to geocode each city
# def geocode_city(city):
#     location = geolocator.geocode(city)
#     if location:
#         return pd.Series({'Latitude': location.latitude, 'Longitude': location.longitude})
#     else:
#         return pd.Series({'Latitude': None, 'Longitude': None})

# # Apply the function to each city in the 'City' column
# df[['Latitude', 'Longitude']] = df['Location'].apply(lambda x: geocode_city(x))

# # Print or display the updated DataFrame (for verification)
# print(df)

# # # # # Save the updated DataFrame back to a CSV file
# df.to_csv('player_data.csv', index=False)
# import pandas as pd
# # import plotly.graph_objects as go
# df = pd.read_csv('/Users/ryan/Downloads/NBAPlayerLocationWebApp/NBA Players by State.csv')
# df_agg = df.groupby('City').agg({'Latitude': 'first', 'Longitude': 'first','State':'first','G': 'sum', 'Player': lambda x: ', '.join(x)}).reset_index()
# df_agg['NumPlayers'] = df.groupby('City')['Player'].nunique().values
# # Initialize the figure with Scattergeo
# fig = go.Figure(go.Scattergeo())

# # Add markers for each city
# for index, row in df_agg.iterrows():
#     fig.add_trace(go.Scattergeo(
#         lon=[row['Longitude']],  # Longitude of the city
#         lat=[row['Latitude']],   # Latitude of the city
#         text=f"City: {row['City']}<br>State: {row['State']}<br>Number of players: {row['NumPlayers']}<br>Players: {row['Player'].replace(', ', ', <br>')}",  # Hover text
#         marker=dict(
#      # Marker size based on the number of players
#             color='red',               # Marker color
#             line=dict(width=0.5, color='rgb(40,40,40)')  # Marker border settings
#         ),
#         name=row['City'],locationmode='ISO-3'  # Name of the trace (city name)
#     ))

# # Update layout of the figure
# fig.update_geos(projection_type="orthographic",showsubunits=True, subunitcolor="Black")
# fig.update_layout(
#     title='NBA Players Distribution by City',
#     geo=dict(
#         showland=True,
#         landcolor='rgb(243, 243, 243)',
#         countrycolor='rgb(204, 204, 204)',
#     ),
#     height=600,  # Adjust figure height
#     margin={"r":0,"t":30,"l":0,"b":0}  # Adjust margins
# )

# # Show the figure
# fig.show()
# df_agg = df.groupby('City').agg({'Latitude': 'first', 'Longitude': 'first','State':'first','G': 'sum', 'Player': lambda x: ', '.join(x)}).reset_index()
# df_agg['NumPlayers'] = df.groupby('City')['Player'].nunique().values

# import plotly.express as px
# import plotly.graph_objects as go
# # Load US state abbreviation codes for Plotly chloropleth map
# geojson = px.data.election_geojson()

# # Create the chloropleth map using Plotly Graph Objects
# fig = go.Figure(go.Choropleth(
#     geojson=geojson,
#     locations=df_agg['State'],
#     z=df_agg['NumPlayers'].astype(float),
#     locationmode='USA-states',
#     colorscale='Viridis',
#     colorbar_title='Number of Players',
# ))

# # Update layout settings
# fig.update_layout(
#     title_text='NBA Players Distribution by State',
#     geo=dict(
#         scope='usa',
#         projection=go.layout.geo.Projection(type='albers usa'),
#         showlakes=True,  # Display lakes
#         lakecolor='rgb(255, 255, 255)'  # Color for lakes
#     )
# )

# # Show the figure using Streamlit
# fig.show()

# import plotly.express as px
# import pandas as pd
# import plotly.graph_objects as go

# # Load Plotly GeoJSON data for US states
# geojson = px.data.election_geojson()

# # Load your NBA players data from CSV
# df = pd.read_csv('NBA Players by State.csv')

# # Assuming your CSV has columns like 'City', 'State', 'NumPlayers'
# # Adjust 'locations' and 'color' parameters based on your data structure
# fig = px.choropleth(df, geojson=geojson, locations='State', color='NumPlayers',
#                     scope="usa",
#                     # You can customize labels and other properties here
#                     labels={'NumPlayers': 'Number of Players'}
#                    )

# fig.update_layout(
#     title_text='NBA Players Distribution by State',
#     geo=dict(
#         scope='usa',
#         projection=go.layout.geo.Projection(type='albers usa'),
#         showlakes=True,  # Display lakes
#         lakecolor='rgb(255, 255, 255)'  # Color for lakes
#     )
# )

# fig.show()
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('player_data2.csv')

# Function to determine country based on birth_country
def determine_country(row):
    if row['birth_country'] == 'US':
        return 'USA'
    else:
        return row['birth_location']

# Apply the function row-wise to update the 'Country' column
df['Country'] = df.apply(determine_country, axis=1)

# Optionally, you can overwrite the 'birth_location' column if needed
# df['birth_location'] = df['Country']

# Print the updated DataFrame to verify
print(df.head())  # Display the first few rows to verify the 'Country' column

# Save the updated DataFrame back to CSV
df.to_csv('player_data2.csv', index=False)