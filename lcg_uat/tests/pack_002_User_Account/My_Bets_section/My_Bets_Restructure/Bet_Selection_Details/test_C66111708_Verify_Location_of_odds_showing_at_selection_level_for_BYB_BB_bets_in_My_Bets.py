import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66111708_Verify_Location_of_odds_showing_at_selection_level_for_BYB_BB_bets_in_My_Bets(Common):
    """
    TR_ID: C66111708
    NAME: Verify Location of odds showing at selection level for BYB/BB bets in My Bets
    DESCRIPTION: This testcase verifies the location of odds showing at selection level for BYB/BB bets in My Bets
    PRECONDITIONS: BYB/BB bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_location_of_odds_displayed_for_the_bybbb_bets_in_open_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the BYB/BB bets in Open tab
        EXPECTED: Location of the Odds should be displayed at bet level. Should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/31014a58-0f82-4a8f-8803-8855a5bd11cd)  ![](index.php?/attachments/get/4c1fdf73-8438-49f2-ab65-1083ac74467d)
        """
        pass

    def test_004_verify_location_of_odds_displayed_for_the_bybbb_bets_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the BYB/BB bets in Cash out tab
        EXPECTED: Location of the Odds should be displayed at bet level. Should be displayed as per figma
        """
        pass

    def test_005_verify_location_of_odds_displayed_for_the_bybbb_bets_in_settled_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the BYB/BB bets in Settled tab
        EXPECTED: Location of the Odds should be displayed at bet level. Should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/a6751f6a-698c-4030-920f-34b123985c61)
        """
        pass
