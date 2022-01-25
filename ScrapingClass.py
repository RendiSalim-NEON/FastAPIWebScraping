from bs4 import BeautifulSoup
import requests
from datetime import datetime

## Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.58',
    'Accept-Encoding': 'Content-Encoding'
}


class ScrapeURL(): #connection
    def __init__(self, link):
        self.link = requests.get(link, headers=HEADERS, verify=False).text
        self.soup = BeautifulSoup(self.link, 'lxml')

    def GetLinkDetail(self):
        return [f'https://www.carsome.id{url["href"]}' for url in self.soup.find_all("a", class_="mod-card__head")]



class ScrapeData(ScrapeURL):
    def __init__(self, link):
        super().__init__(link)
        self.url = link

    def ScrapeDetail(self):
        CarData = {}
        CarTitle = self.soup.find("div", class_ ="v-responsive").get("aria-label").split()

        CarData['id'] = self.soup.find("span",class_="id-text").getText().split()[-1]
        CarData['brand'] = CarTitle[1]
        CarData['model'] = " ".join(CarTitle[2:-1])
        CarData['tahun'] = CarTitle[0]
        CarData['lokasi'] = self.soup.select_one("div.location-desc").getText().replace("Carsome ","")
        CarData['harga'] = self.soup.find("span", class_="price").getText().strip().split()[-1].replace(".", "")
        CarData['gambar'] = self.soup.find("div", class_='car-swiper-slide').img.get('src')
        CarData['url'] = self.url
        keySpec = [key.getText().replace(" ","_").lower() for key in self.soup.find_all("span", class_ = "key")]
        valueSpec = [value.getText() for value in  self.soup.find_all("span", class_ = "value")]

        for i in range(len(keySpec)):
            CarData[keySpec[i]] = valueSpec[i]

        return CarData

class CleaningData():
    def __init__(self):
        self.month = {
            "Jan": "Jan",
            "Feb": "Feb",
            "Mar": "Mar",
            "Apr": "Apr",
            "Mei": "May",
            "Jun": "Jun",
            "Jul": "Jul",
            "Agt": "Agt",
            "Sep": "Sep",
            "Okt": "Oct",
            "Nov": "Nov",
            "Des": "Dec"
        }

    def DateFormat(self, data):
        if data is not None:
            CleanData = self.month[data.split()[0]] + " " + data.split()[1]
            return datetime.strptime(CleanData, "%b %Y").strftime("%d-%m-%Y")
        return data

    def Clean(self, data):
        data['jumlah_tempat_duduk'] = data['jumlah_tempat_duduk'][0]
        data['jarak_tempuh_saat_ini'] = data['jarak_tempuh_saat_ini'].replace(".", "").split()[0]
        data['tanggal_registrasi'] = self.DateFormat(data['tanggal_registrasi'])
        data['masa_berlaku_stnk'] = self.DateFormat(data['masa_berlaku_stnk'])
        return data







