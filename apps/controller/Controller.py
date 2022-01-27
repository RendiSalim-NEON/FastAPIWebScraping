from apps.helper import Log
from apps.models import schema
from apps.schemas.Response import BaseResponse
from apps.schemas.SchemaCar import ResponseData
from ScrapingClass import ScrapeURL, ScrapeData, CleaningData
from apps.models.Models import Carsome
from main import PARAMS

SALT = PARAMS.SALT.salt

URL = "https://www.carsome.id/beli-mobil-bekas"


class Controller(object):
    @classmethod
    def get_url(cls, page = None):
        result = BaseResponse()
        result.status = 404
        url = f'{URL}?pageNo={str(page)}'
        request_url = ScrapeURL(url)
        
        try:
            if len(request_url.GetLinkDetail()) == 0 and page is not None:
                e = "THERE IS NO URL CAR"
                Log.error(e)
                result.message = str(e)
                
            elif page is None:
                e = "PAGE UNDEFINED"
                Log.error(e)
                result.message = str(e)

            else:
                result.status = 200
                result.message = "GET URL CAR"
                result.data =  request_url.GetLinkDetail()
                Log.info(result.message)

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    
    @classmethod
    def get_detail_page(cls, url = None):
        result = BaseResponse()
        result.status = 400

        try:
            if url is not None:
                request_car_url = ScrapeData(url)
                result.status = 200
                result.message = "SCRAPE DETAIL CAR"
                data = request_car_url.ScrapeDetail()
                result.data = CleaningData().Clean(data)
                
            else:
                e = "URL UNDEFINED"
                Log.error(e)
                result.message = str(e)

        except:
            m = "URL INVALID"
            Log.error(m)
            result.status = 400
            result.message = str(m)
           
        return result


    @classmethod
    def save_data(cls, data = None):
        result = BaseResponse()
        result.status = 400
        
        if not schema.has_table("CarsomeScraping1"):
            with schema.create("CarsomeScraping1") as table:
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
                table.integer("jumlah_tempat_duduk").nullable()
                table.date("tanggal_registrasi").nullable()
                table.string("tipe_registrasi").nullable()
                table.integer("jarak_tempuh_saat_ini").nullable()
                table.enum("kunci_cadangan", ["Ya", "Tidak"]).nullable()
                table.enum("buku_servis", ["Ya", "Tidak"]).nullable()
                table.string("kadaluwarsa_garansi_pabrik").nullable()
                table.enum("garansi_pabrik", ["Ya", "Tidak"]).nullable()
                table.date("masa_berlaku_stnk").nullable()
            
        try: 
            if (data is not None) and (data['url'] not in Carsome.lists("url")):
                Carsome.insert(data)
                result.status = 200
                result.data = data
                result.message = f"SAVE DATA FROM {data['url']}"
                Log.info(result.message)    

            elif data['url'] in Carsome.lists("url"):
                result.message = f"DATA ALREADY IN DATABASE"
                Log.info(result.message)

            else:
                e = "NO INPUT DATA"
                Log.error(e)
                result.message = str(e)


        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result


        
    @classmethod
    def get_car(cls, brand = None, tahun = None):
        result = BaseResponse()
        result.status = 400

        try:
            if (brand is not None and tahun is not None) and (brand in Carsome.lists("brand") and tahun in Carsome.lists("tahun")):
                data = Carsome.where("brand",brand).where("tahun",tahun).get().serialize()
                result.status = 200
                result.message = f"GET {brand} CAR AND {tahun} DATA"
                result.data = ResponseData(**{'result': data})

            elif brand is None and tahun is None:
                data = Carsome.get().serialize()
                result.status = 200
                result.message = f"GET ALL DATA"
                result.data = ResponseData(**{'result': data})

            elif brand is not None and brand in Carsome.lists("brand"):
                data = Carsome.where("brand", brand).get().serialize()
                result.status = 200
                result.message = f"GET {brand} CAR DATA"
                result.data = ResponseData(**{'result': data})
                
            elif tahun is not None and tahun in Carsome.lists("tahun"):
                data = Carsome.where("tahun", tahun).get().serialize()
                result.status = 200
                result.message = f"GET CAR DATA AT {tahun}"
                result.data = ResponseData(**{'result': data})

            else:
                e = "DATA NOT FOUND"
                result.status = 404
                Log.error(e)
                result.message = str(e)
                
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    
    @classmethod
    def update_data(cls, idcar = None, update_data = None):
        result = BaseResponse()
        result.status = 400

        try:
            if idcar is not None and idcar in Carsome.lists("id"):
                Carsome.where('id', idcar).update(update_data)
                result.status = 200
                result.message = f"UPDATE DATA BY ID: {idcar}"
                Log.info(result.message)

            else:
                e = "ID CAR NOT FOUND"
                result.status = 404
                Log.error(e)
                result.message = str(e)

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def delete_data(cls, idcar = None):
        result = BaseResponse()
        result.status = 400

        try:
            if idcar is not None and idcar in Carsome.lists("id"):
                Carsome.where('id', idcar).delete()
                result.status = 200
                result.message = f"DELETE CAR DATA BY ID: {idcar}"
                Log.info(result.message)

            else:
                e = "ID CAR NOT FOUND"
                result.status = 404
                Log.error(e)
                result.message = str(e)


        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result











        



