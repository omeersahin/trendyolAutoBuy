import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import logging
from configparser import ConfigParser


# Gecikmeleri ve bazı fonksiyonları açıp kapatabilmek için config dosyası okunan fonksiyon bloğu.
def read_config():
    config = ConfigParser()
    config.read('config.cfg')
    cart             =  bool(int(config['Ayarlar']['sepeti_goster']))
    drive_quit       =  bool(int(config['Ayarlar']['chrome_kapat']))
    regular_delay    =  float(config['Ayarlar']['duzenli_gecikme'])
    error_page_delay =  float(config['Ayarlar']['hata_sayfasi_gecikme'])
    drive_quit_delay =  float(config['Ayarlar']['chrome_kapat_gecikme'])
    sort             =  int(config['Ayarlar']['siralama'])
    free_shipment    =  bool(int(config['Ayarlar']['kargo_bedava']))

    return cart, drive_quit, regular_delay, error_page_delay, drive_quit_delay, sort, free_shipment

# Excel verilerini okunup list haline getirildiği fonksiyon bloğu.
def excel_read():
    try:
        df = pd.read_excel('keywords.xlsx', sheet_name='Sheet1')
        product_list = df.values.tolist()
        return product_list
    except:
        logging.error("Program couldn't read excel file.")

# Chromium popup ve uyarıları/bildirileri kapattığımız ve ekranı tam ekran yaptırdığımız fonksiyon bloğu.																													 
def webOptions():
    customOptions = webdriver.ChromeOptions()
    customOptions.add_argument("--disable-notifications") # Uyarı ve Bildirimlerin Kapatılması
    customOptions.add_argument("--disable-popup-blocking")# Pop-Upların kapatılması
    customOptions.add_argument("--start-maximized")       # Tam Ekran yapılması
    customOptions.add_argument('log-level=3')             # SSL Handshake hatasını loglaması önlemek için.
    return customOptions

# Bütün ürünlerin bulunduğu ana ekranda sepete ekle butonu bulunmadığı takdirde sayfaya yönlendirme yapılıp
# ürün sayfasında sepete ekleme işleminin yapıldığı fonksiyon bloğu.
def go_product_page(path,delay):
    
    try:

        driver.get(path)# Sayfaya gider.
        time.sleep(delay)																  
        add_to_basket = driver.find_element(By.XPATH,"//button[@class='add-to-basket']")
        add_to_basket.click()   # Sepete ekler.
    except:
        logging.error("'Add to Basket' button not found.")

# Ürün ekleme fonksiyon bloğu.
# Bazı elementleri Class ismi bazılarını Xpath ile bulmaktadır.								 																	
def add_product(product_name,delay,sort,free_shipment):
    logging.info("Trying to buy " + product_name)
    try:
        driver.get('https://www.trendyol.com/sr?q='+str(product_name)+'&qt='+str(product_name)+'&st='+str(product_name)+'&os=1')
        if driver.find_element(By.XPATH,'//*[@id="search-app"]').get_attribute('id') == 'search-app':
            free_shipment_string = ""
            if free_shipment:
                free_shipment_string = "&fc=true"

            sort_string = 'MOST_RATED'
            if sort == 0:
                sort_string = 'MOST_RATED'
            elif sort == 1:
                sort_string = 'PRICE_BY_ASC'
            elif sort == 2:
                sort_string = 'PRICE_BY_DESC'
            elif sort == 3:
                sort_string = 'BEST_SELLER'
            elif sort == 4:
                sort_string = 'MOST_FAVOURITE'
            elif sort == 5:
                sort_string = 'MOST_RECENT'


            driver.get('https://www.trendyol.com/sr?q='+str(product_name)+'&qt='+str(product_name)+'&st='+str(product_name)+'&os=1'+free_shipment_string+'&sst='+sort_string)
            time.sleep(delay)
            try:
                # Bazı sayfalarda ürün tanıtımı yapıldığı için overlay üzerine bir tıklama yapılması gerekebilmektedir.
                overlay = driver.find_element(By.CLASS_NAME,"overlay")
                overlay.click()
                time.sleep(delay)
                # ---------------------------------------------------------------
            except:
                logging.warning("Overlay element not found.")

            #Product Container
            try:
                add_to_basket = driver.find_element(By.XPATH,"//button[@class='add-to-basket-button']")
                add_to_basket.click()    # Sepete ekler.
            except:
                logging.info("'Add to Basket' button not found.")
                product = driver.find_element (By.XPATH,"//div[@class='image-container']") # Ürünün resim kapsayıcını bulur.
                product_URL = product.find_element(By.XPATH,"..").get_attribute("href") # Parent elementin href URL'ini alır.
                go_product_page(product_URL,delay)# Ürün sayfasına gider.
    except :
        logging.error("Element not found.")
        
    return

if __name__ == "__main__":
    # Log ayarları yapılır.
    logging.basicConfig(filename='app.log', filemode='a',format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    # logging.debug('This is a debug message')
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')
    # -----------------------------------------------

    # Chromium ayarları yapılarak ilk çalıştırıldığı blok.
    try:
        chrome_options = webOptions()
        driver = webdriver.Chrome(options=chrome_options)
    except:
        logging.critical("Chrome not started.")
	# ----------------------------------------------------	
    # 
    [cart, drive_quit, regular_delay, error_page_delay, drive_quit_delay, sort, free_shipment]=read_config()	
    # ----------------------------------------------------								   
    # Excelden okunan anahtar kelimeler sırasıyla ürün ekleme işlemi yapılır.
    # En sonunda da sepet kısmına gider.
    products = excel_read()
    for i in products:
        add_product(''.join(i),regular_delay,sort,free_shipment) # '(birlestirilmesi istenen char)'.join((birlesecek ogeler)) ->> '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
    time.sleep(error_page_delay)
    if cart:
        driver.get("https://www.trendyol.com/sepet")
	# -----------------------------------------------------------------------------	
    if drive_quit:
        time.sleep(drive_quit_delay)
        driver.quit()# Chromiumu kapatır.


