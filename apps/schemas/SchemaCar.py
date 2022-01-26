from unittest import result
from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class RequestData(BaseModel):
    id: str = None
    brand: str = None 
    model: str = None 
    tahun: str = None
    lokasi: str = None 
    harga: float = None 
    gambar: str = None 
    url: str = None
    jenis_bahan_bakar: str = None
    warna: str = None
    jumlah_tempat_duduk: str = None 
    tanggal_registrasi: date = None 
    tipe_registrasi: str = None 
    jarak_tempuh_saat_ini: int = None
    kunci_cadangan: str = None
    buku_servis: str = None
    kadaluwarsa_garansi_pabrik: str = None
    garansi_pabrik: str = None
    masa_berlaku_stnk: date = None

class ResponseData(BaseModel):
    result: List[RequestData]