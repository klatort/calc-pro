from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import chromedriver_autoinstaller
import pandas as pd

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver with headless options
driver = webdriver.Chrome(options=chrome_options)


def safe_find_element(wait, by, value):
    return wait.until(EC.presence_of_element_located((by, value)))


def safe_click_element(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
    except StaleElementReferenceException:
        pass  # Ignoring the exception, assuming the element will be refetched


try:
    driver.get("https://www.huaweicloud.com/intl/en-us/pricing/calculator.html#/ecs")

    wait = WebDriverWait(driver, 10)

    region_button = safe_find_element(
        wait,
        By.XPATH,
        "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/form/div/div/div/div/ul/li[9]/button",
    )
    safe_click_element(driver, region_button)

    RI_button = safe_find_element(
        wait,
        By.XPATH,
        "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[4]/form/div/div/div/div/ul/li[3]/button",
    )
    safe_click_element(driver, RI_button)

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/form/div/div/div/ul",
            )
        )
    )
    type_father = safe_find_element(
        wait,
        By.XPATH,
        "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/form/div/div/div/ul",
    )
    type_children = type_father.find_elements(By.TAG_NAME, "button")
    data = []
    for type_button in type_children:
        safe_click_element(driver, type_button)
        tier_father = safe_find_element(
            wait,
            By.XPATH,
            "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[3]/form/div/div/div/ul",
        )
        tier_children = tier_father.find_elements(By.TAG_NAME, "button")
        for tier_button in tier_children:
            safe_click_element(driver, tier_button)
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[4]/form/div/div/div/ul",
                    )
                )
            )
            cores_father = safe_find_element(
                wait,
                By.XPATH,
                "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[4]/form/div/div/div/ul",
            )
            cores_children = cores_father.find_elements(By.TAG_NAME, "button")
            for cores_button in cores_children:
                safe_click_element(driver, cores_button)
                wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[5]/form/div/div/div/ul",
                        )
                    )
                )
                memory_father = safe_find_element(
                    wait,
                    By.XPATH,
                    "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[5]/form/div/div/div/ul",
                )
                memory_children = memory_father.find_elements(By.TAG_NAME, "button")
                for memory_button in memory_children:
                    safe_click_element(driver, memory_button)
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div/div/form/div/div/div/div",
                            )
                        )
                    )
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[4]",
                            )
                        )
                    )
                    sleep(1)
                    flavor = driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div/div/form/div/div/div/div",
                    )
                    cost = driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[4]",
                    )

                    FLAVOR = flavor.text.split(" ")[2]
                    PRICE = cost.text.split(" ")[1]
                    data.append({"Flavor": FLAVOR, "Price": PRICE})
                    print(FLAVOR, "|", PRICE)
    df = pd.DataFrame(data)
    df.to_excel('RI_linux_prices.xlsx', index=False)
finally:
    driver.quit()
