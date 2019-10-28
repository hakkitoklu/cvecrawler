#cvedetails.com üzerinden tüm zaafiyetlerle ilgili bilgileri çekerek mysql veritabanına aktaran script.
from bs4 import BeautifulSoup
import requests
import pandas as pd
from database import db
from openpyxl.workbook import workbook
#Score değerlerine göre sınıflandırılmış sayfaların linkleri
urls = ["https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=9&cvssscoremax=10&year=0&month=0&cweid=0&order=1&trc=16185&sha=c560d509f935c26128bfb13d2f2dadfcea62215b",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=8&cvssscoremax=8.99&year=0&month=0&cweid=0&order=1&trc=553&sha=47211ec39e8a5bfc696c510450016af4d6c6f60d",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=7&cvssscoremax=7.99&year=0&month=0&cweid=0&order=1&trc=27369&sha=8d1dce4336dc15b67abd26e84cfd7dee885ac426",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=6&cvssscoremax=6.99&year=0&month=0&cweid=0&order=1&trc=17054&sha=74e0bf73b5c24af1d8fa0497960c60660de4f638",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=5&cvssscoremax=5.99&year=0&month=0&cweid=0&order=1&trc=23785&sha=487699e41035ffbb827ae68be83ace9ccd82c221",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=4&cvssscoremax=4.99&year=0&month=0&cweid=0&order=1&trc=27455&sha=24a76f217bca516d9ddb84350e69616cb8f78973",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=3&cvssscoremax=3.99&year=0&month=0&cweid=0&order=1&trc=4556&sha=a5f82bbf2e3b4c1a44673f277621d24e63e478cb",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=2&cvssscoremax=2.99&year=0&month=0&cweid=0&order=1&trc=4880&sha=309000079e74eb94dd19bab74ae6ee2280672c3b",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=1&cvssscoremax=1.99&year=0&month=0&cweid=0&order=1&trc=914&sha=2ee333910b0146938c917d67aa60489f458567df",
"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0.99&year=0&month=0&cweid=0&order=1&trc=703&sha=8cc1914b56963dbe370dba9383f2100c35cf3354"]


def craw(url,pn):
  for page in range(1,pn+1):
        try:
            r = requests.get(url.replace('page=1', 'page=' + str(page)))
            pagetext = r.text
            soup = BeautifulSoup(pagetext, 'html.parser')
            vuln_table = soup.find("table", {"id": "vulnslisttable"})
            list = []
            for i in vuln_table.find_all('td'):
                a = i.text
                a = a.replace('\n', "")
                a = a.replace("\t", "")
                list.append(a)
        except Error as e:
            print("Error : {}".format(e))
        return list
#Tabloda her girdi için 16 değer bulunuyor.Listeye ise her değeri 0 indisinden başlayarak sırayla her değeri
# yeni indise yazarak aldığından döngü aşağıdaki gibi yazılmıştır.Her 16 değerde bir diğer girdiye geçiyor.

#SQL INSERT DÖNGÜSÜ

        """for i in range(0, len(list), 16):
            try:
                db.insert(str(list[i + 1]), str(list[i + 2]), str(list[i + 4]), str(list[i + 5]),
                          str(list[i + 6]), str(list[i + 7]), str(list[i + 9]), str(list[i + 15]))
            except Error as e:
                print("DÖNGÜ PROBLEMİ : {}".format(e))"""

#En son sayfa numarasını bulmak için
def find_last_pn(url):
    r = requests.get(url)
    pagetext = r.text
    soup = BeautifulSoup(pagetext, 'html.parser')
    crawled_page = soup.find("div", {"id": "pagingb", "class": "paging"})
    page_list = []
    for say in crawled_page.find_all('a'):
        a = say.text
        page_list.append(a)
    lpn=int(page_list[-1])
    return lpn
db=db()
s_name=input("Aranan zafiyet başlığı :")   #Example : Linaro
s_version=input("Aranan zafiyet versiyonu :") #Example : 3.3.0


db_data=db.db_get(str(s_name),str(s_version))
#Alınan verileri tablo halinde excel dosyasına aktarma
df=pd.DataFrame(db_data)
excel=df.to_excel(r'path',index=None,header=True)

for url in urls:
    craw(url,find_last_pn(url))