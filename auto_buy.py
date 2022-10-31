from itertools import product
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Excel verilerini okunup list haline getirildiği fonksiyon bloğu
def excel_read():
    df = pd.read_excel('keywords.xlsx', sheet_name='Sheet1')
    product_list = df.values.tolist()
    return product_list

# Chromium popup ve uyarıları/bildirileri kapattığımız ve ekranı tam ekran yaptırdığımız fonksiyon bloğu																													 
def webOptions():
    customOptions = webdriver.ChromeOptions()
    customOptions.add_argument("--disable-notifications") # Uyarı ve Bildirimlerin Kapatılması
    customOptions.add_argument("--disable-popup-blocking")# Pop-Upların kapatılması
    customOptions.add_argument("--start-maximized")       # Tam Ekran yapılması
    return customOptions

# Bütün ürünlerin bulunduğu ana ekranda sepete ekle butonu bulunmadığı takdirde sayfaya yönlendirme yapılıp
# ürün sayfasında sepete ekleme işleminin yapıldığı fonksiyon bloğu.
def go_product_page(path):

    try:

        driver.get(path)# Sayfaya gider.																  
        add_to_basket = driver.find_element(By.XPATH,"//button[@class='add-to-basket']")
        add_to_basket.click()   # Sepete ekler.
    except:
        print("There is not add to basket button")

# Ürün ekleme fonksiyon bloğu.
# Bazı elementleri Class ismi bazılarını Xpath ile bulmaktadır.								 																	
def add_product(product_name):
    print("Trying to buy " + product_name + " keyword")
    try:
        driver.get('https://www.trendyol.com/sr?q='+str(product_name)+'&qt='+str(product_name)+'&st='+str(product_name)+'&os=1')
        if driver.find_element(By.XPATH,'//*[@id="search-app"]').get_attribute('id') == 'search-app':
            driver.get('https://www.trendyol.com/sr?q='+str(product_name)+'&qt='+str(product_name)+'&st='+str(product_name)+'&os=1&fc=true&sst=MOST_RATED')
            time.sleep(0.5)
            try:
                # Bazı sayfalarda ürün tanıtımı yapıldığı için overlay üzerine bir tıklama yapılması gerekebilmektedir.
                overlay = driver.find_element(By.CLASS_NAME,"overlay")
                overlay.click()
                time.sleep(0.5)
                # ---------------------------------------------------------------
            except:
                print("Overlay Element Not Found")

            #Product Container
            try:
                add_to_basket = driver.find_element(By.XPATH,"//button[@class='add-to-basket-button']")
                add_to_basket.click()    # Sepete ekler.
            except:
                print("There is no Add to Basket Button")
                product = driver.find_element (By.XPATH,"//div[@class='image-container']") # Ürünün resim kapsayıcını bulur.
                product_URL = product.find_element(By.XPATH,"..").get_attribute("href") # Parent elementin href URL'ini alır.
                go_product_page(product_URL)# Ürün sayfasına gider.
    except :
        print("There is no such element")
        
    return

if __name__ == "__main__":
    # Chromium ayarları yapılarak ilk çalıştırıldığı blok.
    chrome_options = webOptions()
    driver = webdriver.Chrome(options=chrome_options)
	# ----------------------------------------------------								   
    # Excelden okunan anahtar kelimeler sırasıyla ürün ekleme işlemi yapılır.
    # En sonunda da sepet kısmına gider.	
    products = excel_read()
    for i in products:
        if ''.join(i).find('---') != -1:
            add_product('--------')
        else:
            add_product(''.join(i)) # '(birlestirilmesi istenen char)'.join((birlesecek ogeler)) ->> '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
    time.sleep(2)
    driver.get('https://www.trendyol.com/sepet')
	# -----------------------------------------------------------------------------	

    time.sleep(2)
    driver.quit()# Chromiumu kapatır.


