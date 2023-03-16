from app.backend.url_input import UrlInput

def test_add_url_file():
    test_url_input = UrlInput()
    test_url_input.add_url_file('tests/test_data/test_urls.txt')
    assert test_url_input.url_list == ["https://soundcloud.com/headieone/headie-one-martins-sofa",
                                     "https://soundcloud.com/headieone/headie-one-x-abra-cadabra-x",
                                     "https://soundcloud.com/headieone/headie-one-50s"]
