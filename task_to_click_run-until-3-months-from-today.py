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
task_command = "/home/zhengqunkoo/mysite/task_to_click_run-until-3-months-from-today.py" # Task to run
task_hour = 16 # Scheduled hour
task_minute = 0 # Scheduled minute

# Log file
log_file = "/home/zhengqunkoo/mysite/click_run-until-3-months-from-today.log"

# API endpoints
scheduled_tasks_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/schedule/"
reload_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{webapp_name}/reload/"

# -----------------------------
# HELPERS
# -----------------------------
def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp}: {message}\n")

def get_existing_tasks():
    """
    Get information of current tasks.
    Note that in the response body there is an undocumented API `{"extend_url":"/user/zhengqunkoo/schedule/task/1282479/extend"}`.
    """
    headers = {"Authorization": f"Token {api_token}"}
    response = requests.get(scheduled_tasks_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log(f"Failed to get existing tasks: {response.status_code} {response.text}")
        return []

def delete_task(task_id):
    headers = {"Authorization": f"Token {api_token}"}
    delete_url = f"{scheduled_tasks_url}{task_id}/"
    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 204:
        log(f"Deleted task {task_id} successfully")
    else:
        log(f"Failed to delete task {task_id}: {response.status_code} {response.text}")

def create_task():
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "command": task_command,
        "interval": "daily",
        "hour": task_hour,
        "minute": task_minute
    }
    response = requests.post(scheduled_tasks_url, headers=headers, json=payload)
    if response.status_code == 201:
        log("Task created successfully")
    else:
        log(f"Failed to create task: {response.status_code} {response.text}")

# -----------------------------
# MAIN SCRIPT
# -----------------------------
def click_run_until_3_months_from_today():
    headers = {
        "Authorization": f"Token {api_token}"
    }
    
    try:
        response = requests.post(reload_url, headers=headers)
        if response.status_code == 200:
            log("Webapp reload/extend successful.")
        else:
            log(f"Failed to extend webapp. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        log(f"Exception occurred: {e}")

def reschedule_task():
    tasks = get_existing_tasks()
    # Delete tasks that match our command to avoid duplicates
    for task in tasks:
        if task.get("command") == task_command:
            delete_task(task.get("id"))
    # Create new task
    create_task()

if __name__ == "__main__":
    click_run_until_3_months_from_today()
    reschedule_task()
