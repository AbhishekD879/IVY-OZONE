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
class Test_C11547280_Verify_all_static_routes_headers(Common):
    """
    TR_ID: C11547280
    NAME: Verify all static routes headers
    DESCRIPTION: Cover all static routes across sports.coral.co.uk and include it into daily run:
    DESCRIPTION: https://sports.coral.co.uk/sitemap.xml
    DESCRIPTION: Verify that headers are displayed and names displayed
    PRECONDITIONS: Go to https://sports.coral.co.uk/sitemap.xml
    """
    keep_browser_open = True

    def test_001_verify_headers_from_url_from_httpssportscoralcouksitemapxml(self):
        """
        DESCRIPTION: Verify headers from url from https://sports.coral.co.uk/sitemap.xml
        EXPECTED: - headers are displayed and sport name is shown
        EXPECTED: - sport names in sub-header matches with sport names  in url
        """
        pass
