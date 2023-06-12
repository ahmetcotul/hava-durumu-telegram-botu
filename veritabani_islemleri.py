import sqlite3


conn = sqlite3.connect('veritabani.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS kullanicilar
(kullanici_id INTEGER PRIMARY KEY,ad TEXT, soyad TEXT,il TEXT,ilce TEXT)
''')
conn.commit()
conn.close()


def kullanici_var_mi(user_id):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("SELECT ad, soyad FROM kullanicilar WHERE kullanici_id = ?", (user_id,))
    result=  c.fetchone()
    conn.close()
    return result
def kullanici_ekle(user_id,name,last_name):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("INSERT INTO kullanicilar (kullanici_id,ad,soyad) VALUES (?,?,?)", (user_id, name, last_name))
    conn.commit()
    print("kullanıcı eklendi")
    conn.close()

def il_ekle(il,kullanici_id):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("UPDATE kullanicilar SET il = ? WHERE kullanici_id=?",(il,kullanici_id))
    conn.commit()
    conn.close()
def ilce_ekle(ilce,user_id):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("UPDATE kullanicilar SET ilce = ? WHERE kullanici_id=?",(ilce,user_id))
    conn.commit()
    conn.close()


def ili_cek(user_id):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("SELECT il FROM kullanicilar WHERE kullanici_id = ?",(user_id,))
    il = c.fetchone()
    conn.commit()
    conn.close()
    return il[0]
def ilceyi_cek(user_id):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("SELECT ilce FROM kullanicilar WHERE kullanici_id = ?", (user_id,))
    ilce = c.fetchone()
    conn.commit()
    conn.close()
    return ilce[0]
