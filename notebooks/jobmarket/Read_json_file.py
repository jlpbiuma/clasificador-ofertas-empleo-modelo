import json
# Read json file
with open('./data/offers.json') as f:
    offers_news = json.load(f)
    
    
def format_offer(offer):
    expected_keys = ['title', 'description', 'company', 'location', 'category']
    expected_keys_post = ['date', 'site', 'id', 'url']
    expected_keys_labeled = ['category', 'site', 'location']
    formated_offer = {}
    
    for key in expected_keys:
        if key in offer and offer[key] is not None:
            if key in expected_keys_labeled:
                formated_offer[key] = offer[key]['label']
            else:
                formated_offer[key] = offer[key]
        else:
            formated_offer[key] = None
    
    post = get_last_record(offer['postings'])
    
    for key in expected_keys_post:
        if key in post:
            if key in expected_keys_labeled:
                formated_offer[key] = post[key]['label']
            else:
                formated_offer[key] = post[key]
        else:
            formated_offer[key] = None
    
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

# Save formatted offers in a JSON file
with open("./data/formated_offers.json", "w") as f:
    json.dump(formated_offers, f)