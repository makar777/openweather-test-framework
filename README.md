## Python-based test framework for https://openweathermap.org web service.

#### This framework requires **Python 3.9** and uses **PyTest** as a testing framework.

### Installing:

* Get your API key for open weather API: https://openweathermap.org/faq => "How to get an API key"

* Install Python 3.9;

* Go to project directory and `$pip3 install -r requirements.txt`;

### Running:

* To run all tests suites:
`pytest --api_key=YOUR_API_KEY --html=report.html --self-contained-html`
`report.html` report file will be generated and stored into project root directory

* To run specified test suite:
`pytest tests/DESIRED_TEST_SUITE.py --api_key=YOUR_API_KEY`

### Verification:
* `test_city_name.py` - Verifies `name` attribute corresponds to the entered city name
* `test_lon_lat.py` - Verifies `coord.lat` and `coord.lon` attributes correspond to the ones entered
* `test_zip.py` - Verifies `name` attribute corresponds to the city that contains the ZIP code
 
### Test results:
Open `report.html` to see tests results.
Some tests in `test_lon_lat.py` are failed because openweather `coord.lat` and `coord.lon` attributes do not correspond to the ones entered.
For example, instead of `37.3393,-121.895` it will return `37.3394,-121.8863`.
It is an openweather API bug.

In test `test_lon_lat_json_reduce_precision` you can find if reduce precision by 2 (`round(float(json_data['coord']['lon']), 2) == round(float(lon), 2)`), tests will pass.
