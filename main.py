from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

app = Flask(__name__)

@app.route('/get-keyword-results/', methods=['GET'])
def get_keyword_results():
    keyword = request.args.get('keyword')
    url = f'https://tools.wordstream.com/fkt?website={keyword}'

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'refine-continue'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sc-bTmccw.cFltLW.MuiTable-root'))
        )

        table_data = []
        rows = driver.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'th') + row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            table_data.append(row_data)

        driver.quit()
        return jsonify(table_data)

   
