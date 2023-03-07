from selenium import webdriver


def headless_chrome() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')

    return chrome(options=options)


def chrome(options: webdriver.ChromeOptions = None) -> webdriver:
    return webdriver.Chrome(options=options)
