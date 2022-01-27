# Carsome Web Scraping
Project ini dibuat untuk mengambil informasi mobil bekas dari website yang bernama [Carsome](https://www.carsome.id/beli-mobil-bekas). Setelah Web Scraping dilakukan, data tersebut juga dapat disimpan dalam sebuah postgres database. Web scraping dapat dilakukan dengan memanggil API yang sudah dibuat. Berikut beberapa API yang sudah dibuat:
* scrape_url_car: digunakan untuk mengambil URL mengenai detail mobil
* scrape_car_detail: digunakan untuk mengambil detail dari mobil bekas
* read_data: digunakan untuk mengambil data mobil yang sudah tersimpan di database
* save_data_detail: digunakan untuk menyimpan data mobil yang belum ada di database
* update_data: digunakan untuk mengupdate data dari mobil yang ada di database
* delete_data: digunakan untuk menghapus data dari mobil yang ada di database


## Content:
1. ScrapingCarSome: Code yang digunakan untuk membuat FastAPI dan melakukan scarping pada [Carsome](https://www.carsome.id/beli-mobil-bekas)
1. FastAPITest: Code yang digunakan untuk melakukan pengetesan terhadap FastAPI yang sudah dibuat

## Result:
Hasil akhir dari project ini dirangkum dalam bentuk dashboard yang ada pada **Metabase**