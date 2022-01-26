import json
from fastapi import APIRouter, Body, Response
from typing import Optional
from apps.controller.Controller import Controller as Control

router = APIRouter()


update_data = json.dumps({
    "brand": "Honda",
    "model": "BRIO RS 1.2",
    "tahun": "2018",
    "lokasi": "Kelapa Gading, Jakarta Utara",
    "harga": "135850000",
    "gambar": "https://prod-carsome-id.imgix.net/B2C/439cdfc7-606e-4a2a-83f7-31c3657f38b0.jpg?q=20&w=2400&auto=format",
    "url": "https://www.carsome.id/beli-mobil-bekas/honda/brio/2016-honda-brio-rs-1.2/c4k0000",
    "jenis_bahan_bakar": "Bensin",
    "warna": "Lainnya",
    "jumlah_tempat_duduk": "5",
    "tanggal_registrasi": "01-11-2016",
    "tipe_registrasi": "Perorangan",
    "jarak_tempuh_saat_ini": "53495",
    "kunci_cadangan": "Ya",
    "buku_servis": "Ya",
    "garansi_pabrik": "Tidak",
    "masa_berlaku_stnk": "01-09-2022"
}, indent = 2)

@router.get("/scrape_url_car/")
async def scraping_url(response: Response, page:Optional[int] = None):
    result = Control.get_url(page = page)
    response.status_code = result.status
    return result

@router.get('/scrape_car_detail/')
async def scraping_detail(response: Response, url:Optional[str]=None):
    result = Control.get_detail_page(url = url)
    response.status_code = result.status
    return result

@router.get('/read_data/')
async def read_data(response: Response, brand:Optional[str] = None, tahun:Optional[str] = None):
    result = Control.get_car(brand = brand, tahun = tahun)
    response.status_code = result.status
    return result

@router.post('/save_data_detail/')
async def save_detail(response: Response, data = Body(...)):
    result = Control.save_data(data = data)
    return result

@router.put('/update_data/')
async def update_data(response: Response, idcar:Optional[str], update_data = Body(..., example=update_data)):
    result = Control.update_data(idcar = idcar, update_data = update_data)
    return result

@router.delete('/delete_data/')
async def delete_data(response: Response, idcar:Optional[str]):
    result = Control.delete_data(idcar = idcar)
    return result
