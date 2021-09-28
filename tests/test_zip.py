import pytest
import json
import xml.etree.ElementTree as et
from lib.network.http_utils import HttpUtils
from lib.constants.constants import Constants



@pytest.mark.parametrize("_zip, expected_response_code",
                         [(95128, 401)])
def test_api_key_negative(_zip, expected_response_code):
    """
    Testing of request with invalid API key.

    :param _zip: Valid zip code.
    :return: Check that response code equals to 401 - Unauthorized.
    """
    request_url = f"{Constants.SERVICE_URI}zip={_zip}&appid={Constants.API_KEY_INVALID}"
    _, response_status = HttpUtils.query_service(url=request_url)
    assert expected_response_code == response_status, "Unexpected response status is received for invalid API KEY."


@pytest.mark.parametrize("_zip, country_code, expected_response_code",
                         [(0, "", 400), (10000, ",US", 404)])
def test_zip_not_found_negative(api_key, _zip, country_code, expected_response_code):
    """
    Testing of request with missed zip codes. Includes the following cases:
    zip code does not exist around the world,
    zip code does not exist in specified country but can be found in different country.

    :param api_key: valid API key.
    :param _zip: zip code.
    :param country_code: country code.
    :param expected_response_code: expected response code.
    :return: Check that actual response code equals to expected response code.
    """
    request_url = f"{Constants.SERVICE_URI}zip={_zip}{country_code}&appid={api_key}"
    _, response_status = HttpUtils.query_service(url=request_url)
    assert expected_response_code == response_status, "Unexpected response status is received for invalid API KEY."


@pytest.mark.parametrize("_zip, country_code, expected_city",
                         [(95128, "", Constants.SAN_JOSE_NAME),
                          (95128, ",US", Constants.SAN_JOSE_NAME),
                          (10000, ",FR", Constants.TROYES_NAME)])
def test_zip_json(api_key, _zip, country_code, expected_city):
    """
    Testing of different combinations of zip code and country code values, including missed country code
    to test how default value works, specified both zip and country codes.

    :param api_key: valid API key
    :param _zip: zip code.
    :param country_code: country code.
    :param expected_city: expected city name.
    :return: Check that expected city name is presented in response json document.
    """
    request_url = f"{Constants.SERVICE_URI}zip={_zip}{country_code}&appid={api_key}"
    response_data, response_status = HttpUtils.query_service(url=request_url)
    assert response_status == 200, f"Unexpected response status returned by service for a valid request: " \
                                   f"\n{request_url} " \
                                   f"\nExpected status is 200, returned status is {response_status} "

    json_data = json.loads(response_data.decode('utf-8'))
    assert json_data['name'] == expected_city, "Corresponding city name is not found in json response."


@pytest.mark.parametrize("_zip, country_code, expected_city",
                         [(95128, "", Constants.SAN_JOSE_NAME),
                          (95128, ",US", Constants.SAN_JOSE_NAME),
                          (10000, ",FR", Constants.TROYES_NAME)])
def test_zip_xml(api_key, _zip, country_code, expected_city):
    """
    Testing of different combinations of zip code and country code values, including missed country code
    to test how default value works, specified both zip and country codes.

    :param api_key: valid API key
    :param _zip: zip code.
    :param country_code: country code.
    :param expected_city: expected city name.
    :return: Check that expected city name is presented in response XML document.
    """
    request_url = f"{Constants.SERVICE_URI}zip={_zip}{country_code}&appid={api_key}&mode=xml"
    response_data, response_status = HttpUtils.query_service(url=request_url)
    assert response_status == 200, f"Unexpected response status returned by service for a valid request: " \
                                   f"\n{request_url} " \
                                   f"\nExpected status is 200, returned status is {response_status} "

    decoded_data = response_data.decode('utf-8')
    tree = et.ElementTree(et.fromstring(decoded_data))
    root = tree.getroot()
    for node in root:
        tag = node.tag
        attribute = node.attrib
        if tag == 'city':
            assert attribute.get('name') == expected_city, "Corresponding city name is not found in html response."


@pytest.mark.parametrize("_zip, country_code, expected_city",
                         [(95128, "", Constants.SAN_JOSE_NAME),
                          (95128, ",US", Constants.SAN_JOSE_NAME),
                          (10000, ",FR", Constants.TROYES_NAME)])
def test_zip_html(api_key, _zip, country_code, expected_city):
    """
    Testing of different combinations of zip code and country code values, including missed country code
    to test how default value works, specified both zip and country codes.

    :param api_key: valid API key
    :param _zip: zip code.
    :param country_code: country code.
    :param expected_city: expected city name.
    :return: Check that expected city name is presented in response HTML document.
    """
    request_url = f"{Constants.SERVICE_URI}zip={_zip}{country_code}&appid={api_key}&mode=html"
    response_data, response_status = HttpUtils.query_service(url=request_url)
    decoded_data = response_data.decode('utf-8')
    assert response_status == 200, f"Unexpected response status returned by service for a valid request: " \
                                   f"\n{request_url} " \
                                   f"\nExpected status is 200, returned status is {response_status} "
    assert f">{expected_city}<" in decoded_data, "Corresponding city name is not found in html response."
