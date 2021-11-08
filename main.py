import csv
import dataclasses
import pandas as pd
import time

from crawlers.amazon_crawler import AmazonCrawler

print("Se inicia el proceso de captura de datos")
start_time = time.time()

for crawler in [AmazonCrawler()]:
    result = crawler.run()

dataframe = pd.DataFrame.from_records([article.to_dict() for article in result])

dataframe.to_csv('amazon_laptops_dataset.csv', index=False)

end_time = time.time() - start_time
print(f"Se han obtenido los datos y se ha generado un CSV en {str(end_time)} segundos")