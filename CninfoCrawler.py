from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Cninfo():
    def __init__(self) -> None:
        self.wait_time = 10
    
    def ChromeDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
    
    def GetReportListPageUrl(self, stkid:str|list|int) -> str:
        if type(stkid) == str:
            stkid = [stkid]
        elif type(stkid) == int:
            stkid = [str(stkid)]
        elif type(stkid) != list:
            print("Error: stkid must be of type str, list or int")
            return None

        # 打开浏览器
        self.ChromeDriver()
        
        # 判断主页是否已经存在
        with open('ReportPageUrl.txt', mode='a+') as report:
            ReportPageUrlList = report.read().split('\n')
        GetReportPageUrlList = []

        for stk in stkid:
            exist = False
            for url in ReportPageUrlList:
                if 'stockCode=' + stkid in url:
                    exist = True
                    GetReportPageUrlList.append(url)
                    break
            
            # 通过巨潮搜索获取主页
            if not exist:
                try:
                    # 搜索
                    search_url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=' + stk
                    self.driver.get(search_url)
                    # 等待搜索页面加载完成
                    element = WebDriverWait(self.driver, self.wait_time).until(
                        EC.presence_of_element_located((By.XPATH, r'//*[@id="pane-shj"]/div/div[2]/div[1]/div[2]/span/a'))
                    )
                    # 进入搜索页面
                    url = element.get_attribute('href') + '#periodicReports'
                    with open('ReportPageUrl.txt', mode='a+') as report:
                        report.write(url+'\n')
                    GetReportPageUrlList.append(url)

                except:
                    print(f"Error: Unable to process StkID {stk}")
        
        # 关闭浏览器
        self.driver.quit()
