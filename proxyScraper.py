import os, requests, re

import proxyTester

class getProxies():
    def __init__(self, linkFile, saveFile, timeout, threadCount):
        self.proxyList = []
        self.linkFile = linkFile
        self.saveFile = saveFile
        self.timeout = timeout
        self.successCount = 0
        self.links = None
        self.threadCount = threadCount
        self.__main()

    def __getWebsites(self):
        with open(self.linkFile, 'r+') as linkFile:
            self.links = linkFile.readlines()
    
    def __getProxies(self):
        for website in self.links:
            try:
                response = requests.get(website).text
            except:
                continue
            proxies = re.findall(pattern='(\d*[.]\d*[.]\d*[.]\d*[:]\d*)',
                       string=response, flags=re.IGNORECASE)
            for proxy in proxies:
                self.proxyList.append(proxy)
            proxies = re.findall(pattern='(\d*[:]\d*[:]\d*[:]\d*[:]\d*)',
                                 string=response, flags=re.IGNORECASE)
            for proxy in proxies:
                self.proxyList.append(proxy)
            print(f'Completed: {website.strip()}')

    def __testProxies(self, proxyList):
        testInstance = proxyTester.proxyTester(self.timeout, proxyList, self.threadCount, self.saveFile)
        self.proxyList = testInstance.testProxies()

    def __writeProxies(self):
        print("Removing duplicates...")
        self.proxyList = list(set(self.proxyList))
        print("Removed duplicates...")


        print("Testing proxies... this can take a while...")
        self.__testProxies(self.proxyList)
        print("Tested proxies...")

    def __main(self):
        self.__getWebsites()
        self.__getProxies()
        self.__writeProxies()

        input('Completed proxy sequence!\
        \nCredits to Mehodin, developer for Deceit.SE.\
        \nI hope this worked fine for you!\
        \nPress enter to exit...')
