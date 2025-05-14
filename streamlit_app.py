import streamlit as st
import json
import uuid
from datetime import datetime
import requests

# Page configuration
st.set_page_config(
    page_title="LinkedIn Sales Navigator Scraper",
    layout="wide"
)

# Generate a unique session ID
def generate_session_id():
    return str(uuid.uuid4())

# Validate if input is a valid JSON
def validate_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

# Validate Sales Navigator URL
def validate_url(url):
    return url.startswith("https://www.linkedin.com/sales/")

# Send request to backend scraper API (placeholder)
def send_to_webhook(data):
    WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL"
    BEARER_TOKEN = "YOUR_BEARER_TOKEN"
   
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
     }

    try:
       response = requests.post(WEBHOOK_URL, json-data, headers-headers) 
       response.raise_for_status()
       return response.json()
    except requests.exceptions.RequestException as e:
       st.error(f"Error sending request: {str(e)}") 
       return None

def main():
    st.title("LinkedIn Sales Navigator Scraper")

    #Initialize session state for Logs
    if 'scraper_logs' not in st.session_state: 
        st.session_state.scraper_logs = []
    
    with st.form("scraper_form"):
      # Input fields
      cookie_json = st.text_area("LinkedIn Sales Navigator Cookie JSON", help="Paste your Sales Navigator cookie JSON here")

      search_url = st.text_input("Sales Navigator Search URL", help="Enter the complete Sales Navigator search URL")

      num_leads = st.number_input(
          "Number of Leads to Generate",
          min_value=1,
          max_value=1000,
          value=100,
          help="Enter the number of leads you want to scrape"
      )
      
      email = st.text_input(
          "Email Address",
          help="Enter your email address for notifications"
      )

      submitted = st.form_submit_button("Start Scraping")

      if submitted:
         #Validote inputs
         if not cookie_json or not validate_json(cookie_json): 
           st.error("Please enter valid JSON for the cookie")
           return

      if not validate_url(search_url):
        st.error("Please enter a valid LinkedIn Sales Navigator URL")
        return

      if not email or '@' not in email:
        st.error("Please enter a valid email address")
        return

      # Prepare payload
      payload = {
        "sessionId": generate_session_id(),
        "timestamp": datetime.utcnow().isoformat(),
        "cookieJson": json.loads(cookie_json),
        "searchUrl": search_url,
        "numLeads": num_leads,
        "email": email
      }

      # Send to webhook and get response
      with st.spinner ("Processing your request..."): 
        response = send_to_webhook(payload)

      if response:
           #Update scraper Logs
           st.session_state.scraper_logs = response.get("scraperLogs", [])

           # Display success message
           st.success("Scraping pross initiated successfully!")

# Display scraper Logs
if st.session_state.scraper_logs: 
  st.subheader("Scraper Logs")
  log_container = st.container()

with log_container:
  for log in st.session_state.scraper_logs:
    timestamp = log.get("timestamp", "")
    message = log.get("message", "")
    level = log.get("level", "info")
    if level == "error":
      st.error(f"{timestamp}: {message}")
    elif level == "warning":
      st.warning(f" (timestamp): (message}")
    else:
      st.info(f" {timestamp}: {message}")
    
if __name__ == "__main()__":
  main()
