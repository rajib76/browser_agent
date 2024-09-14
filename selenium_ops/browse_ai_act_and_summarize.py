import time

from selenium import webdriver

from llms.v2.openai_client import ImageRead

ir = ImageRead()

def browse_article(article_id):
    url = "https://artificialintelligenceact.eu/article/{article_id}/".format(article_id=article_id)
    print(url)
    driver = webdriver.Chrome()
    driver.get(url)

    # Get scroll height

    last_position = driver.execute_script("return window.pageYOffset")
    viewport_height = driver.execute_script("return window.innerHeight")
    existing_summary = ""
    while True:
        image_url = driver.get_screenshot_as_base64()
        summary = ir.read_and_sumamrize_image_content(image_url=image_url,existing_summary=existing_summary)
        existing_summary = summary
        driver.execute_script(f"window.scrollBy(0, {viewport_height});")


        time.sleep(2)
        current_position = driver.execute_script("return window.pageYOffset")

        if current_position == last_position:
            break
        last_position = current_position

    driver.quit()
    return summary


if __name__ == "__main__":
    for i in range(1,5):
        summary = browse_article(i)
        with open('ai_act.txt', 'a') as file:
            file.write(summary)

