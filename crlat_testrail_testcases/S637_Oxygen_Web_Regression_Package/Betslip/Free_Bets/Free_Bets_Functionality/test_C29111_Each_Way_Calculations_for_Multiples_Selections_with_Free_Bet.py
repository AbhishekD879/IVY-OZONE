import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29111_Each_Way_Calculations_for_Multiples_Selections_with_Free_Bet(Common):
    """
    TR_ID: C29111
    NAME: Each Way Calculations for Multiples Selections with Free Bet
    DESCRIPTION: This test case verifies each way calculations for Multiple selections when free bet is selected
    PRECONDITIONS: Make sure <RACE> events have each way option available (terms are shown for market)
    PRECONDITIONS: NOTE, for STG environment UAT assistance is needed in order to get free bet tokens available
    PRECONDITIONS: User has to be logged in
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_a_few_lp_selections_from_different_ltracegt_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add a few 'LP' selections from different &lt;Race&gt; events to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_003_go_to_bet_slip_multiples_section(self):
        """
        DESCRIPTION: Go to 'Bet Slip', 'Multiples' section
        EXPECTED: 'Multiples' section is shown
        """
        pass

    def test_004_chose_free_bet_from_the_dropdown_and_select_each_way_option(self):
        """
        DESCRIPTION: Chose free bet from the dropdown and select 'Each way' option
        EXPECTED: *   Free bet is chosen
        EXPECTED: *   'Each way' option is checked
        EXPECTED: *   'Stake' field is empty
        """
        pass

    def test_005_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **free\_bet/(lines*2) * bets[i].payout.potential - free\_bet **
        EXPECTED: *   **bets[i].payout.potential **attribute** **is taken** **from **'builtBet' **responce;
        EXPECTED: *   '**i**' - number of corresponding mutiple bet;
        EXPECTED: *   id = 'symbol of bet type' (e.g. id  = 'DBL' - double, 'TBL' - treble).
        EXPECTED: * lines - number of lines returned in buildBet response
        EXPECTED: * payout.potential = 'potential with legType: "W"' + 'potential with legType: "P"'
        EXPECTED: NOTE: for each multiple bet type there are two identical lines with id. One of them is calculated with 'Each way' option, second - without. Take into consideration line where is id calculated with 'Each way' option
        """
        pass

    def test_006_enter_amount_in_stake_field(self):
        """
        DESCRIPTION: Enter amount in 'Stake' field
        EXPECTED: *   'Stake' field is auto-populated with entered value
        EXPECTED: *   Free bet is chosen
        EXPECTED: *   'Each way' option is checked
        """
        pass

    def test_007_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **(stake + free\_bet/(lines*2)) * bets[i].payout.potential - free\_bet **
        """
        pass

    def test_008_repeat_steps__3___7_for_sp_selections(self):
        """
        DESCRIPTION: Repeat steps # 3 - 7 for 'SP' selections
        EXPECTED: **'Total Est.Returns'** value will always be equal to 'N/A'
        """
        pass
