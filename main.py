import configparser
import json, time, random

import Scrape_categories as scrapper
import ExcelWriter as excel

parser = configparser.ConfigParser()
parser.read("Conf/config.ini")


def confParser(section):
    if not parser.has_section(section):
        print("No section info  rmation are available in config file for", section)
        return
    # Build dict
    tmp_dict = {}
    for option, value in parser.items(section):
        option = str(option)
        value = value
        tmp_dict[option] = value
    return tmp_dict


def read_cat_stored_urls():
    list_prod = []
    f = open("record/cat_urls_list.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        list_prod.append(json.loads(line))
        line = f.readline().split("\n")[0]
    f.close()
    return list_prod


def read_scraped_products():
    list_prod = []
    f = open("record/scraped_products.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        list_prod.append(line)
        line = f.readline().split("\n")[0]
    f.close()
    return list_prod


def write_scraped_products(url):
    f = open("record/scraped_products.txt", "a")
    f.write(url + "\n")
    f.close()


def write_not_scraped_products(url):
    f = open("record/skipped_products.txt", "a")
    f.write(url + "\n")
    f.close()


general_conf = confParser("general_conf")
CHROME_PATH = general_conf["chrome_path"]
base_url = general_conf["base_url"]
start_url = general_conf["start_url"]

categories_list = confParser("categories")

list_scraped_products = read_scraped_products()
#
cat_urls_saved = read_cat_stored_urls()


products_urls_list = []

if __name__ == '__main__':
    #excel.create_heading()

    print("\n\nScraping groceries...\n\n")
    for data in cat_urls_saved:
        for key in data:
            if key == "Fresh Food" or key == "Food Cupboard":
                file_name = "Data/" + key.replace(" ", "_").lower() + "_tesco_products.xlsx"
                #excel.create_heading(file_name)
                print("Scraping " + key + " products...")
                prod_urls_list = list(set(data[key]))
                counter = 1
                for prod_url in prod_urls_list:
                    if prod_url not in list_scraped_products:
                        is_scraped = scrapper.scrape_product(prod_url, key, counter, file_name)
                        if is_scraped:
                            write_scraped_products(prod_url)
                            list_scraped_products.append(prod_url)
                        else:
                            write_not_scraped_products(prod_url)
                    # else:
                    #     print(str(counter) + " => already scraped " + prod_url)
                    counter = counter + 1

    # for cat in categories_list:
    #     cat_link = categories_list[cat]
    #     main_cat = cat.replace("_", " ").title()
    #     print(main_cat)
    #     scrapper.scrape_products_page(main_cat, cat_link, base_url)

    print("Finish...")

