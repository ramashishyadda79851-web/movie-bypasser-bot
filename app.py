from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

app = FastAPI()

# Blogger ko allow karne ka VIP Pass
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"Status": "Render par Bot ekdum solid chal raha hai, Bhai!"}

@app.get("/bypass")
def bypass_link(url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        gateway_url = None
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            valid_links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and "linkmake.in" in href and "image.linkmake.in" not in href:
                    if href not in valid_links:
                        valid_links.append(href)
            
            if valid_links:
                gateway_url = valid_links[-1] 
                    
        if not gateway_url:
            return {"error": "Direct linkmake.in link nahi mila page par."}

        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(gateway_url)
        time.sleep(8) 
        
        for _ in range(3):
            buttons = driver.find_elements(By.TAG_NAME, "button") + driver.find_elements(By.TAG_NAME, "a")
            for btn in buttons:
                try:
                    text = btn.text.strip().lower()
                    if any(x in text for x in ["verify", "click here", "generate", "continue", "get link"]):
                        if not any(bad in text for bad in ["480p", "520mb", "720p", "1080p", "telegram"]):
                            driver.execute_script("arguments[0].click();", btn)
                            time.sleep(5) 
                except:
                    continue
                
        time.sleep(15) 
        
        final_links_data = []
        links = driver.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            href = link.get_attribute("href")
            text = link.text.strip()
            if href:
                bad_words = ['login', 'policy', 'dmca', 'contact', 'faq', 'home', 'telegram', 'cloudflare']
                if not any(x in href.lower() for x in bad_words) and len(text) > 2:
                    final_links_data.append({"name": text, "url": href})
                    
        driver.quit()
        
        return {
            "success": True,
            "original_url": url,
            "high_quality_gateway": gateway_url,
            "download_links": final_links_data
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
