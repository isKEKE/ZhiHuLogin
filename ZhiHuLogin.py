# _*_ coding: utf-8 _*_
import time
import cv2
import numpy
import requests
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def retry_callback_decorator(frequency: int) -> 'typing.Any':
    def wapped(func: 'typing.Callable') -> 'typing.Any':
        def inner(*args, **kwargs) -> 'typing.Any':
            count = 0
            while count < frequency:
                flag = func(*args, **kwargs)
                if flag == True:
                    break
                count += 1
        return inner
    return wapped

# 账号密码
USERNAME = None
PASSWORD = None

# chromedriver.exe 路径
CHROME_DRIVER_PAHT = "F:\\chromedriver.exe"

class ZhiHuLogin(object):
    _service = Service(CHROME_DRIVER_PAHT)
    _chrome_options = ChromeOptions()
    def __init__(self):
        self.url = "https://www.zhihu.com/signin?next=%2F"
        self.browser: Chrome = None

    def init_browser(self) -> None:
        '''初始化'''
        # chrome配置
        # 监听本地
        self._chrome_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:9222")
        self.browser = Chrome(service=self._service, options=self._chrome_options)
        self.browser.maximize_window()


    def visit(self) -> None:
        '''访问'''
        self.browser.get(self.url)
        # 点击密码登录按钮
        self.browser.find_element(
            By.XPATH, '''//div[@class="SignFlow-tab"]''').click()
        # 账号和密码输入框
        username_element = self.browser.find_element(By.NAME, "username")
        password_element = self.browser.find_element(By.NAME, "password")
        # 登录按钮
        login_btn_element = self.browser.find_element(
            By.XPATH, '''//button[contains(@class, "Button SignFlow-submitButton")]''')
        # 输入账号密码
        username_element.send_keys(USERNAME)
        password_element.send_keys(PASSWORD)
        time.sleep(1)
        # 点击登录按钮
        login_btn_element.click()
        time.sleep(1)


    @retry_callback_decorator(5)
    def login(self) -> bool:
        '''登录'''
        try:
            # 获得滑块图片
            bg_element = self.browser.find_element(
                By.XPATH, '''//img[@alt="验证码背景"]''')
            slider_element = self.browser.find_element(
                By.XPATH, '''//img[@alt="验证码滑块"]'''
            )
            # 图片存本地
            bg_src = bg_element.get_attribute("src")
            slider_src = slider_element.get_attribute("src")
            self._pic_to_pc(bg_src, slider_src)
            # 块节点
            chunk_element = self.browser.find_element(
                By.XPATH, '''//div[@class="yidun_slider"]''')
            # 匹配
            offset = self.disitingush()
            # 拖动
            self._drag_slider(chunk_element, offset)
            time.sleep(3)
        except:
            return True
        else:
            return False


    def disitingush(self) -> int:
        '''识别'''
        # 背景图片
        img_bg = cv2.imread("./bg.png")[0:160, 5:320]
        img_bg_canny = self._img_handle(img_bg)
        # 滑块
        img_slider = cv2.imread("./slider.png")
        img_slider_canny = self._img_handle(img_slider)
        # 模糊匹配：cv2.matchTemplate; 归一化相关系数匹配法
        results = cv2.matchTemplate(img_bg_canny, img_slider_canny, cv2.TM_CCOEFF_NORMED)
        # 查找最佳结果
        min_val, max_val, min_index, max_index = cv2.minMaxLoc(results)
        # 位置
        offset = max_index[0] + 10
        return offset


    def _drag_slider(self, chunk, offset: int) -> None:
        '''拖动滑动块'''
        ...


    def _img_handle(self, img: 'numpy.ndarray') -> None:
        '''图片处理'''
        # 高、宽
        height, width, _ = img.shape
        # 反色
        for i in range(height):
            for j in range(width):
                img[i, j] = (255 - img[i, j][0],
                                  255 - img[i, j][1],
                                  255 - img[i, j][2])
        # 高斯模糊
        img_gaussian = cv2.GaussianBlur(img, (3, 3), 0)
        # 边缘检测
        img_canny = cv2.Canny(img_gaussian, 200, 50)
        return img_canny


    def _show(self, img: 'numpy.ndarray') -> None:
        '''展示'''
        cv2.imshow("Image", img)
        cv2.waitKey(0)


    def _pic_to_pc(self, bg_src: str, slider_src: str) -> None:
        bg_content = requests.get(bg_src).content
        slider_content = requests.get(slider_src).content
        open("bg.png", "wb").write(bg_content)
        open("slider.png", "wb").write(slider_content)


    def __del__(self):
        '''回收'''
        if self.browser is not None:
            self.browser.quit()

        cv2.destroyAllWindows()


def main() -> int:
    zhihu = ZhiHuLogin()
    zhihu.init_browser()
    zhihu.visit()
    zhihu.login()
    return 0

if __name__ == "__main__":
    main()
