from selenium import webdriver

_driver = webdriver.Chrome()


def go_login() -> None:
    _driver.get('https://dhlottery.co.kr/user.do?method=login&returnUrl=')


# todo
def title() -> str:
    return _driver.title
