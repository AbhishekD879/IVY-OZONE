# -*- coding: utf-8 -*-
import pytest
import xmltodict
import requests
import tests
from tests.base_test import vtest
from tests.base_test import BaseTest


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.navigation
@pytest.mark.slow
@pytest.mark.timeout(3600)
@vtest
class Test_C11547276_Verify_all_static_routes_redirect_from_url(BaseTest):
    """
    TR_ID: C11547276
    NAME: Verify all static routes redirect from url
    DESCRIPTION: Cover all static routes across sports.coral.co.uk and include it into daily run:
    DESCRIPTION: https://sports.coral.co.uk/sitemap.xml
    """
    keep_browser_open = True

    def get_dict_from_site_map(self):
        url = f'https://{tests.HOSTNAME}/sitemap.xml'
        get_content = requests.get(url).content
        convert_to_dict = xmltodict.parse(get_content)
        return convert_to_dict['urlset']['url']

    def test_001_verify_url_from_https_sports_coral_co_uk_sitemap_xml(self):
        """
        DESCRIPTION: Verify url from https://sports.coral.co.uk/sitemap.xml
        EXPECTED: redirected url match actual url
        """
        list_of_site_urls = self.get_dict_from_site_map()
        error_url_list = []
        for item in list_of_site_urls:
            format_url = item['loc']
            self.device.open_url(format_url)
            self.site.wait_splash_to_hide()
            current = self.device.get_current_url()
            if format_url not in current:
                error_url_list.append(f'Expected url "{format_url}" does not match current "{current}"')
        self.assertFalse(error_url_list, msg=f'URL does not opened {error_url_list}.')
