import hava_durumu as hd
import connectly
import requests
def ileGoreIlceListesi(il):
    params = {
        'il': il
    }
    response_temp = connectly.get_legacy_session().get('https://servis.mgm.gov.tr/web/merkezler', params=params, headers=hd.headers)
    json_temp_data= response_temp.json()[0]

    ilceler_url = "https://raw.githubusercontent.com/isubas/iller_ve_ilceler/master/iller_ve_ilceler.json"
    resp_ilce = requests.get(ilceler_url)
    ilce_data = resp_ilce.json()
    plaka = str(json_temp_data["ilPlaka"])

    ilce_isimler = []
    for i in ilce_data[plaka]["ilceler"]:
        ilce_isimler.append(i["ad"])
    return ilce_isimler


