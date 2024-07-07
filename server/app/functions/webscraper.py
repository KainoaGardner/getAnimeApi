from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
import time


def webscrape(week):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.livechart.me/schedule")

    driver.find_element(By.XPATH, '//*[@title="Full Layout"]').click()

    weekly_object = {"week": week, "weekly": {}}
    days = driver.find_elements(By.CLASS_NAME, "text-2xl")
    day_blocks = driver.find_elements(By.CLASS_NAME, "lc-grid-template-anime-cards")
    for count, day in enumerate(days[1:]):
        day_block = day_blocks[count]
        anime_lists = day_block.find_elements(By.CLASS_NAME, "lc-anime-card")

        for anime in anime_lists:

            try:
                anime_title = anime.find_element(By.CLASS_NAME, "lc-anime-card--title")
                mal_id = anime.find_element(By.CLASS_NAME, "mal")
                mal_id = int(mal_id.get_attribute("href").split("/")[-1])
                ep_count = anime.find_element(By.CLASS_NAME, "font-medium")
                print(anime_title.text)

                weekly_object["weekly"].update(
                    {
                        mal_id: {
                            "title": anime_title.text,
                            "airing_day": day.text,
                            "ep_count": ep_count.text,
                        }
                    }
                )
            except:
                continue

    with open("server/weekly.json", "w") as f:
        weekly_object = json.dumps(weekly_object)
        f.write(weekly_object)

    driver.quit()
