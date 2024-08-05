import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732073_Verify_navigation_to_Correct_4_from_different_pages(Common):
    """
    TR_ID: C57732073
    NAME: Verify navigation to Correct 4 from different pages
    DESCRIPTION: This test case verifies navigation to Correct 4 from different pages
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Link 'Correct 4' is available on the Homepage or any other
    PRECONDITIONS: 3. Banner to 'Correct 4' is available on the Homepage or any other
    PRECONDITIONS: 4. Any other links (eg. Super button, menu item) to 'Correct 4' configured on CMS and are available on the website
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link_on_homepage(self):
        """
        DESCRIPTION: Tap on Correct 4 link on Homepage
        EXPECTED: Correct 4 is successfully opened
        """
        pass

    def test_002_tap_on_correct_4_banner_on_homepage(self):
        """
        DESCRIPTION: Tap on Correct 4 banner on Homepage
        EXPECTED: Correct 4 is successfully opened
        """
        pass

    def test_003_tap_on_any_other_configured_from_cms_links_to_correct_4(self):
        """
        DESCRIPTION: Tap on any other configured from CMS links to Correct 4
        EXPECTED: Correct 4 is successfully opened
        """
        pass
