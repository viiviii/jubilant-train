from selenium import webdriver


def headless_chrome() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    return chrome(options=options)


def chrome(options: webdriver.ChromeOptions = None) -> webdriver:
    return webdriver.Chrome(options=options)
