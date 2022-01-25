from unittest import result
from fastapi import APIRouter, Body, Response
from typing import Optional
from apps.controller.Controller import Controller as Control



router = APIRouter()

# @router.post("/scrape_from_carsome/{endpoint}")
# async def scraping(response: Response, endpage:Optional[int] = None):
#     result = Control.CreateDatabase(endpage = endpage)
#     response.status_code = result.status
#     return result

@router.get("/scrape_url_car/{page}")
async def scraping_url(response: Response, page:int = None):
    result = Control.get_url(page = page)
    response.status_code = result.status
    return result

@router.get('/scrape_car_detail/')
async def scraping_detail(response: Response, url:Optional[str]=None):
    result = Control.get_detail_page(url = url)
    response.status_code = result.status
    return result

@router.post('/save_data_detail')
async def save_detail(response: Response, data = Body(...)):
    result = Control.save_data(data = data)
    return result

