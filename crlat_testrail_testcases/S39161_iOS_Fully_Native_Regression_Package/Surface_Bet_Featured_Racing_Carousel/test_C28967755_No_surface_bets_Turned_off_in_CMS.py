import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C28967755_No_surface_bets_Turned_off_in_CMS(Common):
    """
    TR_ID: C28967755
    NAME: No surface bets/ Turned off in CMS
    DESCRIPTION: This test case verifies that surface bet carousel/container is not displayed when surface bet is not available (turned off in CMS for this page
    DESCRIPTION: OR when the last surface bet is either resulted/ suspended/undisplayed)
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. the surface bet is available (bet has been configured in CMS for this page)
    PRECONDITIONS: 3. there are more than 1 surface bet to be displayed
    """
    keep_browser_open = True

    def test_001_navigate_to_homepage_on_featured_tab(self):
        """
        DESCRIPTION: navigate to homepage on featured tab
        EXPECTED: homepage is displayed with featured tab
        EXPECTED: The surface bet carousel with more than 1 surface bet is displayed  as per design
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3077390)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/3077391)
        """
        pass

    def test_002_emulate_that_surface_bet_is_turned_off_in_cms_for_this_page_na(self):
        """
        DESCRIPTION: emulate that surface bet is turned off in CMS for this page (N/A)
        EXPECTED: Surface bet carousel/container is not displayed
        """
        pass

    def test_003_emulate_displaying_of_surface_bet(self):
        """
        DESCRIPTION: emulate displaying of surface bet
        EXPECTED: The surface bet carousel is displayed as in step1
        """
        pass
