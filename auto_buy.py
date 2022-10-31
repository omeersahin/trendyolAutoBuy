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

    time.sleep(1.0)
    try:
        product     = driver.find_element(By.XPATH,path)
        product_URL  = product.get_attribute("href")    # Ürün sayfasının URL'ini verir.
        driver.get(product_URL) # Sayfaya gider.
        #                                                               ------
        # /html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div[5]/button
        #                                                               ------ 
        # Ürün sayfaları değişiklik gösterebildiğinden dolayı bir 5-7 arasından bulunmaktadır. 
        add_to_basket = driver.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div[5]/button")
    except:
        print("There is not add to basket button at div[5]")
        try:
            add_to_basket = driver.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div[6]/button")
        except:
            print("There is not add to basket button at div[6]")
            add_to_basket = driver.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div[7]/button")                                        
    add_to_basket.click()   # Sepete ekleme butonuna tıklar.
    
# Ürün ekleme fonksiyon bloğu.
# Bazı elementleri Class ismi bazılarını Xpath ile bulmaktadır.
def add_product(product_name):

    try:
        search_box = driver.find_element(By.CLASS_NAME,"vQI670rJ") # Arama kutusu
        search_box.clear()                  # Arama kutusunu temizler.
        search_box.send_keys(product_name)  # Arama kutusuna anahtar kelimeyi girer.

        search_button = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div/div/i") # Arama butonu
        search_button.click() # Arama butonuna tıklar.

        try:
            # Bazı sayfalarda ürün tanıtımı yapıldığı için overlay üzerine bir tıklama yapılması gerekebilmektedir.
            overlay = driver.find_element(By.CLASS_NAME,"overlay")
            overlay.click()
            # -----------------------------------------------------------------------------------------------------
        except:
            print("Overlay Element Not Found")

        time.sleep(1)
        # Kargo Bedava filterisini ekler.
        free_shipping_text = driver.find_element(By.XPATH,"//*[contains(text(),'Kargo Bedava')]")
        free_shipping_checkbox = free_shipping_text.find_element(By.XPATH,"./parent::*")
        free_shipping_checkbox.click()
        # -------------------------------

        time.sleep(1.5)
        # En çok değerlendirilene göre sıralama yapar.
        sort_item = driver.find_element(By.XPATH,("//option[@value='MOST_RATED']"))
        sort_item.click()
        # --------------------------------------------
        time.sleep(1)
        try:
        
            add_to_basket = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/div[2]/button")                                              
            add_to_basket.click()
            #                                                                                                              ------
            #                                             /html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/div[2]/button
            #                                                                                                              ------ 
            # Sayfadaki hızlı teslimat seçeneği gibi bannerlar bir div oluşturduğundan ve her aramada da çıkmadığından
            # ürün sayfaları değişiklik göstermekte 4-5 arasında değişiklik bulunmaktadır.                                                
        except:
            print("There is no Add to Basket Button at div[4]")
            try:
                add_to_basket = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[5]/div[1]/div/div[2]/div[1]/div[2]/button")
                add_to_basket.click()
            except:
                print("There is no Add to Basket Button")
                try:
                    #                                                                                                                                ------
                    #                                             /html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[5]/div[1]/div/div[1]/div[1]/a
                    #                                                                                                                                ------ 
                    # Reklamlardan dolayı bir div oluşturduğundan ve her aramada da çıkmadığından
                    # ürün sayfaları değişiklik göstermekte 1-2 arasında değişiklik bulunmaktadır.
                    if driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]").get_attribute("class") != "banner-rush-delivery":
                        go_product_page("/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[1]/div[1]/a")
                        #                                                                                                   ------
                    else :
                        print("Product URL not found at div[5]")
                        go_product_page("/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[5]/div[1]/div/div[1]/div[1]/a")
                except:
                    print("Product URL not found at div[1]")
                    if driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]").get_attribute("class") != "banner-rush-delivery":
                        go_product_page("/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/a")
                        #                                                                                                   ------
                    else :
                        print("Product URL not found at div[5]")
                        go_product_page("/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[5]/div[1]/div/div[2]/div[1]/a")
                    
                    
                    

    except:
        print("There is no such element")


        

        



if __name__ == "__main__":
    # Chromium ayarları yapılarak ilk çalıştırıldığı blok.
    chrome_options = webOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.trendyol.com/')
    # İlk açıldığında çerezler çıkmaktadır. Otomatik kabul edilmektedir.
    cookies_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    cookies_button.click()    # Çerezleri kabul eder.
    # ----------------------------------------------------

    # Excelden okunan anahtar kelimeler sırasıyla ürün ekleme işlemi yapılmaktadır.
    # En sonunda da sepet kısmına gidilmektedir.
    products = excel_read()
    for i in products:
        print("Trying to buy " + str(i) + " keyword")
        add_product(i)
        time.sleep(1)
    time.sleep(1)
    driver.get('https://www.trendyol.com/sepet')
    # -----------------------------------------------------------------------------


    time.sleep(2)
    driver.quit() # Chromiumu kapatır.


