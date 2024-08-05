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
class Test_C57732002_Verify_navigation_to_1_2_FREE_from_different_pages(Common):
    """
    TR_ID: C57732002
    NAME: Verify navigation to 1-2-FREE from different pages
    DESCRIPTION: This test case verifies navigation to 'Splash screen' from Homepage and Football landing page
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE-4s...' is available on Home, Cricket sports, Event Hub pages
    PRECONDITIONS: 3. AEM banner 'Play 1-2-FREE-4s...' is available on Home, Cricket sports, Event Hub pages
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_quick_link_on_homepage(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE...' quick link on Homepage
        EXPECTED: '1-2-Free' is successfully opened
        """
        pass

    def test_002_tap_on_play_1_2_free_aem_banner_on_homepage(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE...' AEM banner on Homepage
        EXPECTED: '1-2-Free' is successfully opened
        """
        pass

    def test_003_tap_on_play_1_2_free_quick_link_on_football_sports_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE...' quick link on Football sports page
        EXPECTED: '1-2-Free' is successfully opened
        """
        pass

    def test_004_tap_on_play_1_2_free_aem_banner_on_football_sports_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE...' AEM banner on Football sports page
        EXPECTED: '1-2-Free' is successfully opened
        """
        pass

    def test_005_type_url_eg_httpsmsportsladbrokescom1_2_free_of_1_2_free_directly_in_the_browser(self):
        """
        DESCRIPTION: Type URL (e.g. https://msports.ladbrokes.com/1-2-free) of 1-2-Free directly in the browser
        EXPECTED: '1-2-Free' is successfully opened
        """
        pass

    def test_006_surf_to_others_pages_and_page_block_of_httpsmladbrokescom_eg_footer_cricket_sports_page(self):
        """
        DESCRIPTION: Surf to others pages and page block of https://m.ladbrokes.com (eg. Footer, Cricket sports page)
        EXPECTED: 'Play 1-2-FREE...' should only accessible from Homepage and Football sports page
        """
        pass
