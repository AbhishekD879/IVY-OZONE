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
class Test_C66044315_Verify_the_display_of_Bets_based_on_other_fans_module_for_newly_subscribed_Fanzone_user(Common):
    """
    TR_ID: C66044315
    NAME: Verify the display of "Bets based on other fans" module for newly subscribed Fanzone user
    DESCRIPTION: This testcase verifies whether a newly subscribed fanzone user can see "Bets based on other fans" module
    PRECONDITIONS: 1. Navigation in CMS -> CMS -> Sports categories page->Fanzone- Bets based on other fans module should be enabled.
    PRECONDITIONS: 2. CMS -> Fanzone -> Fanzones -> Click on Fanzone name -> Go to Fanzone configurations -> Toggle should be on for -> Show bets based on your team and Show bets based on other Fanzone Team
    """
    keep_browser_open = True

    def test_000_create_a_new_user_login_to_application__and_subscribe_to_any_of_the_team_in_fanzone(self):
        """
        DESCRIPTION: Create a new User, login to application  and subscribe to any of the Team in Fanzone
        EXPECTED: User should be able to login to application successfully and subscribe to any of the team
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

    def test_000_verify_the_option_to_open_and_collapse_the_module_by_clicking_the_chevron(self):
        """
        DESCRIPTION: Verify the option to open and collapse the module by clicking the chevron
        EXPECTED: User should be able to open and collapse the module
        """
        pass

    def test_000_verify_adding_a_selection_to_betslip_from_bets_based_on_other_fans_module(self):
        """
        DESCRIPTION: Verify adding a selection to betslip from Bets based on other fans module
        EXPECTED: Selection should be added successfully to Betslip and able to place a bet
        """
        pass

    def test_000_verify_adding_multiple_selections_to_betslip(self):
        """
        DESCRIPTION: Verify adding multiple selections to Betslip
        EXPECTED: All the multiples should form like Double,Treble, Acca and so on and able to place a bet successfully
        """
        pass
