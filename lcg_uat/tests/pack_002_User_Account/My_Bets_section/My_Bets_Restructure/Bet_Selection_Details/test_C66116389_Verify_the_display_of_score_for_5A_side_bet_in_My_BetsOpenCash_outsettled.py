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
class Test_C66116389_Verify_the_display_of_score_for_5A_side_bet_in_My_BetsOpenCash_outsettled(Common):
    """
    TR_ID: C66116389
    NAME: Verify the display of score for 5A side bet in My Bets(Open,Cash out,settled)
    DESCRIPTION: This testcase verifies the display of score for 5A side bet in My Bets(Open,Cash out,settled)
    PRECONDITIONS: 5A side bet should be available in Open,Cashout tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_5a_side_bet_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify 5A side bet displayed in open tab
        EXPECTED: 5A side be should be diasplayed with all the bet details
        """
        pass

    def test_004_verify_display_of_score_for_5a_side_event_in_open_tab_when_the_event_starts(self):
        """
        DESCRIPTION: Verify display of score for 5A side event in open tab when the event starts
        EXPECTED: Score should be displayed below the 5A side title as per figma
        """
        pass

    def test_005_verify_display_of_score_for_5a_side_event_in_cash_outif_available_tab_when_the_event_starts(self):
        """
        DESCRIPTION: Verify display of score for 5A side event in Cash out(if available) tab when the event starts
        EXPECTED: Score should be displayed below the 5A side title as per figma
        """
        pass

    def test_006_verify_display_of_score_for_5a_side_event_in_settled_tab_when_the_event_resulted(self):
        """
        DESCRIPTION: Verify display of score for 5A side event in Settled tab when the event resulted
        EXPECTED: Score should be displayed below the 5A side title as per figma
        """
        pass
