from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest



@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--no-sandbox")  # Убирает проблемы с sandbox в контейнере
    options.add_argument("--disable-dev-shm-usage")  # Исправляет ошибки с памятью
    options.add_argument("--headless")  # Запуск в headless-режиме (если нужно)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


def test_web_api(driver):
    url = "http://localhost:5000"
    driver.get(url)
    
    # Получаем и выводим заголовок страницы
    title = driver.title
    print("Title of the page:", title)
    
    # Делаем скриншот и сохраняем его в файл screenshot.png
    screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
    driver.save_screenshot(screenshot_path)
    
    # Проверяем, что скриншот был успешно сохранён
    assert os.path.exists(screenshot_path), "Скриншот не был создан!"
