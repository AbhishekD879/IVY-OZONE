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
class Test_C66114018_Verify_displaying_of_icon_for_result_below_the_event_name_at_selection_level_for_won_and_placed_horses_in_Settled_tab(Common):
    """
    TR_ID: C66114018
    NAME: Verify displaying of icon for result below the event name at selection level for won and placed horses in Settled tab
    DESCRIPTION: This test case Verify displaying of icon for result below the event name at selection level for won and placed horses in Settled tab
    PRECONDITIONS: Bets should be available in Settle tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_002_navigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to Horse racing page
        EXPECTED: HR landing page is opened
        """
        pass

    def test_003_place_single_bets_on__races(self):
        """
        DESCRIPTION: Place single bets on  Races
        EXPECTED: Bets should be placed successfully
        """
        pass

    def test_004_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        pass

    def test_005_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_006_check_the_bets_placed_for_single(self):
        """
        DESCRIPTION: Check the bets placed for single
        EXPECTED: Bets should be available in open tab
        """
        pass

    def test_007_click_on_settle_tab_after_the_above_bets_are_settled(self):
        """
        DESCRIPTION: Click on Settle tab after the above bets are settled
        EXPECTED: Bets should be available in settle tab after settlement
        """
        pass

    def test_008_check_the_lcon_result_places_display_for_single_selections(self):
        """
        DESCRIPTION: Check the lcon Result places display for single selections
        EXPECTED: Icon &amp; result places to be displayed below the event name
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/ce3af98a-342a-4e67-85fc-3de97eb93fce)
        EXPECTED: ![](index.php?/attachments/get/f5ece5b6-7481-43fb-bfff-387eb18c5023)
        """
        pass
