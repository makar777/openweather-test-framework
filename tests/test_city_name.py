import pytest
import xml.etree.ElementTree as et
import json
from lib.network.http_utils import HttpUtils
from lib.constants.constants import Constants


@pytest.mark.parametrize("city_name",
                         ["San%20Jose", "san%20jose", "SAN%20JOSE", "sAn%20jOsE", "%20San%20Jose", "San%20Jose%20"])
def test_city_name_json(api_key, city_name):
    """
    Testing of different types of city name representation, including lower case, upper case, mixed case, camel case,
    leading space, trailing space.

    :param api_key: valid API key
    :param city_name: City name
    :return: Check that requested city name is presented in response json document.
    """
    request_url = f"{Constants.SERVICE_URI}q={city_name}&appid={api_key}"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == 200, f"Unexpected response code returned by service for a valid request: " \
                                 f"\n{request_url} " \
                                 f"\nExpected status is 200, returned status is {response_code} "

    json_data = json.loads(response_data.decode('utf-8'))
    assert json_data['name'] == Constants.SAN_JOSE_NAME


@pytest.mark.parametrize("city_name",
                         ["Mexico"])
def test_city_name_special_json(api_key, city_name):
    """
    Special case: city name equals to country name.

    :param api_key: valid API key
    :param city_name: City name
    :return: Check that requested city name is presented in response json document.
    """
    request_url = f"{Constants.SERVICE_URI}q={city_name}&appid={api_key}"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == 200, f"Unexpected response code returned by service for a valid request: " \
                                 f"\n{request_url} " \
                                 f"\nExpected status is 200, returned status is {response_code} "

    json_data = json.loads(response_data.decode('utf-8'))
    assert json_data['name'] == "Mexico"


@pytest.mark.parametrize("city_name, expected_response_code",
                         [("San*Jose", 404), ("", 400), ("%20", 404)])
def test_city_name_negative(api_key, city_name, expected_response_code):
    """
    Testing of different types of incorrect city name representation, including not existing city name,
    empty city name, space as city name.

    :param api_key: valid API key.
    :param city_name: City name.
    :param expected_response_code: Expected service response code.
    :return: Check that actual response code equals to expected response code.
    """
    request_url = f"{Constants.SERVICE_URI}q={city_name}&appid={api_key}"
    _, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == expected_response_code, f"Unexpected response code returned by service for a valid request: " \
                                                    f"\n{request_url} " \
                                                    f"\nExpected status is 200, returned status is {response_code} "


@pytest.mark.parametrize("city_name",
                         ["San%20Jose"])
def test_api_key_negative(city_name):
    """
    Testing of request with invalid API key.

    :param city_name: Valid city name
    :return: Check that response code equals to 401 - Unauthorized.
    """
    request_url = f"{Constants.SERVICE_URI}q={city_name}&appid={Constants.API_KEY_INVALID}"
    _, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == 401, "Unexpected response status is received for invalid API KEY."


@pytest.mark.parametrize("city_name",
                         ["San%20Jose", "san%20jose", "SAN%20JOSE", "sAn%20jOsE", "%20San%20Jose", "San%20Jose%20"])
def test_city_name_xml(api_key, city_name):
    """
    Testing of different types of city name representation, including lower case, upper case, mixed case, camel case,
    leading space, trailing space.

    :param api_key: valid API key
    :param city_name: City name
    :return: Check that requested city name is presented in response XML document.
    """
    request_url = f"{Constants.SERVICE_URI}q={city_name}&appid={api_key}&mode=xml"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == 200, f"Unexpected response code returned by service for a valid request: " \
                                 f"\n{request_url} " \
                                 f"\nExpected status is 200, returned status is {response_code} "
    tree = et.ElementTree(et.fromstring(response_data))
    root = tree.getroot()
    for node in root:
        tag = node.tag
        attribute = node.attrib
        if tag == 'city':
            assert attribute.get('name') == Constants.SAN_JOSE_NAME


@pytest.mark.parametrize("city_name",
                         ["San%20Jose", "san%20jose", "SAN%20JOSE", "sAn%20jOsE", "%20San%20Jose", "San%20Jose%20"])
def test_city_name_html(api_key, city_name):
    """
    Testing of different types of city name representation, including lower case, upper case, mixed case, camel case,
    leading space, trailing space.

    :param api_key: valid API key
    :param city_name: City name
    :return: Check that requested city name is presented in response HTML document.
    """
    request_url = f"{Constants.SERVICE_URI}q={city_name}&appid={api_key}&mode=html"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    decoded_response_data = response_data.decode('utf-8')
    assert f">{Constants.SAN_JOSE_NAME}<" in decoded_response_data

