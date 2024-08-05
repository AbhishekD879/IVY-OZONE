import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29464_Verify_that_links_from_sitemapxml_are_present_in_application(Common):
    """
    TR_ID: C29464
    NAME: Verify that links from sitemap.xml are present in application
    DESCRIPTION: Test case verifys that all links from sitemap.xml are present in application.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-9279: SEO - Create Oxygen Site Map
    PRECONDITIONS: Use https://bm-tst2.coral.co.uk/sitemap.xml link for checking of links.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_httpsbm_tst2coralcouksitemapxml_link(self):
        """
        DESCRIPTION: Open https://bm-tst2.coral.co.uk/sitemap.xml link
        EXPECTED: 
        """
        pass

    def test_003_verify_if_every_link_from_the_list_in_xml_is_present_in_application(self):
        """
        DESCRIPTION: Verify if every link from the list in XML is present in application
        EXPECTED: All links from the list are present in aaplication
        """
        pass
