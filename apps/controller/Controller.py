from lib2to3.pytree import Base
from fastapi import exceptions
from orator.exceptions.query import QueryException
from apps.helper import Log
from apps.models import schema
from apps.schemas.Response import BaseResponse
from ScrapingClass import ScrapeURL, ScrapeData, CleaningData
from apps.models.Models import Carsome

URL = "https://www.carsome.id/beli-mobil-bekas"
CONNECTION = ScrapeURL(URL)
CONNECTION_DB = "postgresql://postgres:admin12345678@localhost:5432/postgres"


class Controller(object):
    @classmethod
    def get_url(cls, page = None):
        result = BaseResponse()
        result.status = 404
        url = URL + "?pageNo=" + str(page)
        request_url = ScrapeURL(url)
        
        try:
            if len(request_url.GetLinkDetail()) == 0:
                result.message = "There is no car data in this page"
            else:
                result.status = 200
                result.message = "Success get URL data"
                result.data =  request_url.GetLinkDetail()
            
            Log.info(result.message)
        except:
            m = "Error"
            Log.error(m)
            result.status = 400
            result.message = str(m)

        return result

    
    @classmethod
    def get_detail_page(cls, url = None):
        result = BaseResponse()
        result.status = 400

        try:
            if url is not None:
                request_car_url = ScrapeData(url)
                result.status = 200
                result.message = "Success scrape all car data"
                data = request_car_url.ScrapeDetail()
                result.data = CleaningData().Clean(data)

            else:
                result.message = "There are no URL"

            Log.info(result.message)
        except:
            m = "Invalid URL"
            Log.error(m)
            result.message = str(m)

        return result


    @classmethod
    def save_data(cls, data = None):
        result = BaseResponse()
        result.status = 400
        
        if not schema.has_table("CarsomeScraping"):
            with schema.create("CarsomeScraping") as table:
                table.string("id")
                table.string("brand")
                table.string("model")
                table.string("tahun").nullable()
                table.string("lokasi").nullable()
                table.float("harga")
                table.long_text("gambar").nullable()
                table.long_text("url").nullable()
                table.char("jenis_bahan_bakar", 10).nullable()
                table.string("warna").nullable()
                table.string("jumlah_tempat_duduk").nullable()
                table.date("tanggal_registrasi").nullable()
                table.string("tipe_registrasi").nullable()
                table.string("jarak_tempuh_saat_ini").nullable()
                table.enum("kunci_cadangan", ["Ya", "Tidak"]).nullable()
                table.enum("buku_servis", ["Ya", "Tidak"]).nullable()
                table.date("kadaluwarsa_garansi_pabrik").nullable()
                table.enum("garansi_pabrik", ["Ya", "Tidak"]).nullable()
                table.date("masa_berlaku_stnk").nullable()
            
        try: 
            if (data is not None) and (data['url'] not in Carsome.lists("url")):
                Carsome.insert(data)
                result.status = 200
                result.data = data
                result.message = f"Success Save data from {data['url']}"
            elif data['url'] in Carsome.lists("url"):
                result.message = f"Data from {data['url']} already in database"
            else:
                result.message = f"There are no input data"

            Log.info(result.message)

        except QueryException:
            m = "column Id, brand, model, and harga is null"
            result.status = 400
            Log.error(m)
            result.message = str(m)
        
        except:
            m = "Error"
            result.status = 400
            Log.error(m)
            result.message = str(m)

        return result


        
    @classmethod
    def get_car(cls, brand = None, tahun = None):
        result = BaseResponse()
        result.status = 400

        if (brand is not None and tahun is not None) and (brand in Carsome.lists("brand") and tahun in Carsome.lists("tahun")):
            data = Carsome.where("brand",brand).where("tahun",tahun).get().serialize()
            result.status = 200
            result.message = f"Success get car data, brand:{brand.title()} and tahun: {tahun}"
            result.data = data

        elif brand is None and tahun is None:
            data = Carsome.get().serialize()
            result.status = 200
            result.message = f"Success get all car data, brand:{brand} and tahun: {tahun}"
            result.data = data

        elif brand is not None and brand in Carsome.lists("brand"):
            data = Carsome.where("brand", brand.title()).get().serialize()
            result.status = 200
            result.message = f"Success get all car data, brand:{brand}"
            result.data = data
            
        elif tahun is not None and tahun in Carsome.lists("tahun"):
            data = Carsome.where("tahun", tahun).get().serialize()
            result.status = 200
            result.message = f"Success get all car data, brand:{brand}"
            result.data = data

        else:
            result.status = 404
            result.message = f"Data Not Found"

        return result

    
    @classmethod
    def update_data(cls, idcar = None, update_data = None):
        result = BaseResponse()
        result.status = 400

        try:
            if idcar is not None and idcar in Carsome.lists("id"):
                Carsome.where('id', idcar).update(update_data)
                result.status = 200
                result.message = f"Update data by idcar: {idcar}"
            else:
                result.status = 404
                result.message = "id car not found"
            
            Log.info(result.message)

        except:
            m = "Error"
            Log.error(m)
            result.status = 400
            result.message = str(m)

        return result

    @classmethod
    def delete_data(cls, idcar = None):
        result = BaseResponse()
        result.status = 400

        try:
            if idcar is not None and idcar in Carsome.lists("id"):
                Carsome.where('id', idcar).delete()
                result.status = 200
                result.message = f"Success Delete data by car id: {idcar}"
            else:
                result.status = 404
                result.message = "car id not found"
            Log.info(result.message)

        except:
            m = "Error"
            Log.error(m)
            result.status = 400
            result.message = str(m)

        return result











        



