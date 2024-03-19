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
    options.add_argument('--disable-images')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'refine-continue'))
        ).click()
        print("Button Clicked")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sc-bTmccw.cFltLW.MuiTable-root'))
        )
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.sc-bczRLJ.jDmpHO.MuiTypography-root'))
        )    
        print("Table Loaded")
        table_data = []
        rows = driver.find_elements(By.CSS_SELECTOR, 'tbody.sc-hQRsPl.hkwLLR.MuiTableBody-root tr')
            for row in rows:
                cols = row.find_elements(By.CSS_SELECTOR, 'th, td')
                row_data = {
                    "keyword": cells[0].text,
                    "search_volume": cells[1].text,
                    "cpc_low": cells[2].text,
                    "cpc_high": cells[3].text,
                    "competition": cells[4].text
                }
                table_data.append(row_data)
    
            return jsonify(table_data)   
        driver.quit()

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
