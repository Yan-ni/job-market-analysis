from tests._utils import load_test_data
from scraper import Scraper
from bs4 import BeautifulSoup
import pytest
import os

__dirname = os.path.dirname(__file__)
__filename = os.path.basename(__file__)[0:-3]
TEST_DATA_DIR_PATH = os.path.join(__dirname, __filename)

test_data = load_test_data(TEST_DATA_DIR_PATH)

@pytest.mark.parametrize(('input', 'expected', 'test_name'), test_data)
def test_get_soup_test(input: str, expected: str, test_name: str):
  input_soup = BeautifulSoup(input, 'html.parser')

  output = Scraper.get_soup_text(input_soup)

  assert isinstance(output, str)
  assert output == expected, f'Test {test_name} failed'
