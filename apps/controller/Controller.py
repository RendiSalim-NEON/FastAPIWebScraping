import pandas as pd
import sqlalchemy
from apps.helper import Log
from apps.models import schema
from apps.schemas.Response import BaseResponse
from ScrapingClass import ScrapeURL, ScrapeData, CleaningData
from apps.models.Models import Carsome

URL = "https://www.carsome.id/beli-mobil-bekas"
CONNECTION = ScrapeURL(URL)
CONNECTION_DB = "postgresql://postgres:admin12345678@localhost:5432/postgres"


class Controller(object):
    # @classmethod
    # def CreateDatabase(cls, endpage = None):
    #     result = BaseResponse()
    #     result.status = 400


    #     if not schema.has_table("CarsomeScraping"):
    #         DATA = []

    #         if endpage is None:
    #             endpage = CONNECTION.LastPage()

    #         # Scrape Data
    #         for page in range(1, endpage+1):
    #             UrlPage = URL + "?pageNo=" + str(page)
    #             UrlConnection = ScrapeURL(UrlPage)
    #             CarUrl = UrlConnection.ScrapeCarURL()

    #             for url in CarUrl:
    #                 scrape = ScrapeData(url).ScrapeDetail()
    #                 DATA.append(scrape)

    #         # Data Cleansing -> buat function
    #         df = pd.DataFrame(DATA)
    #         df['Jumlah Tempat Duduk'] = df['Jumlah Tempat Duduk'].apply(lambda x: x[0] if len(x) > 1 else x)
    #         # df['Tanggal Registrasi'] = pd.to_datetime(df['Tanggal Registrasi']).dt.strftime("%Y-%m")
    #         df['Jarak Tempuh Saat Ini'] = df['Jarak Tempuh Saat Ini'].apply(lambda x: x.replace(".", "").split()[0])

    #         # import result to sql 
    #         engine = sqlalchemy.create_engine(CONNECTION_DB)
    #         df.to_sql("CarsomeScraping", 
    #                 engine,
    #                 schema='public',
    #                 if_exists="replace",
    #                 index = False)
    #         result.status = 200
    #         result.message = "Scraping and Create Database Success"
    #         result.data = Carsome.get().serialize()
    #         Log.info(result.message)
        
    #     result.message = 'Database has'

    #     return result

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
                table.integer("tahun")
                table.float("harga")
                table.long_text("gambar")
                table.long_text("url")
                table.char("jenis_bahan_bakar", 10)
                table.string("warna")
                table.string("jumlah_tempat_duduk")
                table.date("tanggal_registrasi")
                table.string("tipe_registrasi")
                table.string("jarak_tempuh_saat_ini")
                table.enum("kunci_cadangan", ["Ya", "Tidak"])
                table.enum("buku_servis", ["Ya", "Tidak"])
                table.date("kadaluwarsa_garansi_pabrik")
                table.date("masa_berlaku_stnk")
        
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

        return result












        



