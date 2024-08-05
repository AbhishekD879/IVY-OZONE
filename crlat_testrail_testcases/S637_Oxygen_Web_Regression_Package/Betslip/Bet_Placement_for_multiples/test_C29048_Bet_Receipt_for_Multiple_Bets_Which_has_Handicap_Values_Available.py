import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29048_Bet_Receipt_for_Multiple_Bets_Which_has_Handicap_Values_Available(Common):
    """
    TR_ID: C29048
    NAME: Bet Receipt for Multiple Bets Which has Handicap Values Available
    DESCRIPTION: This test case verifies Bet Receipt information for Multiple Bets if all or some selections which form multiple bet have handicap values available
    DESCRIPTION: **Jira tickets:** ** BMA-5049, **BMA-5275 (Add Each Way to bet receipt)
    DESCRIPTION: *   BMA-12164 (Bet History/My Bets - Display Unit Stake)
    DESCRIPTION: *   BMA-14421 (Add/Improve Each Way (E/W) notification on betslip receipt)
    DESCRIPTION: * BMA-11096 User is not left on the same page after clicking Done button on slide out Betlsip
    PRECONDITIONS: 1.  Make sure user is logged into their account
    PRECONDITIONS: 2.  The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 3.  Odds format is Fractional
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_any_sport(self):
        """
        DESCRIPTION: Open any <Sport>
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_003_add_several_selections_from_different_events_to_the_betslipmake_sure_selections_have_handicap_values_available(self):
        """
        DESCRIPTION: Add several selections from different events to the Betslip
        DESCRIPTION: Make sure selections have handicap values available
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_004_open_betslip__multiplessection(self):
        """
        DESCRIPTION: Open Betslip-> 'Multiples' section
        EXPECTED: Multiples are available for added selections
        """
        pass

    def test_005_enter_stakes_in_stake_field_for_all_available_multiples(self):
        """
        DESCRIPTION: Enter stakes in 'Stake' field for all available Multiples
        EXPECTED: 
        """
        pass

    def test_006_remember_stakes_total_stake_and_estimated_returns_and_total_est_returns_values(self):
        """
        DESCRIPTION: Remember Stakes, Total Stake and Estimated Returns and Total Est. Returns values
        EXPECTED: 
        """
        pass

    def test_007_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' button
        EXPECTED: 1.  Bet is placed successfully
        EXPECTED: 2.  User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: 3.  Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_008_verify_header(self):
        """
        DESCRIPTION: Verify header
        EXPECTED: 1. 'Bet Receipt' header is present
        EXPECTED: 2. Section header is 'Multiples (#)' with the total number of placed Multiple bets
        EXPECTED: i.e "Double (2)"
        """
        pass

    def test_009_verify_multiples_information(self):
        """
        DESCRIPTION: Verify Multiples information
        EXPECTED: Bet Receipt contains information about just placed Multiple bets:
        EXPECTED: Bet Receipt details for each multiple selection:
        EXPECTED: *   Multiple name (#), where # is a number of bets involved in a Multiple
        EXPECTED: *   the selections made by the customer are displayed for each Multiple with their Odds
        EXPECTED: *   the markets types user has bet on - i.e. Win or Each Way
        EXPECTED: *   the events names to which the outcomes belong too
        EXPECTED: *   the Bet ID i.e. "O/0123828/0000155"
        EXPECTED: *   Unit Stake and 'E/W' label (if 'Each Way' option was selected)
        EXPECTED: *   Free Bet Stake (if Free bet was selected)
        EXPECTED: *   Total Stake = Stake + Free Bet Stake
        EXPECTED: *   Est. Returns
        EXPECTED: Total Bet Receipt details:
        EXPECTED: *   Free Bet Stake  (if Free bet was selected)
        EXPECTED: *   Total Stake = Stake + Free Bet Stake
        EXPECTED: *   Total Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: All information corresponds to the information about just placed bet
        """
        pass

    def test_010_verify_the_handicap_value(self):
        """
        DESCRIPTION: Verify the handicap value
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_011_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed directly to the right of the outcome names
        EXPECTED: Handicap value is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_012_verify_handicap_value_sign(self):
        """
        DESCRIPTION: Verify handicap value sign
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_013_go_to_settings_switch_odds_format_to_decimal_and_go_back_to_bet_receipt_page(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format to Decimal and go back to Bet Receipt page
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_3_7(self):
        """
        DESCRIPTION: Repeat steps 3-7
        EXPECTED: Odds are shown in Decimal format on the Bet Receipt
        """
        pass

    def test_015_verify_total_stake_and_total_est_returns_fields(self):
        """
        DESCRIPTION: Verify 'Total Stake' and 'Total Est. Returns' fields
        EXPECTED: 'Total Stake' and 'Total Est. Returns' fields are displayed and correspond to the values on the Betslip
        """
        pass

    def test_016_tap_reuse_selection_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Reuse Selection' button on Bet Receipt page
        EXPECTED: User is returned to the Betslip to initiate bet placement again on the same selections
        """
        pass

    def test_017_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: * Bet Slip Slider closes
        EXPECTED: * User stays on same page
        """
        pass
