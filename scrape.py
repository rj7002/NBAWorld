# import json
# import csv

# # Specify input JSON file path
# json_file = '/Users/ryan/Downloads/NBAPlayerLocationWebApp/data.json'

# # Specify output CSV file path
# csv_file = '/Users/ryan/Downloads/NBAPlayerLocationWebApp/player_data.csv'

# try:
#     # Read JSON data from file
#     with open(json_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     # Verify loaded data structure
#     if not isinstance(data, dict):
#         raise TypeError('JSON data is not in expected dictionary format.')

#     # Extracting header fields from the first record in the data
#     headers = list(data[next(iter(data))].keys())

#     # Writing data to CSV file
#     with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=headers)
#         writer.writeheader()
#         for player_id, player_data in data.items():
#             writer.writerow(player_data)

#     print(f'CSV file "{csv_file}" has been successfully created.')

# except FileNotFoundError:
#     print(f'Error: JSON file "{json_file}" not found.')

# except json.JSONDecodeError as e:
#     print(f'Error decoding JSON file: {e}')

# except TypeError as e:
#     print(f'Error: {e}')

# except Exception as e:
#     print(f'An unexpected error occurred: {e}')


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# url = 'https://www.basketball-reference.com/friv/birthplaces.fcgi?country=US&state=AL'

# # Send a GET request to the URL
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find the table containing player data
#     table = soup.find('table', {'class': 'sortable'})

#     # Initialize empty lists for headers and data
#     headers = []
#     data = []

#     # Extract table rows
#     rows = table.find_all('tr')

#     # Extract headers from the second row (index 1) onwards
#     for th in rows[1].find_all('th'):
#         headers.append(th.text.strip())

#     # Extract rows from the table body skipping the first row (headers)
#     for row in rows[2:]:
#         row_data = []
#         for td in row.find_all('td'):
#             row_data.append(td.text.strip())
#         data.append(row_data)

#     # Ensure we only pass 31 columns to DataFrame constructor
#     headers = headers[:31]
#     data = [row[:31] for row in data]

#     # Create a DataFrame
#     df = pd.DataFrame(data, columns=headers)

#     # Print or further process the DataFrame
#     print(df)

# else:
#     print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # URL of the main birthplaces page
# url = 'https://www.basketball-reference.com/friv/birthplaces.fcgi'

# # Send a GET request to the URL
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find all links to state/country pages
#     state_links = []
#     for a in soup.find_all('a', href=True):
#         if 'friv/birthplaces.fcgi?country' in a['href']:
#             state_links.append('https://www.basketball-reference.com' + a['href'])

#     # Create a DataFrame to store the links
#     df_links = pd.DataFrame(state_links, columns=['Link'])

#     # Print or further process the DataFrame
#     print(df_links)
#     df_links.to_csv('links.csv')

# else:
#     print(f'Failed to retrieve the webpage. Status code: {response.status_code}')


import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the main birthplaces page
url = 'https://www.basketball-reference.com/friv/birthplaces.fcgi'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links to state/country pages
    state_links = []
    for a in soup.find_all('a', href=True):
        if 'friv/birthplaces.fcgi?country' in a['href']:
            state_links.append('https://www.basketball-reference.com' + a['href'])

    # Create a DataFrame to store the links
    df_links = pd.DataFrame(state_links, columns=['Link'])

    # Print or further process the DataFrame
    # print(df_links)
    # df_links.to_csv('links.csv')

    df_data = pd.read_csv('links.csv')
    count = 0
    for link in df_data['Link']:
        try:
            # Send a GET request to the URL
            response = requests.get(link)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the table containing player data
                table = soup.find('table', {'class': 'sortable'})

                if table:
                    # Initialize empty lists for headers and data
                    headers = []
                    data = []

                    # Extract table rows
                    rows = table.find_all('tr')

                    # Extract headers from the second row (index 1) onwards
                    for th in rows[1].find_all('th'):
                        headers.append(th.text.strip())

                    # Extract rows from the table body skipping the first row (headers)
                    for row in rows[2:]:
                        row_data = []
                        for td in row.find_all('td'):
                            row_data.append(td.text.strip())
                        data.append(row_data)

                    # Ensure we only pass 31 columns to DataFrame constructor
                    headers = headers[:31]
                    data = [row[:31] for row in data]

                    # Create a DataFrame
                    df = pd.DataFrame(data, columns=headers)

                    # Write to CSV file in append mode
                    df.to_csv('alldata.csv', mode='a', header=True, index=False)

                    count += 1
                    print(f'Successfully processed {link}. Count: {count}')

                else:
                    print(f'Table not found on page: {link}')

            else:
                print(f'Failed to retrieve the webpage: {link}. Status code: {response.status_code}')

        except Exception as e:
            print(f'Error processing page: {link}. Error: {str(e)}')
        

else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
