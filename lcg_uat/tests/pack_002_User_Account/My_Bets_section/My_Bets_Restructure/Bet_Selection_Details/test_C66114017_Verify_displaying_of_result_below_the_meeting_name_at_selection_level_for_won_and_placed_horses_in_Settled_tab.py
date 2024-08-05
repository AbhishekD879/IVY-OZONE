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
class Test_C66114017_Verify_displaying_of_result_below_the_meeting_name_at_selection_level_for_won_and_placed_horses_in_Settled_tab(Common):
    """
    TR_ID: C66114017
    NAME: Verify displaying of result below the meeting name at selection level for won and placed horses in Settled tab
    DESCRIPTION: This test case Verify displaying of result below the meeting name at selection level for won and placed horses in Settled tab
    PRECONDITIONS: Bets should be available in open/cashout tabs
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

    def test_008_check_the_result_location_display_for_single_selections(self):
        """
        DESCRIPTION: Check the result location display for single selections
        EXPECTED: Result to be displayed below the event name in line with REPLAY ICON
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/394f1493-ba65-41b2-867c-3013c23d05b7)
        EXPECTED: ![](index.php?/attachments/get/5a10afb6-122a-4c00-a629-91756521e428)
        """
        pass
