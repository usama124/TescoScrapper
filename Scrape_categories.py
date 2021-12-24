import json, requests
import re, time, random
from bs4 import BeautifulSoup
import DownloadImage as downloader
import ExcelWriter as excel


def get_page_obj(url):
    error_count = 0
    error = True
    page_obj = None
    while error and error_count < 3:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            r.encoding = "utf-8"
            page = r.text
            page_obj = BeautifulSoup(page, "lxml")
            error = False
        except:
            error = True
            error_count = error_count + 1
            print("%s URL not accessible " % (url))

    return page_obj


def write_scraped_products(url):
    f = open("record/scraped_products.txt", "a")
    f.write(url + "\n")
    f.close()


def save_urls_to_file(cat_links):
    f = open("record/cat_urls_list.txt", "a")
    f.write(json.dumps(cat_links) + "\n")
    f.close()


def get_categories_tags(page_obj):
    tags_list = []
    tags_ul = page_obj.find("nav", attrs={"aria-label": "breadcrumb"}).find("ol").findAll("li")
    for tag in tags_ul:
        try:
            tag_text = tag.find("a").text.replace("\n", "").replace(",", "").strip()
            tags_list.append(tag_text)
        except:
            pass
    while "" in tags_list: tags_list.remove("")
    tags = "|".join(tags_list)
    while len(tags_list) < 4:
        tags_list.append("")

    return (tags_list, tags)


def get_alphabets_unit(value):
    only_alpha = ""
    for char in value:
        if char.isalpha():
            only_alpha += char
    return only_alpha

def convert_weight_to_kg(weight : str):
    if weight is None or weight == "":
        return ""
    non_decimal = re.compile(r'[^\d.-]+')
    unit = get_alphabets_unit(weight).strip()
    try:
        if unit.lower() == "kg":
            return weight
        elif unit.lower() == "l":
            return weight
        elif unit.lower() == "g":
            weight = non_decimal.sub('', weight).strip()
            if "." in weight:
                weight = str(float(weight) / 1000) + "Kg"
            else:
                weight = str(int(weight) / 1000) + "Kg"
        elif unit.lower() == "ml":
            weight = non_decimal.sub('', weight).strip()
            if "." in weight:
                weight = str(float(weight) / 1000) + "L"
            else:
                weight = str(int(weight) / 1000) + "L"
        else:
            weight = ""
    except Exception as e:
        weight = ""
        pass
    return weight


def download_all_images(images_list, prod_sku):
    img_name_lst = []
    for img in images_list:
        image_name = downloader.download_image(img, prod_sku)
        img_name_lst.append(image_name)

    while len(img_name_lst) < 4:
        img_name_lst.append("")

    return img_name_lst


def scrape_product(link, main_cat, counterr, file_name):
    is_scraped = False
    print(str(counterr) + " => Scraping product link...")
    prod_sku = str(link).split("/")[-1]
    page_obj = get_page_obj(link)
    if page_obj is None:
        return is_scraped
    try:
        prod_title = page_obj.find("h1", attrs={"class": "product-details-tile__title"}).text.strip()
        categories_list, tags = get_categories_tags(page_obj)
        # cat = categories_list[0]
        # if cat != main_cat:
        #     return is_scraped
        try:
            cost_div = page_obj.find("div", attrs={"class": "price-details--wrapper"})
            price = cost_div.find("div", attrs={"class": "price-control-wrapper"}).text.strip()
            price_per_unit = cost_div.find("div", attrs={"class": "price-per-quantity-weight"}).text.strip()
        except:
            price = ""
            price_per_unit = ""
            pass
        prod_desc = page_obj.find("div", attrs={"class": "product-blocks"})
        try:
            weight = prod_desc.find("div", attrs={"id": "pack-size"}).text.split(":")[-1].strip()
            weight = convert_weight_to_kg(weight)
        except:
            weight = ""
            pass
        prod_desc = str(prod_desc)
        #prod_sku = page_obj.find("span", attrs={"id": "productSKU"}).text.strip()
        image_link = page_obj.find("img", attrs={"class": "product-image"}).attrs["src"]
        image_name = downloader.download_image(image_link, prod_sku)
        excel.write_excel_file(file_name, categories_list, tags, prod_sku, prod_title, price, price_per_unit, weight, prod_desc, image_link, image_name)
        is_scraped = True
    except Exception as e:
        print(e)
        pass
    return is_scraped


def scrape_products_page(main_cat, link, base_url):
    prod_urls_list = []
    page_obj = get_page_obj(link)
    if page_obj is not None:
        try:
            total_products = page_obj.find("div", attrs={"class": "pagination__items-displayed"}).findAll("strong")[-1].text.split(" ")[0].strip()
            total_products = int(total_products)
            print("Total Products = " + str(total_products))
        except:
            total_products = -1
        counter = 1
        while True:
            print("Scraping page " + str(counter) + " ...")
            if page_obj is not None:
                try:
                    products_grid_items = page_obj.find("ul", attrs={"class": "product-list grid"}).findAll("li")
                except Exception as e:
                    break
                for product_div in products_grid_items:
                    try:
                        prod_info = product_div.find("a", attrs={"class": "product-image-wrapper"})
                        prod_link = base_url + prod_info.attrs["href"]
                        prod_urls_list.append(prod_link)
                    except:
                        pass

            prod_urls_list = list(set(prod_urls_list))
            counter = counter + 1
            page_url = link + "?page=" + str(counter)
            page_obj = get_page_obj(page_url)

        prod_urls_list = list(set(prod_urls_list))
        if len(prod_urls_list) >= (total_products - 10):
            cat_links = {main_cat: prod_urls_list}
            save_urls_to_file(cat_links)
            print("Saved all urls to file...")
        else:
            cat_links = {main_cat: []}
            save_urls_to_file(cat_links)
            print("Skipped writing urls to file...")