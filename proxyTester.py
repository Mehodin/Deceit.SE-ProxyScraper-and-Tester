import requests
from multiprocessing.dummy import Pool as ThreadPool
import time
from threading import Thread

class proxyTester():
    def __init__(self, timeout, iterator, threadCount, outFile):
        self.timeout = timeout
        self.iterator = iterator
        self.workingProxies = []
        self.threadCount = threadCount
        self.outFile = outFile
        self.tested = 0
        self.worked = 0
        pass

    def __splitIterator(self):
        sizePerList = len(self.iterator)//self.threadCount
        print(f"Starting with checking proxies... Thread count = {self.threadCount}")
        for index in range(self.threadCount):
            setattr(self, f'iterator{index + 1}',
                    self.iterator[sizePerList * index: sizePerList * (index + 1)])

    def __constructProxy(self, proxy:str):
        http_proxy  = f"http://{proxy}"
        https_proxy = f"https://{proxy}"
        ftp_proxy   = f"ftp://{proxy}"

        proxyDict = { 
                    "http"  : http_proxy, 
                    "https" : https_proxy, 
                    "ftp"   : ftp_proxy
                    }
        return proxyDict

    def __testWorker(self, *iterator):
        
        for proxy in iterator:
            proxyObject = self.__constructProxy(proxy)
            try:
                requests.get('https://httpbin.org/ip',
                            proxies=proxyObject, timeout=self.timeout)
                self.workingProxies.append(proxy)
                with open(self.outFile, 'a') as file:
                    file.write(f'{proxy}\n')
                self.worked += 1
                self.tested += 1
                print(f'Tested proxy {proxy},{self.worked} out of {self.tested} worked, total amount: {len(self.iterator)}')
            except Exception as E:
                self.tested += 1
                print(f'Tested proxy {proxy},{self.worked} out of {self.tested} worked, total amount: {len(self.iterator)}.')
        

    def testProxies(self):
        self.__splitIterator()
        threads = []
        for index in range(self.threadCount):
            iterator = getattr(self, f'iterator{index + 1}')
            thread = Thread(target=self.__testWorker, args=(iterator))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return self.workingProxies
