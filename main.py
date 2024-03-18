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

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sc-bTmccw.cFltLW.MuiTable-root'))
        )
        table = driver.find_element(By.CSS_SELECTOR, 'table.sc-bTmccw.cFltLW.MuiTable-root')
        rows = table.find_elements(By.CSS_SELECTOR, 'tr')

        table_data = []
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, 'th, td')
            row_data = [cell.text for cell in cells if cell.text]  # Exclude empty strings
            if row_data:
                table_data.append(row_data)

        driver.quit()
        return jsonify(table_data)

    except Exception as e:
        driver.quit()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Set the FLASK_ENV environment variable to 'development' to enable debug mode
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
