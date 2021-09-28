import pytest
import json
import xml.etree.ElementTree as et
from lib.network.http_utils import HttpUtils
from lib.constants.constants import Constants



@pytest.mark.parametrize("lon, lat, expected_response_code",
                         [(1000, 1000, 400),('lon', 'lat', 400), ('', 37.3394, 400), (-121.895, '', 400),
                          ('', '', 400)])
def test_api_key_negative(api_key, lon, lat, expected_response_code):
    """
    Testing of incorrect longitude and latitude values as request parameters including:
    Incorrect lon and lat digit values, incorrect lon and lat string values, missed lon, missed lat, missed lon and lat.

    :param api_key: valid API key.
    :param lon: Longitude.
    :param lat: Latitude.
    :param expected_response_code: Expected response code.
    :return: Check that actual response code equals to expected response code.
    """
    request_url = f"{Constants.SERVICE_URI}lat={lat}&lon={lon}&appid={api_key}"
    _, response_status = HttpUtils.query_service(url=request_url)
    assert expected_response_code == response_status, "Unexpected response status is received for invalid API KEY."


@pytest.mark.parametrize("lon, lat",
                         [(-121.895, 37.3394), (-121.894, 37.3394), (-121.895, 37.3393), (-121.8951, 37.33941),
                          (-121.8949, 37.33939), ('-121.895', '37.3394')
                         ])
def test_lon_lat_json(api_key, lon, lat):
    """
    Testing of correct longitude and latitude values of San Jose city with different precision levels,
    string representation of longitude and latitude.

    :param api_key: valid API key.
    :param lon: Longitude.
    :param lat: Latitude.
    :return: Check that response JSON document contains requested longitude and latitude values.
    """
    request_url = f"{Constants.SERVICE_URI}lat={lat}&lon={lon}&appid={api_key}"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == 200, f"Unexpected response code returned by service for a valid request: " \
                                 f"\n{request_url} " \
                                 f"\nExpected status is 200, returned status is {response_code} "

    json_data = json.loads(response_data.decode('utf-8'))
    assert json_data['coord']['lon'] == float(lon)
    assert json_data['coord']['lat'] == float(lat)
    assert json_data['name'] == Constants.SAN_JOSE_NAME


@pytest.mark.parametrize("lon, lat",
                         [(-121.895, 37.3394), (-121.894, 37.3394), (-121.895, 37.3393), (-121.8951, 37.33941),
                          (-121.8949, 37.33939), ('-121.895', '37.3394')])
def test_lon_lat_xml(api_key, lon, lat):
    """
    Testing of correct longitude and latitude values of San Jose city with different precision levels,
    string representation of longitude and latitude.

    :param api_key: valid API key.
    :param lon: Longitude.
    :param lat: Latitude.
    :return: Check that response XML document contains requested longitude and latitude values.
    """
    request_url = f"{Constants.SERVICE_URI}lat={lat}&lon={lon}&appid={api_key}&mode=xml"
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
            for child in node.iter():
                child_tag = child.tag
                child_attribute = child.attrib
                if child_tag == 'coord':
                    assert child_attribute.get('lon') == str(lon)
                    assert child_attribute.get('lat') == str(lat)


@pytest.mark.parametrize("lon, lat",
                         [(-121.895, 37.3394), (-121.894, 37.3394), (-121.895, 37.3393), (-121.8951, 37.33941),
                          (-121.8949, 37.33939), ('-121.895', '37.3394')])
def test_lon_lat_html(api_key, lon, lat):
    """
    Testing of correct longitude and latitude values of San Jose city with different precision levels,
    string representation of longitude and latitude.

    :param api_key: valid API key.
    :param lon: Longitude.
    :param lat: Latitude.
    :return: Check that response HTML document contains requested longitude and latitude values.
    """
    request_url = f"{Constants.SERVICE_URI}lat={lat}&lon={lon}&appid={api_key}&mode=html"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    decoded_response_data = response_data.decode('utf-8')
    assert f">{Constants.SAN_JOSE_NAME}<" in decoded_response_data


@pytest.mark.parametrize("lon, lat",
                         [(-121.895, 37.3394), (-121.894, 37.3394), (-121.895, 37.3393), (-121.8951, 37.33941),
                          (-121.8949, 37.33939), ('-121.895', '37.3394')
                         ])
def test_lon_lat_json_reduce_precision(api_key, lon, lat):
    """
    Testing of correct longitude and latitude values of San Jose city with lowered precision level,
    string representation of longitude and latitude.

    :param api_key: valid API key.
    :param lon: Longitude.
    :param lat: Latitude.
    :return: Check that response JSON document contains requested longitude and latitude values.
    """
    request_url = f"{Constants.SERVICE_URI}lat={lat}&lon={lon}&appid={api_key}"
    response_data, response_code = HttpUtils.query_service(url=request_url)
    assert response_code == 200, f"Unexpected response code returned by service for a valid request: " \
                                 f"\n{request_url} " \
                                 f"\nExpected status is 200, returned status is {response_code} "

    json_data = json.loads(response_data.decode('utf-8'))
    assert round(float(json_data['coord']['lon']), 2) == round(float(lon), 2)
    assert round(float(json_data['coord']['lat']), 2) == round(float(lat), 2)
    assert json_data['name'] == Constants.SAN_JOSE_NAME
