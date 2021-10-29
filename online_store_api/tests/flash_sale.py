import logging
import requests
import threading
import uuid
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

CUSTOMER_WANT_TO_BUY = 15
PRODUCT_TO_SELL = 20
BUY_TIMES = 10
QTY_EVERY_CUSTOMER = 3

# expected values
LAST_STOCK = PRODUCT_TO_SELL % QTY_EVERY_CUSTOMER
TOTAL_ORDERED = PRODUCT_TO_SELL - LAST_STOCK

# setup logging test
logging.basicConfig(
    filename="logs/flash_sale.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)


def action_order(customer_id, product_id):
    for _buy_time in range(BUY_TIMES):
        url = BASE_URL + "/api/cart/"
        body = {
            "customer_id": customer_id,
            "product_id": product_id,
            "qty": QTY_EVERY_CUSTOMER,
        }

        response_cart = requests.post(url, json=body)
        if response_cart.status_code != 200:
            logging.error(response_cart.json())

        url_order = BASE_URL + "/api/order/"
        body_order = {"customer_id": customer_id}
        response = requests.post(url_order, json=body_order)
        if response.status_code != 200:
            logging.error(response.json())


def run_with_threads(method, customer_ids, product_id):
    threads = []
    for customer in customer_ids:
        args = (customer, product_id)
        thread = threading.Thread(target=method, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    customer_ids = []
    for i in range(CUSTOMER_WANT_TO_BUY):
        random = str(uuid.uuid4())[-5:]
        customer_uname = f"customer f{random}"
        url = BASE_URL + "/api/customer/"
        body = {"username": customer_uname}
        response = requests.post(url, json=body)
        customer_ids.append(response.json().get("id"))

    # create product for testing
    random = str(uuid.uuid4())[-5:]
    product_name = f"Product {random[-7:]}"
    product_stock = PRODUCT_TO_SELL
    product_url = BASE_URL + "/api/product/"
    product_body = {"name": product_name, "stock": product_stock}
    response = requests.post(product_url, json=product_body)
    product_id = response.json().get("id")

    # add product to cart with threading
    run_with_threads(action_order, customer_ids, product_id)

    # show result with expected
    ordered_product_url = BASE_URL + "/api/product/ordered/"
    response = requests.post(ordered_product_url, json={"product_id": product_id})
    if response.status_code != 200:
        logging.error(response.json())

    data_response = response.json()
    last_stock_response = data_response.get("current_stock")
    total_ordered_response = data_response.get("total")

    # check
    print("=========== EXPECTED RESULT =============")
    print("last stock: ", LAST_STOCK)
    print("total ordered: ", TOTAL_ORDERED)

    print("=========== ACTUAL RESULT =============")
    print("last stock: ", last_stock_response)
    print("total ordered: ", total_ordered_response)

    print("last stock valid? ", last_stock_response == LAST_STOCK)
    print("total ordered valid? ", total_ordered_response == TOTAL_ORDERED)
