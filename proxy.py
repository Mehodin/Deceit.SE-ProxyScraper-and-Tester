import moduleInstaller
import proxyScraper


proxyScraper.getProxies(linkFile = 'url.txt',
                        saveFile = 'proxies.txt',
                        timeout = 5,
                        threadCount = 10)

