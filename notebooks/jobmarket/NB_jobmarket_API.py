#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
import requests
import json
from tqdm import tqdm


# # Fetch the offers to jobmarket

# In[2]:


# Request data from API
user = "hacomar@fulp.es"
clave = "Atenas.2023"
base_url = "https://www.jobmarketinsights.com/jmi-api/"
login_url = base_url + "token"
N_offers = 51000


# # Log into API

# In[3]:


def login():
    # Define the headers to set the Content-Type
    headers = {'Content-Type': 'application/json'}
    # Create a dictionary containing the data to send as JSON
    payload = {'email': user, 'password': clave}
    # Convert the payload to JSON format
    json_payload = json.dumps(payload)
    # Send the POST request with the specified headers and JSON data
    r = requests.post(login_url, data=json_payload, headers=headers)
    # Check if the request was successful (status code 200)
    if r.status_code == 200:
        # Parse the JSON response
        data = r.json()
        token = data["auth"]["token"]
        return token
    else:
        print(f"Request failed with status code {r.status_code}")
        return None
token = login()
print(token)


# # Scope

# In[4]:


scope_url = base_url + "scopes"
def get_scope(token):
    payload = {'token': token}
    headers = {'Content-Type': 'application/json'}
    json_payload = json.dumps(payload)
    r = requests.post(scope_url, data=json_payload, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        print(f"Request failed with status code {r.status_code}")
        return None
response = get_scope(token)
scopes = response["scopes"][0]["key"]
print(scopes)


# In[5]:


token


# # Periods

# In[6]:


# Ask for list with able periods
periods_url = base_url + "periods"
def get_periods(token):
    payload = {'token': token}
    headers = {'Content-Type': 'application/json'}
    json_payload = json.dumps(payload)
    r = requests.post(periods_url, data=json_payload, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data['periods']
    else:
        print(f"Request failed with status code {r.status_code}")
        return None
# Returns an array of dicts with 4 keys: from, label, to, key
periods = get_periods(token)
print(periods)
# For example, we will use the first period
period = periods[10]
initial_date = period['from']
end_date = period['to']


# # Missing advertisers

# In[7]:


missing_adverts_url = base_url + "missingAdvertisers"

def create_payload(token, initial_date, end_date, size=100, offset=0):
    payload = {'strictPeriod': True, 'location': 'ES', 'token': token,"period" : "custom", "customDateFrom": initial_date, "customDateTo": end_date, "offset": offset}
    headers = {'Content-Type': 'application/json'}
    json_payload = json.dumps(payload)
    return json_payload, headers

def get_missing_adverts(token, scope, initial_date, end_date, size=100, offset=0):
    payload, headers = create_payload(token, scope, initial_date, end_date, size, offset)
    json_payload = json.dumps(payload)
    r = requests.post(missing_adverts_url, data=json_payload, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        print(f"Request failed with status code {r.status_code}")
        return None
# print(get_missing_adverts(token, scopes, initial_date, end_date))


# # Sites

# In[8]:


sites_url = base_url + "sites"
def get_sites(token):
    payload = {'token': token}
    headers = {'Content-Type': 'application/json'}
    json_payload = json.dumps(payload)
    r = requests.post(sites_url, data=json_payload, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        print(f"Request failed with status code {r.status_code}")
        return None
response = get_sites(token)
print(response)


# # Custom period

# In[9]:


# Create a function to create a list of objects with from and to keys with dates from an initial date to an end date
def create_date_range(initial_date, end_date):
    # The starting date is always at YYYY-MM-01 format
    initial_date = initial_date[:8] + "01"
    # The end date is always at YYYY-MM-01 format
    end_date = end_date[:8] + "01"
    # Create a list of dates from the initial date to the end date
    date_range = pd.date_range(initial_date, end_date, freq="MS")
    # Create a list of dicts with the dates
    date_range = [{"from": date.strftime("%Y-%m-%d"), "to": (date + pd.DateOffset(months=1)).strftime("%Y-%m-%d")} for date in date_range]
    # Delete last date because it is the first day of the next month
    date_range = date_range[:-1]
    return date_range
initial_date = "2021-01-01"
end_date = "2023-07-01"
new_periods = create_date_range(initial_date, end_date)
N_offers = 51000


# # Offers count

# In[10]:


count_url = base_url + "count"
offers_url = base_url + "offers"

def create_payload(token, site, location, initial_date, end_date, size=100, offset=0):
    payload = {'site': site, 'size': size, 'offset':offset, 'token': token, "period" : "custom", "customDateFrom": initial_date, "customDateTo": end_date, "location":location }
    return json.dumps(payload)

def get_offers(token, site, location, initial_date, end_date, size, offset):
    headers = {'Content-Type': 'application/json'}
    json_payload = create_payload(token, site, location, initial_date, end_date, size=size, offset=offset)
    try:
        r = requests.post(offers_url, data=json_payload, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            # print(data)
            return data['offers']
        else:
            print(f"Request failed with status code {r.status_code}")
            return None
    except:
        return None

def get_count(token, site, location, initial_date, end_date):
    headers = {'Content-Type': 'application/json'}
    json_payload = create_payload(token, site, location, initial_date, end_date)
    try:
        r = requests.post(count_url, data=json_payload, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data['offers']['market']
        else:
            print(f"Request failed with status code {r.status_code}")
            return None
    except:
        return None

def get_offers_by_period(token, site, location, initial_date, end_date, max_offers=1000):
    print(f"Period: {initial_date} - {end_date}")
    count = get_count(token, site, location, initial_date, end_date)
    print(f"Count: {count}")
    offers = []
    for offset in range(0, count, 100):
        print(f"Actual offers: {len(offers)}")
        size = 100
        response = get_offers(token, site, location, initial_date, end_date, size, offset)
        if response is not None:
            offers.extend(response)
        else:
            print("Error en la petición", offset, size, initial_date, end_date)
        if len(offers) >= max_offers:
            break
    return offers
    
def get_offers_by_period_list(token, site, location, periods, max_offers=1000):
    offers = []
    for period in periods:
        initial_date = period['from']
        end_date = period['to']
        print(f"Period: {initial_date} - {end_date}")
        count = get_count(token, site, location, initial_date, end_date)
        print(f"Count: {count}")
        # Wrap the loop with tqdm to create a progress bar
        for offset in tqdm(range(0, count, 100), desc="Downloading offers"):
            response = get_offers(token, site, location, initial_date, end_date, size=100, offset=offset)
            if response is not None:
                offers.extend(response)
            else:
                print("Error en la petición", offset, 100, initial_date, end_date)
            if len(offers) >= max_offers:
                break  # Exit the loop if you reach the maximum number of offers
    return offers

N_offers = 2000000
site = 1963
# location = "ES|53|GC^ES|53|TF"
# ! ES|53|GC|Las Palmas de Gran Canaria^ES|53|TF|Santa Cruz de Tenerife /= ES|53|GC^ES|53|TF
# location = "ES|53|GC|Las Palmas de Gran Canaria^ES|53|TF|Santa Cruz de Tenerife"
location = "ES"
initial_date = '2023-01-01'
end_date = '2023-01-10'
# offers_news = get_offers_by_period(token, site, location, initial_date, end_date, max_offers=N_offers)
site = 1963
location = "ES"
initial_date = '2021-01-01'
end_date = '2023-07-01'
new_periods = create_date_range(initial_date, end_date)
offers_news = get_offers_by_period_list(token, site, location, new_periods, max_offers=N_offers)
# Save the offers in a JSON file
with open("./data/offers.json", "w") as f:
    json.dump(offers_news, f)


# In[ ]:


# Cast to df
df_offers = pd.DataFrame(offers_news)
# Show shape
print(df_offers.shape)
# Delete repeated offers with same "description"
df_offers = df_offers.drop_duplicates(subset=['postings'])
# Show shape
print(df_offers.shape)
# Cast again to list of dicts
offers_news = df_offers.to_dict('records')


# In[ ]:


def format_offer(offer):
    expected_keys = ['title', 'description', 'company', 'location', 'category']
    expected_keys_post = ['date', 'site', 'id', 'url']
    expected_keys_labeled = ['category', 'site', 'location']
    formated_offer = {}
    for key in expected_keys:
        if key not in offer and offer[key] is not None:
            formated_offer[key] = None
        else:
            try:
                if key in expected_keys_labeled and offer[key] is not None:
                    formated_offer[key] = offer[key]['label']
                else:
                    formated_offer[key] = offer[key]
            except:
                continue
    post = get_last_record(offer['postings'])
    for key in expected_keys_post:
        if key not in post:
            formated_offer[key] = None
        else:
            try:
                if key in expected_keys_labeled and offer[key] is not None: 
                    formated_offer[key] = post[key]['label']
                else:
                    formated_offer[key] = post[key]
            except:
                continue
    formated_offer['id_oferta'] = get_id_oferta(formated_offer)
    return formated_offer

def get_last_record(postings):
    dates = []
    for post in postings:
        dates.append(post['date'])
    # Get index of the last date
    index = dates.index(max(dates))
    return postings[index]

def get_id_oferta(offer):
    url = offer['url']
    # Get the id after "of-i" in the url
    if "www.infojobs.net" in url:
        id_oferta = url.split("of-i")[1]
    else:
        id_oferta = None
    # Delete the last part of the id
    return id_oferta

def format_all_offers(offers):
    formated_offers = []
    for offer in offers:
        formated_offers.append(format_offer(offer))
    return formated_offers

formated_offers = format_all_offers(offers_news)

# Cast to df
df_offers = pd.DataFrame(formated_offers)
# Save to json
df_offers.to_json("./data/formated_offers.json", orient="records")

