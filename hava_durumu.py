import connectly
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# fake user-agent
ua = UserAgent()

# hadiseye göre sınıflandırma
hadiseler = {"A":"Açık","AB":"Az Bulutlu",
             "D":"Dumanlı","HY":"Hafif Yağmurlu","HSY":"Hafif Sağnak Yağışlı",
             "HKY":"Hafif Kar Yağışlı","YYSY":"Yer Yer Sağnak Yağışlı",
             "KKY":"Karla Karışık Yağmurlu","GKR":"Güneyli Kuvvetli Rüzgar",
             "PB":"Parçalı Bulutlu","PUS":"Puslu","Y":"Yağmurlu","SY":"Sağanak Yağışlı",
             "KY":"Kar Yağışlı","R":"Rüzgarlı","KKR":"Kuzeyli Kuvvetli Rüzgar",
             "CB":"Çok Bulutlu","S":"Sis","KY":"Kuvvetli Yağmurlu","KSY":"Kuvvetli Sağanak Yağışlı",
             "YKY":"Yoğun Kar Yağışlı","GSY":"Gök Gürültülü Sağnak Yağışlı","TF":"Toz veya Kum Fırtınası",
             "KGSY":"Kuvvetli Gökgürültülü Sağanak Yağışlı",
             }

# headers
headers = {
            'User-Agent': ua.chrome,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://www.mgm.gov.tr/',
            'Origin': 'https://www.mgm.gov.tr',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
    }
#METEROLOJI GENEL MUDURLUGU VERILERINE GORE SCRAPING ISLEMI
def mgm(il, ilce=""):
    if ilce.strip().lower()=="merkez":
        ilce=""
    params_city = {
        'il': il,
        'ilce':ilce
    }
    try:
        response_temp = connectly.get_legacy_session().get('https://servis.mgm.gov.tr/web/merkezler', params=params_city, headers=headers)
        jsonTempData = response_temp.json()[0]
    except:
        return "Yanlış sorgu"
    
    params_id = {
        'merkezid': jsonTempData["merkezId"],
    }
    response_mgm = connectly.get_legacy_session().get('https://servis.mgm.gov.tr/web/sondurumlar', params=params_id, headers=headers)
    jsonData = response_mgm.json()[0]

    #veriler en önemlisi
    sehir = jsonTempData['il']
    ilce = jsonTempData['ilce']
    sicaklik = jsonData['sicaklik']
    hadisekodu = jsonData['hadiseKodu']
    #yagis =str(float(jsonData['yagis6Saat']))[2:]
    olcumZamani = jsonData["veriZamani"][11:16]
    nemOrani = jsonData["nem"]

    try:
        hadise = hadiseler[hadisekodu]
    except:
        hadise = ""
    return f"""MGM(Meteroloji Genel Müdürlüğü)ne göre:{sehir},{ilce}
Ölçüm saati={olcumZamani}
Nem Oranı={nemOrani}%
Sıcaklık={sicaklik}°C
{hadise}"""

#GOOGLE VERILERINE GORE
def google_veri(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",il="",ilce=""):
    response_google= connectly.get_legacy_session().get(f"https://www.google.com/search?q={il}+{ilce}+hava+durumu+",headers={'user-agent':user_agent,'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',},verify=True)
    parser = BeautifulSoup(response_google.text,"html.parser")
    durum = parser.find("span", {"id": "wob_dc"})
    weather = parser.find("span",{"class":"wob_t q8U8x"}).text
    #eger cevirmeye gerekli olursa
    #weather = parser.find("span",{"class":"wob_t q8U8x"}).text
    #weather = (int(weather) -32 ) * 5.0/9.0
    #weather = round(weather,1)
    zaman = parser.find("div",{"class":"wob_dts"})
    yagis_ihtimali = parser.find("span", {"id": "wob_pp"})
    return f"""\n
Google weather.com verilerine göre:{il.capitalize()},{ilce.capitalize()}
Ölçüm zamanı={zaman.text}
Sıcaklık={weather}°C
Yağış İhtimali={yagis_ihtimali.text}
{durum.text}"""
