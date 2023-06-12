# hava-durumu-telegram-botu
Simple weather project for web scraping using requests and beautiful soup via python-telegram-bot

[![Ekran Resmi](./video.mp4)](./video.mp4)


# Index
0. [https://t.me/ExampleMyWeatherBot](https://t.me/ExampleMyWeatherBot )
1. [Installation](#installation)
2. [Setup](#setup)
3. [Purpose](#project-purpose)


## Installation
ilk önce bağımlı kütüphaneleri yüklüyoruz.
```
pip3 install -r requirements.txt    
```
Çalıştırma:
```
python3 main.py
```
## Setup
- Kendi oluşturmak isteyen kullanıcılar için..

1. Telegramdan [BotFather](https://t.me/BotFather) dan yeni bir bot oluşturuyoruz.
2. [main.py](main.py) dosyasında main fonksiyonu 105.satırdaki string ifadeye  bot token'ı  [BotFather](https://t.me/BotFather)dan aldığımız yeni botun token'ını yazıyoruz
4. İster kendi server'ına python kurup da çalıştır ister local çalıştır kendi botunun keyfini çıkar

**önemli nokta:** bot oluşturunca hazır komutları oluşturmayı da unutmayın...
- Kendi kullandığım garantisi olmayan kendi botumu kullanmak isteyen kullanıcılar için
 
    #### Bağlantı: [ExampleMyWeatherBot](https://t.me/ExampleMyWeatherBot )


## Project Purpose
Kısaca Amacı:
    Google ve MGM(Meteroloji Genel Müdürlüğü)yi kullanarak scraping işlemi sonucu hava durumlarını (iki ayrı kaynaktan) tek bir kaynağa (Telegram botunda) çıktısını veren basit bir hava durumu uygulaması.


*Çalışma Adımları* 


1. Konuşmaya başlayınca (**start** gelecek) ve soracak bana **'Hava Durumuna Hoşgeldiniz, lütfen ilinizi yazınız: '** şeklinde. 
2. Il bilgilerini alınca ilçeler listesini getirecek telegrambot - inline keyboards  ile 
3. Il ve ilçe parametreleri sonucunda hava durumunu döndürecek ve ne zaman **"\sondurum"** komutu yazarsa hava durumunu getirecek olay bu


