#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

import urllib.parse as urlparse
from urllib.parse import parse_qs

import json


def get_all_stars():
    all_stars = {}

    r = requests.get('https://www.basketball-reference.com/awards/all_star_by_player.html')
    soup = BeautifulSoup(r.text, 'html.parser')

    table_rows = soup.find('tbody').findAll('tr')
    for row in table_rows:
        cols = row.findAll('td')
        player_id = cols[1].find('a')['href'].split('/')[-1].replace('.html', '')
        all_star_selections = cols[2].text

        all_stars[player_id] = all_star_selections

    return all_stars


def process_location(location_link, location_name, data, all_star_dict):
    print(location_name)

    full_link = 'https://www.basketball-reference.com/' + location_link
    parsed_params = parse_qs(urlparse.urlparse(full_link).query)
    country = parsed_params['country'][0]

    try:
        state = parsed_params['state'][0]
    except KeyError:
        state = None

    r = requests.get(full_link)
    soup = BeautifulSoup(r.text, 'html.parser')

    player_rows = soup.find('table', attrs={'class': 'stats_table'}).find('tbody').findAll('tr', class_=lambda x: x != 'thead')

    for row in player_rows:
        player = row.find('td', attrs={'data-stat': 'player'})

        if player:
            player_link = player.find('a')['href']
            player_name = player.find('a').text.strip()
            player_id = player['data-append-csv']
            career_ppg = row.find('td', attrs={'data-stat': 'pts_per_g'})
            start_year = row.find('td', attrs={'data-stat': 'year_min'})
            end_year = row.find('td', attrs={'data-stat': 'year_max'})
            birth_city = row.find('td', attrs={'data-stat': 'birth_city'})

            # Handle NoneType for career_ppg, start_year, end_year, and birth_city
            career_ppg = float(career_ppg.text.strip()) if career_ppg else 0.0
            start_year = int(start_year.text.strip()) if start_year else 0
            end_year = int(end_year.text.strip()) if end_year else 0
            birth_city = birth_city.text.strip() if birth_city else 'N/A'

            try:
                all_star_appearances = int(all_star_dict[player_id])
            except KeyError:
                all_star_appearances = 0

            data[player_id] = {
                'name': player_name,
                'bbref_link': player_link,
                'bbref_id': player_id,
                'career_ppg': career_ppg,
                'birth_location': location_name,
                'birth_country': country,
                'birth_state': state,
                'birth_city': birth_city,
                'start_year': start_year,
                'end_year': end_year,
                'high_school_state': None,
                'high_school_city': None,
                'high_school_name': None,
                'all_star_appearances': all_star_appearances
            }
        else:
            print(f"No player data found for {location_name}")

    return data


def process_high_schools(hs_link, location_name, data):
    print(location_name)

    full_link = 'https://www.basketball-reference.com/' + hs_link
    parsed_params = parse_qs(urlparse.urlparse(full_link).query)

    try:
        state = parsed_params['state'][0]
    except KeyError:
        state = None

    r = requests.get(full_link)
    soup = BeautifulSoup(r.text, 'html.parser')

    player_rows = soup.find('table', attrs={'class': 'stats_table'}).find('tbody').findAll('tr', class_=lambda x: x != 'thead')

    for row in player_rows:
        player = row.find('td', attrs={'data-stat': 'player'})

        if player:
            player_id = player['data-append-csv']
            high_school_city = row.find('td', attrs={'data-stat': 'hs_city'}).text.strip()
            high_school_name = row.find('td', attrs={'data-stat': 'hs_name'}).text.strip()

            try:
                if player_id in data:
                    data[player_id]['high_school_state'] = location_name
                    data[player_id]['high_school_city'] = high_school_city
                    data[player_id]['high_school_name'] = high_school_name
                else:
                    print(f"Player ID {player_id} not found in birthplace data.")
            except KeyError:
                print(f"KeyError: Player ID {player_id}")

        else:
            print(f"No player data found for {location_name}")

    return data


all_star_dict = get_all_stars()
player_birthplaces = {}

# Birthplaces

r = requests.get('https://www.basketball-reference.com/friv/birthplaces.fcgi')
soup = BeautifulSoup(r.text, 'html.parser')
wrappers = soup.find('div', attrs={'class': 'data_grid_group'}).findAll('p')

for wrapper in wrappers[2:]:
    link = wrapper.find('a')
    if link:
        try:
            player_birthplaces = process_location(link['href'], link.text, player_birthplaces, all_star_dict)
        except Exception as e:
            print(f"Error processing location {link.text}: {e}")
    else:
        print("Link not found in wrapper:", wrapper)

# High Schools

r = requests.get('https://www.basketball-reference.com/friv/high_schools.fcgi')
soup = BeautifulSoup(r.text, 'html.parser')
wrappers = soup.find('div', attrs={'class': 'data_grid_group'}).findAll('p')

for wrapper in wrappers:
    link = wrapper.find('a')
    if link:
        player_birthplaces = process_high_schools(link['href'], link.text, player_birthplaces)
    else:
        print("Link not found in wrapper:", wrapper)

with open('../raw_data/raw_player_data.json', 'w') as f:
    json.dump(player_birthplaces, f)
