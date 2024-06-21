from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def webscrape(week):

    # today = day_dict[date.today().weekday()]
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.senpai.moe/?season=fall2024&mode=table")

    name = driver.find_elements(By.CLASS_NAME, "series_instance")

    weekly_object = {"week": week, "weekly": {}}
    for show in name:
        title = show.find_element(By.CLASS_NAME, "seriesTitle")
        airing_day = show.find_element(By.CLASS_NAME, "weekday")
        mal_id = show.find_element(By.LINK_TEXT, "MAL")
        mal_id = int(mal_id.get_attribute("href").split("/")[-1])
        weekly_object["weekly"].update(
            {
                mal_id: {
                    "title": title.text,
                    "airing_day": airing_day.text,
                }
            }
        )

    with open("server/weekly.json", "w") as f:
        weekly_object = json.dumps(weekly_object)
        f.write(weekly_object)

    driver.quit()
