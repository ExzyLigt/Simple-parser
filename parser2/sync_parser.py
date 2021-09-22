import argparse
import datetime
import os.path
from typing import Callable

import requests
import ujson
from bs4 import BeautifulSoup
from requests.models import Response

from parser2.to_xlsx import dict_to_excel

ROOT = "https://swgshop.ru/"
SEARCH_URL = "https://swgshop.ru/search/?AJAX_search=Y&q="
ARTICUL_LENGTH = 6

id_of_item_in_search = {
    "tag": "a",
    "class_": "catalog-tile__link",
}

id_of_recommended_articuls = {
    "tag": "div",
    "class_": "catalog-item__articul",
}


def load_json(json_file: str) -> dict:
    """Load json file

    Args:
        json_file (str): Absolute json file path or relative path to python interpreter

    Returns:
        dict: Plain dict object
    """
    with open(json_file, "r") as json:
        j = ujson.load(json)

        return j


def create_list_from_json(json_file: str) -> list[str]:
    """Parse json string with distinct structure

    Args:
        json_file (str): Absolute json file path or relative json path to python interpreter

    Returns:
        list[str]: List with all articuls
    """
    items_dict = load_json(json_file)

    return [item["sku"] for item in items_dict["Аркуш1"]]


def do_requests(urls: list[str]) -> list[Response]:
    """Do requests to URLs

    Args:
        urls (list[str]): List with URLs

    Returns:
        list[Response]: List of Responses objects
    """
    return [requests.get(url) for url in urls]


def get_soup(*, response: Response) -> BeautifulSoup:
    """Factory method aimed for supplying soup object to each request

    Args:
        response (Response): Response object

    Returns:
        BeautifulSoup: BeautifulSoup object
    """
    return BeautifulSoup(response.text, "lxml")


def get_urls_for_search(articuls: list[str]) -> list[str]:
    """Create list that contains concatenated SEARCH_URL and articuls

    Args:
        articuls (list[str]): List of articuls

    Returns:
        list[str]: List of full URLs to search
    """
    return [SEARCH_URL + articul for articul in articuls]


def get_full_url_for_products(href: str) -> str:
    """Join ROOT path and recieved href

    Args:
        href (str): Href

    Returns:
        str: Full path for item
    """
    return os.path.join(ROOT, href[1:])


def search_href_of_product(
    response: Response, *, tag: str, class_: str
) -> Callable[[str], str]:
    """Search href of product in html page

    Args:
        response (Response): Response object for distinct URL
        tag (str): Href's tag in HTML
        class_ (str): Href's class in HTML

    Returns:
        str: Function that returns full URL path
    """
    soup = get_soup(response=response)
    product = soup.find(tag, class_=class_)
    href = product.get("href")

    return get_full_url_for_products(href=href)


def create_list_of_full_urls(responses: list[Response]) -> list[str]:
    """Create full URLs list for all articuls

    Args:
        responses (list[Response]): List of Responses

    Returns:
        list[str]: Full URLs list
    """
    return [
        search_href_of_product(response, **id_of_item_in_search)
        for response in responses
    ]


def find_recommended_articuls(
    response: Response, *, tag: str, class_: str
) -> list[str]:
    """Find recommended articuls within item

    Args:
        response (Response): Response object
        tag (str): Recommended articul's tag in HTML
        class_ (str): Recommended articul's class in HTML

    Returns:
        list[str]: List of recommended articuls
    """
    soup = get_soup(response=response)
    articuls_ = soup.find_all(tag, class_=class_)

    return [article.text[-ARTICUL_LENGTH:] for article in articuls_]


def main(
    json_file: str,
    upload_file_type: str = "xlsx",
) -> None:
    """Single entry point for script

    Args:
        json_file (str): Absolute json file path or relative json path to python interpreter
        upload_file_type (str): Format of output file
    """
    articuls = create_list_from_json(json_file)
    full_urls_for_search = get_urls_for_search(articuls)
    responses_list = do_requests(full_urls_for_search)
    full_urls_list = create_list_of_full_urls(responses_list)
    responses = do_requests(full_urls_list)

    d = {
        art: find_recommended_articuls(res, **id_of_recommended_articuls)
        for art, res in zip(articuls, responses)
    }

    if upload_file_type == "xlsx":
        dict_to_excel(d)
    else:
        json_filename = str(datetime.datetime.now()) + ".json"
        with open(json_filename, "w") as new_json:
            ujson.dump(d, new_json, indent=4)


if __name__ == "__main__":
    import time

    parser = argparse.ArgumentParser(__name__)
    parser.add_argument(
        "json",
        help="json to parse",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--type",
        help="type of output file",
        type=str,
        choices=["json", "xlsx"],
        default="xlsx",
    )
    args = parser.parse_args()

    print(args)

    start_time = time.time()
    main(args.json, args.type)
    print(time.time() - start_time)
