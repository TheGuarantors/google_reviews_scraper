from SnowflakeConnector import SnowflakeConnector
from WebDriver import WebDriver
from multiprocessing import Pool
import os
import pandas as pd
import threading
import numpy as np

with open('needs_parse.txt', 'r', encoding="utf-8") as f:
    ad_from_file = f.readlines()

ad_from_file = [x.strip() for x in ad_from_file]

threads = []

threadCount = 8 #Number of Threads you want

#Custom Thread class 
class doStuffThread(threading.Thread):
    def __init__(self, partLinks):
        threading.Thread.__init__(self)
        self.partLinks = partLinks
    def run(self):
        data = WebDriver(self.partLinks).run_scraping()
        file_name_counter = [int(x.split('.')[0]) for x in os.listdir('reviews') if x.split('.')[0]]
        file_name_counter = '1' if not file_name_counter else str(max(file_name_counter) + 1)
        pd.DataFrame(data).transpose().to_csv(f'reviews//{file_name_counter}.csv')

def scraping():
    #Split the links to give each thread a part of them
    for partLinks in np.array_split(ad_from_file,threadCount):
        t = doStuffThread(partLinks)
        threads.append(t)
        t.start()
    #wait till all Threads are finished
    for x in threads:
        x.join()

if __name__ == '__main__':
    scraping()
    
