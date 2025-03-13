from http import HTTPStatus

import pytest
from assertions.objects_assertion import should_be_posted_success, should_be_updated_success, should_be_deleted_success, \
    should_be_valid_objects_response

from api.api_client import ApiClient
from api.objects_api import get_objects, get_object, post_object, put_object, delete_object
from assertions.assertion_base import assert_status_code, assert_response_body_fields, assert_bad_request, \
    assert_not_found, assert_empty_list, assert_schema, assert_not_exist
from models.object_models import ObjectOutSchema, ObjectCreateOutSchema, CustomObjCreateOutSchema, \
    ObjectUpdateOutSchema, CustomObjUpdateOutSchema
from utilities.files_utils import read_json_test_data, read_json_common_request_data


class TestObjects:
    """
    Тесты /objects
    """

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_objects(self, client, request):
        """
        получение заранее заготовленных объектов из базы с параметрами по-умолчанию,
        GET /objects
        """
        # получаем объекты из базы
        response = get_objects(client)

        # убеждаемся, что в ответ пришли объекты, которые мы ожидаем
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body_fields(request, response)

    @pytest.mark.parametrize("param", [{"index": 0, "ids": [1]}, {"index": 1, "ids": [1, 2]}])
    def test_get_objects_id_param(self, client, request, param):
        """
        получение заранее заготовленных объектов из базы с параметром ids,
        GET /objects
        """
        # получаем массив объектов с определенными айдишниками
        response = get_objects(client, *param['ids'])

        # убеждаемся, что в ответ пришли именно те объекты, id которых мы запросили
        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_objects_response(request, response, param)

    def test_get_objects_not_exist_id(self, client):
        """
        попытка получить из базы объект с несуществующим id,
        GET /objects
        """
        # пытаемся получить объект, несуществующий в системе
        response = get_objects(client, 8523697415)

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.OK)
        assert_empty_list(response)

    def test_get_objects_invalid_id(self, client):
        """
        попытка получить из базы объект с невалидным по типу id,
        GET /objects
        """
        # пытаемся получить объект, отправив невалидный по типу параметр ids
        response = get_objects(client, "kjdsf23321")

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.OK)
        assert_empty_list(response)

    def test_get_object(self, client, request):
        """
        получение заранее заготовленного объекта из базы,
        GET /objects/{id}
        """
        # получаем единичный объект с сервера
        response = get_object(client, 7)

        # убеждаемся, что получен именно тот объект, который мы запросили
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ObjectOutSchema)
        assert_response_body_fields(request, response)

    def test_get_object_not_exist(self, client, request):
        """
        попытка получить из базы единичный объект с несуществующим id,
        GET /objects/{id}
        """
        # запрашиваем единичный объект с сервера с несуществующим id
        response = get_object(client, 1593576458)

        # убеждаемся, что сервер вернул NOT FOUND ответ
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_not_exist(request, response, 1593576458)

    def test_post_object_empty_body(self, client, request):
        """
        запись объекта в базу с пустым телом,
        POST /objects
        """
        # записываем объект в базу с пустым телом
        response = post_object(client, json={})

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ObjectCreateOutSchema)
        should_be_posted_success(request, client, response, exp_obj={"data": None, "name": None})

    def test_post_object_with_full_body(self, client, request):
        """
        запись объекта в базу полностью заполненным телом,
        POST /objects
        """
        # записываем объект в базу со всеми заполненными полями
        exp_obj = read_json_common_request_data("valid_post_object")
        response = post_object(client, json=exp_obj)

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, CustomObjCreateOutSchema)
        should_be_posted_success(request, client, response, exp_obj)

    def test_post_object_send_invalid_json(self, client, request):
        """
        попытка записать в базу невалидный json,
        POST /objects
        """
        # отправляем запрос на запись объекта в базу с невалидным json в теле
        response = post_object(client, content='{"name",}', headers={"Content-Type": "application/json"})

        # убеждаемся, что сервер дал BAD REQUEST ответ
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_bad_request(request, response)