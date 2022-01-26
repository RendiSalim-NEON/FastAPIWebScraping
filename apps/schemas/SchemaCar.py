import enum
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
    tanggal_registrasi: str = None 
    tipe_registrasi: str = None 
    jarak_tempuh_saat_ini: int = None
    kunci_cadangan: bool = None
    buku_servis: bool = None
    kadaluwarsa_garansi_pabrik: str = None
    garansi_pabrik: bool = None
    masa_berlaku_stnk: str = None

class ResponseData(BaseModel):
    data: List[RequestData]