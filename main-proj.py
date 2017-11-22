import threading
from queue import Queue
from spider import Spider
from domain import *
from main import *

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'http://mariana-badea.ro/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
print(DOMAIN_NAME)
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0 :
        print(str(len(queue_links)) + 'links in the queue')
        create_jobs()


create_workers()
crawl()