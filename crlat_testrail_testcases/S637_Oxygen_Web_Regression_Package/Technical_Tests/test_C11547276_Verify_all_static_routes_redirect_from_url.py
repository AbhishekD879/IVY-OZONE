import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C11547276_Verify_all_static_routes_redirect_from_url(Common):
    """
    TR_ID: C11547276
    NAME: Verify all static routes redirect from url
    DESCRIPTION: Cover all static routes across sports.coral.co.uk and include it into daily run:
    DESCRIPTION: https://sports.coral.co.uk/sitemap.xml
    PRECONDITIONS: Go to https://sports.coral.co.uk/sitemap.xml
    """
    keep_browser_open = True

    def test_001_verify_that_each_url_from_httpssportscoralcouksitemapxml_is_actual(self):
        """
        DESCRIPTION: Verify that each url from https://sports.coral.co.uk/sitemap.xml is actual
        EXPECTED: Redirected url match actual url
        EXPECTED: User is redirected to appropriate site page
        """
        pass

    def test_002_verify_that_sub_header_in_url_match_sub_header_name_on_page(self):
        """
        DESCRIPTION: Verify that sub-header in url match sub-header name on page
        EXPECTED: Sub-header in url match sub-header name on page
        """
        pass
