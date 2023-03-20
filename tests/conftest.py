import pytest
from datetime import datetime

from app.backend.settings import Settings
from app.backend.filters import Filters
from app.backend.url_input import UrlInput

@pytest.fixture
def config1(): 
    class Mock():  
        settings = Settings()
        settings.estimate_scroll()
        filters = Filters()
        filters.add_or_remove_filter('add', 'NE', 'NS')
        url_input = UrlInput()
        url_input.url_list = ['https://soundcloud.com/headieone/headie-one-martins-sofa', 
                              'https://soundcloud.com/headieone/headie-one-x-abra-cadabra-x', 
                              'https://soundcloud.com/headieone/headie-one-50s']
        datetime = datetime.now()
    return Mock()

@pytest.fixture
def config2(): 
    class Mock():  
        settings = Settings()
        settings.estimate_scroll()
        settings.csv_merge = True
        settings.csvfilename = 'test_config2'
        filters = Filters()
        filters.add_or_remove_filter('add', 'NE', 'NS')
        url_input = UrlInput()
        url_input.url_list = ['https://soundcloud.com/headieone/headie-one-martins-sofa', 
                              'https://soundcloud.com/headieone/headie-one-x-abra-cadabra-x', 
                              'https://soundcloud.com/headieone/headie-one-50s']
        datetime = datetime.now()
    return Mock()

@pytest.fixture
def sample_url_list():
    return ['https://soundcloud.com/headieone/headie-one-martins-sofa', 
            'https://soundcloud.com/headieone/headie-one-x-abra-cadabra-x', 
            'https://soundcloud.com/headieone/headie-one-50s']