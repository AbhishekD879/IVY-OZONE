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
class Test_C66119944_Verify_watch_icon_display_for_BYB_BB_bet_in_My_BetsOpenCashout_When_streaming_is_available_for_the_event(Common):
    """
    TR_ID: C66119944
    NAME: Verify watch icon display for BYB/BB bet in My Bets(Open,Cashout) When streaming is available for the event
    DESCRIPTION: This testcase verifies watch icon display for BYB/BB bet in My Bets(Open,Cashout) When streaming is available for the event
    PRECONDITIONS: Football events which has both BYB data and streaming should be available
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        pass

    def test_002_click_on_football_event_which_has_byb_data(self):
        """
        DESCRIPTION: Click on Football event which has BYB data
        EXPECTED: Navigated to event details page
        """
        pass

    def test_003_place_bybbb_bet(self):
        """
        DESCRIPTION: Place BYB/BB bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_004_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_005_wait_until_the_event_is_kicked_off(self):
        """
        DESCRIPTION: Wait until the event is kicked off
        EXPECTED: Football event should start and show the watch icon for the event
        """
        pass

    def test_006_verify_the_location_of_watch_icon_for_bybbb_bet_in_open_tab(self):
        """
        DESCRIPTION: Verify the location of watch icon for BYB/BB bet in open tab
        EXPECTED: As per figma 'Watch' icon should be Vertically aligned with potential returns.
        EXPECTED: ![](index.php?/attachments/get/55bc4a5f-7927-43fc-89d3-cca6604cbe38)
        """
        pass

    def test_007_verify_the_location_of_watch_icon_for_bybif_available_bet_in_open_tab(self):
        """
        DESCRIPTION: Verify the location of watch icon for BYB(if available) bet in open tab
        EXPECTED: As per figma 'Watch' icon should be Vertically aligned with potential returns.
        EXPECTED: ![](index.php?/attachments/get/4dc8e6ac-a495-4660-9680-383945dc801d)
        """
        pass
