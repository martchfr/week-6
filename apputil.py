import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import pandas as pd
from joblib import Parallel, delayed

load_dotenv()

class Genius:

    # Iniatilzes Function and Pulls Access Token from Environment
    def __init__(self, access_token=None):
        self.access_token = access_token or os.environ.get("ACCESS_TOKEN")

        if self.access_token is None:
            raise ValueError(
                "No access token found. Pass access_token=... or set ACCESS_TOKEN in your .env file."
            )
        
    # Returns dictionary of artist searched
    def get_artist(self, search_term):
        genius_search_url = f"http://api.genius.com/search?q={search_term}"
    
        search_response = requests.get(genius_search_url, 
                                headers={"Authorization": "Bearer " + self.access_token})
        
        artist_id = search_response.json()["response"]["hits"][0]["result"]["primary_artist"]["id"]

        genius_artist_url = f"http://api.genius.com/artists/{artist_id}"

        artist_response = requests.get(genius_artist_url,
                                       headers={"Authorization" : "Bearer " + self.access_token})

        return artist_response.json()
    
    # Returns a Dataframe containg name, id, and followers for a list of Artists
    def get_artists(self, search_terms):

        artist_rows = []

        for term in search_terms:
            artist_json = self.get_artist(term)
            artist = artist_json["response"]["artist"]
            
            artist_rows.append({
                "search_term" : term,
                "artist_name" : artist["name"],
                "artist_id" : artist["id"],
                "followers" : artist["followers_count"]
            })
        df = pd.DataFrame(artist_rows)

        return df