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
class Test_C29043_Multiple_Information_Description(Common):
    """
    TR_ID: C29043
    NAME: Multiple Information Description
    DESCRIPTION: This test case verifies Informational Description of Multiple Types on the Betslip
    DESCRIPTION: This test case is applied for **Mobile** and **Tablet** application.
    PRECONDITIONS: *Note:*
    PRECONDITIONS: In order to check the potential payout value for multiple bets please go to Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: * For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: * For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    PRECONDITIONS: 1. Add several selections from different events to the Betlsip
    """
    keep_browser_open = True

    def test_001_go_to_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to Betslip->'Multiples' section
        EXPECTED: 
        """
        pass

    def test_002_verify_information_description_for_multiple_types(self):
        """
        DESCRIPTION: Verify Information description for Multiple Types
        EXPECTED: 
        """
        pass

    def test_003_click_i_icon_for_double_multiple_type(self):
        """
        DESCRIPTION: Click 'i' icon for Double Multiple Type
        EXPECTED: Popup with description appears:
        EXPECTED: "A Double consists of one bet involving two selections from different events. Both selections must be successful for your bet to win."
        """
        pass

    def test_004_treble(self):
        """
        DESCRIPTION: Treble
        EXPECTED: A Treble consists of one bet involving three selections from different events. All three must be successful for your bet to win.
        """
        pass

    def test_005_trixie(self):
        """
        DESCRIPTION: Trixie
        EXPECTED: A Trixie consists of four bets involving three selections from different events: 3 doubles and 1 treble. A minimum of 2 of your selections must be successful to get a return.
        """
        pass

    def test_006_patent(self):
        """
        DESCRIPTION: Patent
        EXPECTED: A Patent consists of 7 bets involving 3 selections from different events: 3 singles, 3 doubles and 1 treble. You need one successful selection to guarantee a return.
        """
        pass

    def test_007_single_stakes_about_3(self):
        """
        DESCRIPTION: Single Stakes About 3
        EXPECTED: Single Stakes About 3
        """
        pass

    def test_008_accumulator(self):
        """
        DESCRIPTION: Accumulator
        EXPECTED: An Accumulator is one bet with four or more selections from different events. All selections must be successful for your bet to win.
        """
        pass

    def test_009_yankee(self):
        """
        DESCRIPTION: Yankee
        EXPECTED: A Yankee consists of 11 bets involving 4 selections from different events:
        EXPECTED: 6 doubles, 4 trebles and 1 fourfold accumulator.
        """
        pass

    def test_010_lucky_15(self):
        """
        DESCRIPTION: Lucky 15
        EXPECTED: A Lucky 15 consists of 15 bets involving 4 selections in different events:
        EXPECTED: 4 singles 6 doubles 4 trebles 1 accumulator You need only 1 winner to guarantee a return. In the event of 1 winner and 3 losers, the odds for the winner are doubled. For 4 winners out of 4 a bonus of 10% is added.
        EXPECTED: Please note: the above bonuses and concessions apply only to bets on horseracing, greyhounds or a combination of both. Any accepted bet that includes a selection from a different sport will not qualify for any bonus or concession
        """
        pass

    def test_011_canadian(self):
        """
        DESCRIPTION: Canadian
        EXPECTED: A Super Yankee (or Canadian) consists of 26 bets involving 5 selections from different events:
        EXPECTED: 10 doubles, 10 trebles, 5 four-fold accumulators and 1 five-fold accumulator.
        EXPECTED: You need a minimum of 2 of your selections to win to get a return
        """
        pass

    def test_012_lucky_31(self):
        """
        DESCRIPTION: Lucky 31
        EXPECTED: A Lucky 31 consists of 31 bets involving 5 selections in different events:
        EXPECTED: 5 singles 10 doubles 10 trebles 5 four-fold accumulators 1 five-fold accumulator You need only 1 winner to guarantee a return. In the event of 1 winner and 4 losers, the odds for the winner are doubled. For 5 winners out of 5 a bonus of 20% is added.
        EXPECTED: Please note: the above bonuses and concessions apply only to bets on horseracing, greyhounds or a combination of both. Any accepted bet that includes a selection from a different sport will not qualify for any bonus or concession.
        """
        pass

    def test_013_heinz(self):
        """
        DESCRIPTION: Heinz
        EXPECTED: A Heinz consists of 57 bets involving 6 selections from different events:
        EXPECTED: 15 doubles, 20 trebles, 15 four-fold accumulators, 6 five-fold accumulator and 1 six-fold accumulator
        EXPECTED: A minimum of 2 of your selections must be successful to get a return.
        """
        pass

    def test_014_lucky_63(self):
        """
        DESCRIPTION: Lucky 63
        EXPECTED: A Lucky 63 consists of 63 bets involving 6 selections in different events:
        EXPECTED: 6 singles 15 doubles 20 trebles 15 four-fold accumulators 6 five-fold accumulators 1 six-fold accumulator
        EXPECTED: You need only 1 winner to guarantee a return. In the event of 1 winner and 5 losers, the odds for the winner are doubled. For 5 winners out of 6 a bonus of 10% is added. For 6 winners out of 6 a bonus of 25% is added.
        EXPECTED: Please note: the above bonuses and concessions apply only to bets on horseracing, greyhounds or a combination of both. Any accepted bet that includes a selection from a different sport will not qualify for any bonus or concession.
        """
        pass

    def test_015_super_heinz(self):
        """
        DESCRIPTION: Super Heinz
        EXPECTED: A Super Heinz consists of 120 bets involving 7 selections from different events:
        EXPECTED: 21 doubles, 35 trebles, 35 four-fold accumulators, 21 five -fold accumulators 7 six-fold accumulators and 1 seven-fold accumulator
        EXPECTED: A minimum of 2 of your selections must be successful to get a return.
        """
        pass

    def test_016_goliath(self):
        """
        DESCRIPTION: Goliath
        EXPECTED: A Goliath consists of 247 bets involving 8 selections from different events:
        EXPECTED: 28 doubles, 56 trebles, 70 four-fold accumulators, 56 five-fold accumulators, 28 six-fold accumulators, 8 seven-fold accumulators and 1 eight-fold accumulator.
        EXPECTED: You need a minimum of 2 of your selections to be successful to get a return.
        """
        pass

    def test_017_verify_other_available_multiple_types(self):
        """
        DESCRIPTION: Verify other available Multiple Types
        EXPECTED: Popup with the following text appears:
        EXPECTED: "N bets"
        EXPECTED: where N - number of bets involved in Multiple
        """
        pass
