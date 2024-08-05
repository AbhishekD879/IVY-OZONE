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
class Test_C66119941_Verify_football_commentary_at_selection_level_for_5A_Side_bets_in_my_bets_area(Common):
    """
    TR_ID: C66119941
    NAME: Verify football commentary at selection level for 5A Side bets in my bets area
    DESCRIPTION: BYB data should be available to place bets
    PRECONDITIONS: This testcase verifies football commentary at selection level for 5A Side bets in my bets area
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

    def test_002_place_5a_side_bet(self):
        """
        DESCRIPTION: Place 5A side bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_wait_until_the_event_is_kicked_off(self):
        """
        DESCRIPTION: Wait until the event is kicked off
        EXPECTED: Football event should start and show the commentary for the event
        """
        pass

    def test_005_verify_the_location_of_football_commentary_for_5a_side_bet_in_open_tab(self):
        """
        DESCRIPTION: Verify the location of football commentary for 5A side bet in open tab
        EXPECTED: The location of the football commentary should be displayed below player bets data as per figma
        EXPECTED: ![](index.php?/attachments/get/5c973c77-0485-4804-985d-83e508d464aa)
        """
        pass

    def test_006_verify_step_6_in_cashout_tabif_cash_out_is_available(self):
        """
        DESCRIPTION: Verify step 6 in cashout tab(if cash out is available)
        EXPECTED: Result should be same
        """
        pass
