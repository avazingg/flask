import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest

def test_web_api():
    # Настройка опций Chrome
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Используем WebDriver Manager для автоматической установки ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Используем localhost для локального запуска
        url = os.environ.get('APP_URL', 'http://localhost:5000')
        driver.get(url)
        
        # Получаем и выводим заголовок страницы
        title = driver.title
        print("Title of the page:", title)
        
        # Делаем скриншот и сохраняем его в файл screenshot.png
        screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
        driver.save_screenshot(screenshot_path)
        
        # Проверяем, что скриншот был успешно сохранён
        assert os.path.exists(screenshot_path), "Скриншот не был создан!"
    
    finally:
        # Закрываем драйвер в блоке finally, чтобы гарантировать его закрытие
        driver.quit()
