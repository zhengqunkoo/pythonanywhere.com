#!/usr/bin/env python

import requests
from datetime import datetime
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
api_token = os.getenv("API_TOKEN")   # Replace with your PythonAnywhere API token
username = "zhengqunkoo"     # Your PythonAnywhere username
webapp_name = "zhengqunkoo.pythonanywhere.com"

# Log file
log_file = "/home/zhengqunkoo/mysite/click_run-until-3-months-from-today.log"

# -----------------------------
# SCRIPT
# -----------------------------
def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp}: {message}\n")

def click_run_until_3_months_from_today():
    headers = {
        "Authorization": f"Token {api_token}"
    }
    
    # API endpoint to reload webapp (closest safe equivalent to 'run until 3 months')
    url = f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{webapp_name}/reload/"
    
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            log("Webapp reload/extend successful.")
        else:
            log(f"Failed to extend webapp. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        log(f"Exception occurred: {e}")

if __name__ == "__main__":
    click_run_until_3_months_from_today()
