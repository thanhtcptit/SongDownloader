import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 

class Render(QWebPage):  
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

url = 'http://mp3.zing.vn/bai-hat/Dung-Ai-Nhac-Ve-Anh-Ay-Tra-My-Idol/ZW7FC0FB.html'
#This does the magic.Loads everything
r = Render(url)
#result is a QString.
result = r.frame.toHtml()

formatted_result = str(result.toAscii())

#Next build lxml tree from formatted_result
tree = html.fromstring(formatted_result)

#Now using correct Xpath we are fetching URL of archives
archive_links = tree.xpath('//div[@class="campaign"]/a/@href')
#print archive_links