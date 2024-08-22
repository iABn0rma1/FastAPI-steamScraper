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
def get_discounted_games(request: Request, n: int = 50):
    scraper = SteamStoreScraper()
    games = scraper.ScrapeGames(n0Games=n)
    return templates.TemplateResponse("index.html", {"request": request, "games": games})