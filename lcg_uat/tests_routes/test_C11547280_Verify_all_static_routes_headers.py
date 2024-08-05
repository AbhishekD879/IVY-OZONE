# -*- coding: utf-8 -*-
import pytest
import xmltodict
import requests
import tests
from tests.base_test import vtest
from tests.base_test import BaseTest
from voltron.utils.helpers import find_element


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.navigation
@pytest.mark.slow
@pytest.mark.timeout(3600)
@vtest
class Test_C11547280_Verify_all_static_routes_headers(BaseTest):
    """
    TR_ID: C11547280
    NAME: Verify all static routes headers
    DESCRIPTION: Cover all static routes across sports.coral.co.uk and include it into daily run:
    DESCRIPTION: https://sports.coral.co.uk/sitemap.xml
    DESCRIPTION: Verify that headers are displayed and names displayed
    """
    keep_browser_open = True

    def get_dict_from_site_map(self):
        url = f'https://{tests.HOSTNAME}/sitemap.xml'
        get_content = requests.get(url).content
        convert_to_dict = xmltodict.parse(get_content)
        return convert_to_dict['urlset']['url']

    def test_001_verify_headers_from_url__httpssportscoralcouksitemapxml(self):
        """
        DESCRIPTION: Verify headers from url from https://sports.coral.co.uk/sitemap.xml
        EXPECTED: headers are displayed and sport name is shown
        """
        list_of_site_urls = self.get_dict_from_site_map()
        error_header_list = []
        header_text = {}
        for item in list_of_site_urls:
            format_url = item['loc']
            self.device.open_url(format_url)
            self.site.wait_splash_to_hide()
            current = self.device.get_current_url()
            header = self.site.header if f'https://{tests.HOSTNAME}/' == current \
                else find_element(selector="xpath=.//*[@data-crlat='topBarTitle' or @data-crlat='signUpTitle']")

            if not header:
                error_header_list.append(f'Header is not displayed on page "{current}"')
            if header and f'https://{tests.HOSTNAME}/' != current:
                header_text[current] = header.text
        self.assertEqual(error_header_list, [], msg=f'Headers are not displayed on {error_header_list}.')
        self.assertNotIn('KEY_NOT_FOUND', header_text, msg=f'Wrong header text for pages "{list(header_text.keys())}"')
