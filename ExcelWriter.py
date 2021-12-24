import openpyxl


def create_heading(file_name):

    headers = ["Main Category", "Sub Category", "Sub Sub Category", "Sub Sub Sub Category", "Tags", "SKU", "Title", "Price", "Price/unit", "Weight", "Product Details", "Image Link", "Image 1"]
    # workbook_name = "Data/tesco_products.xlsx"
    workbook_name = file_name

    wb_obj = openpyxl.Workbook()
    sheet = wb_obj.active
    sheet.append(headers)
    wb_obj.save(filename=workbook_name)


def write_excel_file(file_name, categories_list, tags, sku, title, price, price_per_unit, weight, prod_details, img_link, img):
    # workbook_name = "Data/tesco_products.xlsx"
    workbook_name = file_name
    wb = openpyxl.load_workbook(workbook_name)
    page = wb.active

    data = [categories_list[0], categories_list[1], categories_list[2], categories_list[3], tags, sku, title, price, price_per_unit, weight, prod_details, img_link, img]

    page.append(data)
    wb.save(filename=workbook_name)