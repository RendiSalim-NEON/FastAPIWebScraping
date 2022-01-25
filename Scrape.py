import pandas as pd
import sqlalchemy
from ScrapingClass import ScrapeURL, ScrapeData


URL = "https://www.carsome.id/beli-mobil-bekas?pageNo=33"
DATA = []
CONNECTION_DB = "postgresql://postgres:admin12345678@localhost:5432/postgres"


# for page in range(1, 2):
#     UrlPage = URL + str(page)
#     UrlConnection = ScrapeURL(UrlPage)
#     CarUrl = UrlConnection.ScrapeCarURL()

#     for url in CarUrl:
#         scrape = ScrapeData(url).ScrapeDetail()
#         DATA.append(scrape)
        
#     print(f"Done Scrape for Page {page}")


# df = pd.DataFrame(DATA)
# df['jumlah_tempat_duduk'] = df['jumlah_tempat_duduk'].apply(lambda x: x[0] if len(x) > 1 else x)
# # df['Tanggal Registrasi'] = pd.to_datetime(df['Tanggal Registrasi']).dt.strftime("%Y-%m")
# df['jarak_tempuh_saat_ini'] = df['jarak_tempuh_saat_ini'].apply(lambda x: x.replace(".", "").split()[0])
# print(df.head())

CONNECTION = ScrapeURL("https://www.carsome.id/beli-mobil-bekas")
print(CONNECTION.LastPage())

# engine = sqlalchemy.create_engine(CONNECTION_DB)
# df.to_sql("CarsomeScraping", 
#             engine,
#             schema='public',
#             if_exists="replace",
#             index = False)