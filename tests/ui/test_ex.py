import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.binary_location = '/usr/bin/google-chrome-stable'

    # Явно указываем путь к ChromeDriver в контейнере
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    driver.quit()

def test_web_api(driver):
    url = "http://web:5000"
    driver.get(url)
    
    # Получаем и выводим заголовок страницы
    title = driver.title
    print("Title of the page:", title)
    
    # Делаем скриншот и сохраняем его в файл screenshot.png
    screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
    driver.save_screenshot(screenshot_path)
    
    # Проверяем, что скриншот был успешно сохранён
    assert os.path.exists(screenshot_path), "Скриншот не был создан!"
