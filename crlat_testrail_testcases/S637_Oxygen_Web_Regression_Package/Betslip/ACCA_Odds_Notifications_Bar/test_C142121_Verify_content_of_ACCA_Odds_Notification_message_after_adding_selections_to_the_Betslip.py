import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C142121_Verify_content_of_ACCA_Odds_Notification_message_after_adding_selections_to_the_Betslip(Common):
    """
    TR_ID: C142121
    NAME: Verify content of ACCA Odds Notification message after adding selections to the Betslip
    DESCRIPTION: This test case verifies ACCA Odds Notification displaying after adding selections to the Betslip
    DESCRIPTION: Odds calculation on ACCA notification instruction: https://confluence.egalacoral.com/display/SPI/Odds+calculation+on+ACCA+notification
    DESCRIPTION: AUTOTEST [C9697927]
    PRECONDITIONS: Application is loaded
    """
    keep_browser_open = True

    def test_001_go_to_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports Landing page
        EXPECTED: Sports Landing page is opened
        """
        pass

    def test_002_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: ACCA Odds Notification appears at the bottom of the screen but above Footer menu
        """
        pass

    def test_003_scroll_page_down_and_up(self):
        """
        DESCRIPTION: Scroll page down and up
        EXPECTED: * ACCA Odds Notification message is sticky
        EXPECTED: * ACCA Odds Notification message remains in the same place
        """
        pass

    def test_004_verify_acca_odds_notification_content(self):
        """
        DESCRIPTION: Verify ACCA Odds Notification content
        EXPECTED: ACCA Odds Notification contains the following information:
        EXPECTED: * Multiples name (Double, Treble, Accumulator (4), etc.) and Odds are displayed
        EXPECTED: * The odds are displayed in fractional format as default for logged OUT in user
        EXPECTED: * The odds are displayed in appropriate format depending on user preference i.e. decimal/ fractional for logged IN user
        EXPECTED: * An arrow is displayed to the right of the message bar
        """
        pass

    def test_005_verify_that_potential_payout_parameter_from_the_buildbet_response_is_displayed_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Verify that potential payout parameter from the buildBet response is displayed on ACCA Odds Notification message
        EXPECTED: * Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds
        """
        pass

    def test_006_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: The same are displayed on the Bestlip near relevant Multiple
        """
        pass

    def test_007_repeat_steps_2_5_for_races_lp_price_type_only(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Races (LP price type only)
        EXPECTED: 
        """
        pass
