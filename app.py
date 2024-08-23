import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scraper import SteamStoreScraper 

app = FastAPI()

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

class Game(BaseModel):
    Name: str
    Date: str
    Platforms: list
    Original_Price: str
    Discount_Percentage: str
    Discount_Price: str
    Reviews: str
    Review_Count: str

def get_region_from_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return data.get("countryCode", "IN")
    except Exception as e:
        print(f"Error fetching region: {e}")
        return "IN"

@app.get("/", response_model=list[Game])
def get_discounted_games_default(request: Request):
    scraper = SteamStoreScraper()
    games = scraper.ScrapeGames(n0Games=30)
    count = len(games)
    return templates.TemplateResponse("index.html", {"request": request, "games": games, "count": count})

@app.get("/{n}", response_model=list[Game])
def get_discounted_games(request: Request, n: int):
    scraper = SteamStoreScraper()
    games = scraper.ScrapeGames(n0Games=n)
    count = len(games)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return templates.TemplateResponse("index.html", {"request": request, "games": games}, media_type="text/html")
    else:
        return templates.TemplateResponse("index.html", {"request": request, "games": games, "count": count})
