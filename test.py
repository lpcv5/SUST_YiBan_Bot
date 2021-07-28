import xmltodict as xmltodict
from cssselect import xpath
from lxml import etree

import goto_checkpage
import util
import json
import re

html = etree.parse('min.html', etree.HTMLParser())
url_list = html.xpath('/html/body/div[@class="weui-grids grids-small"]/a/@href')
elem = html.xpath("/html/body/div[@class='weui-grids grids-small']/a/p/text()")
# url_holiday = url_list[elem.index("寒假信息上报")]
# url_morn = url_list[elem.index("晨检上报")]
# url_noon = url_list[elem.index("午检上报")]
url = {
    "url_holiday": url_list[elem.index("寒假信息上报")],
    "url_morn": url_list[elem.index("晨检上报")],
    "url_noon": url_list[elem.index("午检上报")]
       }
with open('url.json', 'w') as date:
    json.dump(url, date)


# url = '../public/index.php?key=Pvr6nPpGgyFaHMmigjyi8p6YiMfcA2vT68XdjOduoUcuMi41ZgzuO4W7Za/get5gZdXk5FPud9QeRdwq' \
#       '//HTDYaN7DfcGuzn8Z70nCBYP9tK6YA8ijw1ItGA7Xh511fs0ZmT9iFLiocC718lgC5bmXljKEsmSzideORMdjVNUnA= '
# print(re.findall(r"key=(.+?)$", url)[0])
