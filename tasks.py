from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.Tables import Tables
import os
import time

def archive_receipts():
    archive = Archive()
    receipts_dir = "output/receipts"
    zip_path = "output/receipts.zip"
    archive.archive_folder_with_zip(receipts_dir, zip_path)
    return zip_path

def store_receipt_as_pdf(order_number):
    pdf = PDF()
    receipt_html = browser.page().content()
    receipts_dir = "output/receipts"
    os.makedirs(receipts_dir, exist_ok=True)
    output_path = f"{receipts_dir}/receipt_{order_number}.pdf"
    pdf.html_to_pdf(receipt_html, output_path)
    return output_path

def screenshot_robot(order_number):
    screenshots_dir = "output/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    output_path = f"{screenshots_dir}/robot_{order_number}.png"
    browser.page().screenshot(path=output_path)
    return output_path

def embed_screenshot_to_receipt(screenshot, pdf_file):
    pdf = PDF()
    pdf.add_files_to_pdf([pdf_file, screenshot], pdf_file, append=True)

def go_to_order_another():
    browser.page().click("#order-another")

def open_robot_order_website():
    browser.configure(slowmo=100)
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    url = "https://robotsparebinindustries.com/orders.csv"
    http = HTTP()
    http.download(url, "orders.csv", overwrite=True)
    tables = Tables()
    orders = tables.read_table_from_csv("orders.csv", header=True)
    return orders

def close_annoying_modal():
    page = browser.page()
    if page.is_visible(".alert-buttons button.btn-dark"):
        page.click(".alert-buttons button.btn-dark")
        
def fill_the_form(row):
    page = browser.page()
    page.select_option("#head", str(row["Head"]))
    page.check(f"#id-body-{row['Body']}")
    page.fill("input[placeholder='Enter the part number for the legs']", str(row["Legs"]))
    page.fill("#address", row["Address"])

def preview_robot():
    page = browser.page()
    page.click("#preview")

def submit_order():
    page = browser.page()
    max_attempts = 5
    for _ in range(max_attempts):
        page.click("#order")
        time.sleep(1)
        if page.is_visible("#order-another"):
            break
        if page.is_visible("css:.alert.alert-danger"):
            continue

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    open_robot_order_website()
    close_annoying_modal()
    orders = get_orders()
    for row in orders:
        print(f"Processing order: {row}")
        fill_the_form(row)