from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {GITHUB_TOKEN}"}



@app.get("/github-users")
def get_github_users(request: Request, page: int = 1):
    per_page = 5
    url = f"https://api.github.com/users?per_page={per_page}&since={(page-1)*per_page}"
    response = requests.get(url)
    users = response.json()
    return templates.TemplateResponse("user.html", {"request": request, "users": users, "page": page})



@app.get("/github-user/{username}")
def github_user_detail(request: Request, username: str):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    user = response.json()
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})



@app.get("/github-user/{username}/orgs")
def github_user_orgs(request: Request, username: str):
    url = f"https://api.github.com/users/{username}/orgs"
    response = requests.get(url, headers=headers)
    orgs = response.json()
    return templates.TemplateResponse("user_orgs.html", {"request": request, "orgs": orgs, "username": username})