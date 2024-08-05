import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C66044314_Verify_the_display_of_selections_in_this_module_contains_all_the_other_Fanzone_team_selections(Common):
    """
    TR_ID: C66044314
    NAME: Verify the display of selections in this module contains all the other Fanzone team selections
    DESCRIPTION: This testcase verifies the display of selections in this module contains all the other Fanzone team selections
    PRECONDITIONS: 1. Navigation in CMS -> CMS -> Sports categories page->Fanzone- Bets based on other fans module should be enabled.
    PRECONDITIONS: 2. CMS -> Fanzone -> Fanzones -> Click on Fanzone name -> Go to Fanzone configurations -> Toggle should be on for -> Show bets based on your team and Show bets based on other Fanzone Team
    """
    keep_browser_open = True

    def test_000_launch_and_log_in_to_the_application(self):
        """
        DESCRIPTION: Launch and log in to the Application
        EXPECTED: User should launch and log in to the Application Successfully
        """
        pass

    def test_000_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: Fanzone page should load successfully
        """
        pass

    def test_000_verify_the_display_of_bets_based_on_other_fans_carousel_in_fanzone(self):
        """
        DESCRIPTION: Verify the Display of Bets based on other Fans Carousel in Fanzone
        EXPECTED: User should be able to see "Bets based on other fans" module
        """
        pass

    def test_000_verify_the_module(self):
        """
        DESCRIPTION: Verify the module
        EXPECTED: It should be in Open mode by default
        """
        pass

    def test_000_verify_the_display_of_selections_in_this_bets_based_on_other_fans_module_contains_all_the_other_fanzone_team_selections(self):
        """
        DESCRIPTION: Verify the display of selections in this "Bets based on other fans" module contains all the other Fanzone team selections
        EXPECTED: All the other Fanzone team selections should be visible in this module
        """
        pass
