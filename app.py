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

@app.get("/", response_model=list[Game])
async def get_discounted_games(request: Request, n: int = 50, offset: int = 0):
    client_ip = request.client.host
    region = get_region_from_ip(client_ip)
    scraper = SteamStoreScraper(region=region)
    games = scraper.ScrapeGames(n0Games=n, offset=offset)
    count = len(games)
    return templates.TemplateResponse("index.html", {"request": request, "games": games, "count": count})

def get_region_from_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return data.get("countryCode", "IN")
    except Exception as e:
        print(f"Error fetching region: {e}")
        return "IN"
