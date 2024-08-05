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
class Test_C66043619_Verify_the_Bet_Placement_when_we_add_selections_from_Bets_Based_on_your_team_module(Common):
    """
    TR_ID: C66043619
    NAME: Verify the Bet Placement when we add selections from Bets Based on your team module
    DESCRIPTION: This test case is to verify the selections added to betslip
    PRECONDITIONS: 1. Bets Based On Your Team Module and Bets Based On Other Fans Module is configured and Enabled in Fanzone.
    PRECONDITIONS: 2. CMS Navigations --
    PRECONDITIONS: CMS -> Sports Pages -> Sport Categories -> Fanzone -> Bets Based On Your Team Module & Bets Based On Other Fans Module
    PRECONDITIONS: 3. CMS -> Fanzone-> Fanzones -> Fanzone Name -> Fanzone Configurations -> ON/OFF Toggle for Show Bets Based On Your Team & Show Bets Based on Other Fanzone Team.
    PRECONDITIONS: 4. User should Subscribe to any Fanzone team
    """
    keep_browser_open = True

    def test_000_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and Login with Valid Credentials
        EXPECTED: User should launch the Application and Login Successfully
        """
        pass

    def test_000_navigate_to_fanzone(self):
        """
        DESCRIPTION: Navigate to Fanzone
        EXPECTED: Able to naviagte to the Fanzone page, and by default Now &amp; Next Tab should open
        """
        pass

    def test_000_verify_display_of_bets_based_on_your_team_module(self):
        """
        DESCRIPTION: Verify display of bets based on your team module
        EXPECTED: Able to see the bets based on your team module
        """
        pass

    def test_000_verify_the_display_of_max_number_of_betsselections_in_a_card_view_as_per_the_figma_design(self):
        """
        DESCRIPTION: Verify the display of max number of bets/selections in a card view as per the figma design
        EXPECTED: User could able to see the max number of bets in a card view as per the figma and max number configured in the cms
        """
        pass

    def test_000_click_on_any_selection(self):
        """
        DESCRIPTION: Click on any selection
        EXPECTED: User can able to add the selections to the betslip successfully
        """
        pass

    def test_000_navigate_to_betslip_page_and_place_a_bet(self):
        """
        DESCRIPTION: Navigate to Betslip page and place a bet
        EXPECTED: Able to navigate and place a bet successfully
        """
        pass

    def test_000_add_multiple_selections_to_the_betslip_and_verify_place_a_bet(self):
        """
        DESCRIPTION: Add multiple selections to the betslip and verify place a bet
        EXPECTED: Multiple bets are formed and able to place a bets successfully
        """
        pass
