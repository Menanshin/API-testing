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