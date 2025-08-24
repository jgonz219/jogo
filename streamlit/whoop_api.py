from dotenv import load_dotenv
import streamlit as st
import requests
import os
import time
from urllib.parse import urlencode

# Load .env file
load_dotenv()

# Configuration
CLIENT_ID = os.getenv("WHOOP_CLIENT_ID", None)
CLIENT_SECRET = os.getenv("WHOOP_CLIENT_SECRET", None)
REDIRECT_URI = os.getenv("WHOOP_REDIRECT_URI", "http://localhost:8501")

# WHOOP API endpoints
AUTHORIZE_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"

# Scopes
SCOPES = [
    "read:recovery",
    "read:cycles", 
    "read:sleep",
    "read:workout",
    "read:profile",
    "read:body_measurement"
]

def get_authorization_url():
    """Generate OAuth2 authorization URL"""
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'state': 'streamlit_whoop_app'
    }
    return f"{AUTHORIZE_URL}?{urlencode(params)}"

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    
    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        st.session_state.access_token = token_data.get('access_token')
        st.session_state.authenticated = True

    except requests.exceptions.RequestException as e:
        st.error(f"Authentication failed: {e}")

def get_body_measurement():
    """Fetch body measurement data from WHOOP API"""
    headers = {
        'Authorization': f"Bearer {st.session_state.access_token}"
    }
    
    try:
        response = requests.get(
            "https://api.prod.whoop.com/developer/v2/user/measurement/body", 
            headers=headers
        )
        response.raise_for_status()

        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch body measurement data: {e}")
        return None
    
def get_workouts():
    headers = {
        'Authorization': f"Bearer {st.session_state.access_token}"
    }

    all_workouts = []
    next_token = None

    try:
        while True:
            params = {
                'start': '2025-07-20T01:00:00.000Z',
            }
            if next_token:
                params['nextToken'] = next_token
            
            response = requests.get(
                "https://api.prod.whoop.com/developer/v2/activity/workout",
                headers=headers,
                params=params
            )
            
            if response.status_code == 429:
                st.error("Rate limit exceeded. Waiting 10 seconds")
                time.sleep(10)
                continue
            
            response.raise_for_status()
            data = response.json()

            # Extend with workouts from this page
            all_workouts.extend(data.get('records', []))
            
            # Check if there's more data
            next_token = data.get('next_token')
            if not next_token:
                break

        return all_workouts

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch workouts data: {e}")
        return None

def refresh():
    # Check for authorization code in URL parameters
    query_params = st.query_params
    auth_code_from_url = query_params.get("code", None)
    auth_url = get_authorization_url()
    st.link_button(label="Refresh Whoop data", url=auth_url)

    # If we have a code in the URL, process it
    if auth_code_from_url and 'access_token' not in st.session_state:
        with st.spinner("Refreshing WHOOP data..."):
            exchange_code_for_token(auth_code_from_url)
            st.query_params.clear()

    if 'access_token' in st.session_state:
        with st.spinner("Fetching body measurement...", show_time=True):
            st.session_state.body_measurement = get_body_measurement()
        with st.spinner("Fetching workouts...", show_time=True):
            st.session_state.workouts = get_workouts()
