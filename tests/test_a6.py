#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from loguru import logger

# from tuan_lib.services.a6.service import A6ServiceFactory


# def test_product_get_all():
#     params = {"id": 1, "codex": "123", "status": 2}
#     response = A6ServiceFactory.fromService('product').get_all(params)
#     logger.info(response)
#
#
# def test_product_get_by_id():
#     response = A6ServiceFactory.fromService('product').get_by_id({'id': 1})
#     logger.info(response)
#
#
# def test_product_create():
#     response = A6ServiceFactory.fromService('product').create({'codex': 1})
#     logger.info(response)
#
#
# def test_product_update():
#     response = A6ServiceFactory.fromService('product').update({'id': 1, 'codex': 2})
#     logger.info(response)
#
#
# def test_product_parent_get_all():
#     response = A6ServiceFactory.fromService('product_parent').get_all()
#     logger.info(response)
#
#
# def test_product_parent_get_by_id():
#     response = A6ServiceFactory.fromService('product_parent').get_by_id({'id': 1})
#     logger.info(response)
#
#
# def test_product_parent_create():
#     response = A6ServiceFactory.fromService('product_parent').create({
#         'title': 'Something title',
#         'status': 2
#     })
#     logger.info(response)
#
#
# def test_product_parent_update():
#     response = A6ServiceFactory.fromService('product_parent').update({
#         'id': 1,
#         'status': 1,
#     })
#     logger.info(response)
#
#
# def test_product_supplier_create():
#     response = A6ServiceFactory.fromService('product_supplier').create({
#         'supplier_id': 43,
#         'product_id': 2,
#         'code_length': 0,
#         'product_code': 'test',
#         'supplier_api_config': None,
#         'whoexport': 1,
#         'supplier_value': 10000,
#         'code_prefix': 'TE'
#     })
#     logger.info(response)
#
#
# def test_product_supplier_update():
#     response = A6ServiceFactory.fromService('product_supplier').update({
#         'id': 1,
#         'status': 2
#     })
#     logger.info(response)


def test_redis():
    cookies = {'urb___hash__': 'e775205a32cfd8e60486d568090d00a0'}
    for i in range(2001, 3000):
        response = requests.get(f'https://hub.urbox.vn/ajax/system/resetGiftCodeStatusByGiftDetail?id={i}', cookies=cookies)
        logger.info(response)
