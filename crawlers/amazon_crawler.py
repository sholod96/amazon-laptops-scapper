import time
from .base_crawler import BaseCrawler
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from models.article import Article

LIMITE_PAGINAS = 30

class AmazonCrawler(BaseCrawler):
    def __init__(self):
        super(AmazonCrawler, self).__init__()

    def run(self):
        url = 'https://www.amazon.es/s?rh=n%3A938008031&fs=true&ref=lp_938008031_sar'
        #url = 'https://www.amazon.es/s?i=computers&rh=n%3A938008031&fs=true&page=399&qid=1636360774&ref=sr_pg_2'
        result = []

        # Navegamos a la URL
        self.get(url)
        time.sleep(1)

        # Aceptar cookies
        wait = WebDriverWait(self.browser, 20)
        wait.until(ec.element_to_be_clickable((By.ID, "sp-cc-accept"))).click()

        # Obtener las urls de todos los productos que se van a obtener.
        urls = self.get_urls()

        # Parsear cada URL para obtener la información de los productos.
        article_list = self.get_articles(urls)

        return article_list

    def get_urls(self):
        urls = []
        contador = 0
        start_time = time.time()
        while contador < LIMITE_PAGINAS:
            # Scroll hasta el final.
            self.scroll_bottom()

            # Recopilamos entradas de producto.
            portatiles = self.find_elements_by_class_name("s-result-item")
            # Buscamos la URL de cada producto.

            for portatil in portatiles:
                if portatil.get_attribute('data-component-type') == "s-search-result":
                    url_portatil = portatil.find_element(By.XPATH, ".//a[contains(@class, a-link-normal)]").get_attribute('href')
                    urls.append(url_portatil)

            try:
                # Miramos si hay página siguiente.
                siguiente_url = self.find_element_by_class_name("a-last").find_element(By.XPATH, ".//a").get_attribute('href')
                self.get(siguiente_url)
                contador = contador + 1
            except NoSuchElementException:
                break

        end_time = time.time()
        secs = (end_time - start_time)
        # Dropeamos duplicados pasando a diccionario y después de nuevo a lista.
        urls = list(dict.fromkeys(urls))

        print(f"URLs scrapped in {str(secs)} seconds.")
        return urls

    def check_element_exists_xpath(self, xpath):
        try:
            self.find_element_by_xpath(xpath)

        except NoSuchElementException:
            return False

        return True

    def check_element_exists_id(self, id):
        try:
            self.find_by_id(id)

        except NoSuchElementException:
            return False

        return True

    def get_articles(self, urls):
        article_list = []
        for url in urls:
            self.get(url)
            self.scroll_bottom()
            # Como mínimo queremos nombre y precio del producto.

            if self.check_element_exists_id("productTitle"):
                nombre = self.find_by_id("productTitle").get_attribute("innerHTML").strip("\n")

                if self.check_element_exists_xpath("//span[contains(@class, a-price)]"):
                    try:
                        price = self.find_element_by_xpath("//span[contains(@class, a-text-price)]/span[@class=\"a-offscreen\"]")\
                            .get_attribute("innerHTML")
                    except NoSuchElementException:
                        price = None
                else:
                    price = None
            else:
                nombre = None
                price = None

            # Tenemos los dos elementos mínimos, nombre y precio. Buscamos los demás (opcionales).
            if nombre is not None and price is not None:
                if self.check_element_exists_id("productOverview_feature_div"):
                    # Inicialización de atributos
                    series = None
                    marca = None
                    usos = None
                    pantalla = None
                    sistema_operativo = None
                    entrada_interfaz = None
                    fabricante_cpu = None

                    # Existe ficha técnica del producto, obtenemos todos los elementos de la tabla
                    ficha = self.find_by_id("productOverview_feature_div")
                    table_elements = ficha.find_elements(By.XPATH, ".//div/div/div/table/tbody/*/td/span")

                    # Elementos impares, título de la característica
                    title_list = table_elements[::2]

                    # Elementos pares, contenido de la característica.
                    info_list = table_elements[1::2]

                    # Obtenemos la información.
                    for title, info in zip(title_list, info_list):
                        title_text = title.get_attribute("innerHTML").strip()
                        info_text = info.get_attribute("innerHTML").strip()

                        if title_text.lower() == "series":
                            series = info_text
                        elif title_text.lower() == "marca":
                            marca = info_text
                        elif title_text.lower() == "tamaño de pantalla":
                            pantalla = info_text
                        elif title_text.lower() == "sistema operativo":
                            sistema_operativo = info_text
                        elif title_text.lower() == "usos específicos del producto":
                            usos = info_text
                        elif title_text.lower() == "entrada de interfaz humana":
                            entrada_interfaz = info_text
                        elif title_text.lower() == "fabricante de cpu":
                            fabricante_cpu = info_text

                    article = Article(
                        url=url,
                        name=nombre,
                        price=price,
                        series=series,
                        marca=marca,
                        pantalla=pantalla,
                        sistema_operativo=sistema_operativo,
                        usos=usos,
                        entrada_interfaz=entrada_interfaz,
                        fabricante_cpu=fabricante_cpu
                    )
                    article_list.append(article)

                else:
                    article = Article(
                        url=url,
                        name=nombre,
                        price=price,
                        series=None,
                        marca = None,
                        usos = None,
                        pantalla = None,
                        sistema_operativo = None,
                        entrada_interfaz = None,
                        fabricante_cpu = None
                    )
                    article_list.append(article)

        return article_list














