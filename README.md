# 知乎自动化登录

## 一、系统环境

- 开发语言: Python3+
- 第三方库: requests、selenium、opencv
## 二、骚操作

> 这个代码就是帮助你理解我如何过的知乎检测；有时候某网页不只是检测`window.navigator`对象，但是我又很小白咋办？来了：通过自定义端口的方式进行自动化！什么意思？就是我开启一个正常的chrome浏览器，然后我开个端口，我让selenium通过这个端口去操作打开的正常chrome浏览器。

```
# _*_ coding: utf-8 _*_
import os
import subprocess
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# chrome.exe文件绝对路径
CHROME_PATH = r"C:\Users\XXX\AppData\Local\Google\Chrome\Application\chrome.exe"
# 自定义端口方式chrome浏览器用户数据存储位置，防止覆盖自己的源数据
CHROME_INFO_PATH = r"F:\chrome-data"
# 开启端口
CHROME_PORT = 9222
# 命令
COMMANDS = [CHROME_PATH,
            f"--remote-debugging-port={CHROME_PORT}",
            f'--user-data-dir={CHROME_INFO_PATH}']

def main() -> int:
    # 打开浏览器
    pipe = subprocess.Popen(" ".join(COMMANDS), shell=False)
    url = "https://antispider1.scrape.center/"
    service = Service("F:\\chromedriver.exe")
    # chrome配置
    chrome_options = ChromeOptions()
    # 监听本地
    chrome_options.add_experimental_option(
        "debuggerAddress", f"127.0.0.1:{CHROME_PORT}")
    # 浏览器对象
    browser = Chrome(service=service, options=chrome_options)
    try:
        browser.get(url)
        input("quit?>")
    finally:
        browser.quit()
        pipe.kill()
    return 0

if __name__ == "__main__":
    main()
```

## 三、作者注释

- 声明一些特殊原因，关于如何拖动滑块并过检测我无法细说，大致就是你需自己实现`ZhiHuLogin::_drag_slider`方法
- 方法就是：等...S, 然后直接拖动即可。

