"""
Bing APIを使用して、画像検索してダウンロードするモジュール
* Bing API keyはenvファイルで設定
* 画像の保存先はsetting.pyに記述
"""
import configparser
from pathlib import Path
import requests
from settings import ROOT_PATH, RAW_DATA_PATH
from logging import getLogger, basicConfig, DEBUG
config = configparser.ConfigParser()
config.read(ROOT_PATH.joinpath('env'))
headers = {"Ocp-Apim-Subscription-Key": config['BingAPI']['api_key']}

END_POINT = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
COUNT = 150
MAX_DOWNLOAD = 500
QUERY = '乃木坂46'


def call_api(query, count, offset, logger=None):
    """
    Bing APIの呼び出し

    :param query:
    :param count:
    :param offset:
    :param logger:
    :return:
    """
    logger = logger or getLogger(__name__)
    params = {'q': query, 'count': count, 'offset': offset}
    logger.debug(f'Call api params: {params}')
    response = requests.get(END_POINT, headers=headers, params=params)
    response.raise_for_status()
    contents = response.json()
    logger.debug(f'{contents}')
    return contents


def get_result_count(query):
    contents = call_api(query, 1, 0)
    return contents['totalEstimatedMatches']


def get_image_urls_for_one_offset(query, offset, return_next_offset=False, logger=None):
    """
    Bing APIを叩いて検索結果を取得し、検索結果から画像のurlを取得する

    :param query:
    :param offset:
    :param return_next_offset:
    :param logger:
    :return:
    """
    logger = logger or getLogger(__name__)
    logger.debug(f'call api for offset: {offset}')
    contents = call_api(query, COUNT, offset, logger)
    if return_next_offset:
        return [content['contentUrl'] for content in contents['value']], contents['nextOffset']
    else:
        return [content['contentUrl'] for content in contents['value']]


def get_image_urls_for_all_offsets(query):
    """
    Bing APIの仕様上、検索結果が小分けでしか取得できないので、ループを回す

    :param query: str: 検索ワード
    :return:
    """
    current_offset = 0
    urls = []
    while True:
        urls_in_offset, next_offset = get_image_urls_for_one_offset(query, current_offset, True)
        urls.extend(urls_in_offset)
        if next_offset - current_offset < COUNT or next_offset > MAX_DOWNLOAD:
            break
        else:
            current_offset = next_offset
    return urls


def download_image(url, save_to: Path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with save_to.open('wb') as f:
        f.write(response.content)


def download_images_for_query(query, save_directory: Path, logger=None):
    """
    検索した画像を、指定の場所にダウンロードして保存する

    :param query: str: 検索ワード
    :param save_directory: Path: 保存先
    :param logger:
    :return:
    """
    logger = logger or getLogger(__name__)
    urls = get_image_urls_for_all_offsets(query)
    for url in urls:
        try:
            download_image(url, save_directory.joinpath(Path(url).name))
        except (requests.exceptions.HTTPError, requests.TooManyRedirects, requests.ConnectionError, OSError) as e:
            logger.warning(e)


if __name__ == '__main__':
    basicConfig(level=DEBUG)
    download_images_for_query(QUERY, RAW_DATA_PATH)