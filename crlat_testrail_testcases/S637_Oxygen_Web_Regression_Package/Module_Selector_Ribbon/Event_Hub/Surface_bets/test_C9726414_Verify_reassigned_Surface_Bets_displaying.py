import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C9726414_Verify_reassigned_Surface_Bets_displaying(Common):
    """
    TR_ID: C9726414
    NAME: Verify reassigned Surface Bets displaying
    DESCRIPTION: Test case verifies that Surface Bet can be reassigned to other category
    PRECONDITIONS: 1. There are a Surface Bet added to the SLP in the CMS
    PRECONDITIONS: 2. Open the Home page, SLP and Event hub tab in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Event Hub > <eventHub> > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_edit_the_surface_bet_uncheck_display_on_highlights_tab_assign_the_surface_bet_to_some_slp_and_event_hub(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet, uncheck "Display on Highlights tab", assign the Surface Bet to some SLP and Event Hub
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_home_page_and_slp_and_verify_surface_bet_is_reassigned_to_other_category(self):
        """
        DESCRIPTION: In the application refresh Home page and SLP and verify Surface Bet is reassigned to other category
        EXPECTED: * Surface Bet is shown on the sport category landing page
        EXPECTED: * Surface Bet is shown on the Event Hub tab
        EXPECTED: * Surface Bet isn't shown on the Home page
        """
        pass

    def test_003_in_the_cms_revert_changes_from_the_1st_step(self):
        """
        DESCRIPTION: In the CMS revert changes from the 1st step.
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_refresh_home_page_and_slp_and_verify_surface_bet_is_reassigned(self):
        """
        DESCRIPTION: In the application refresh Home page and SLP and verify Surface Bet is reassigned
        EXPECTED: * Surface Bet isn't shown on the sport category landing page
        EXPECTED: * Surface Bet isn't shown on the Event Hub tab
        EXPECTED: * Surface Bet is shown on the Home page
        """
        pass
