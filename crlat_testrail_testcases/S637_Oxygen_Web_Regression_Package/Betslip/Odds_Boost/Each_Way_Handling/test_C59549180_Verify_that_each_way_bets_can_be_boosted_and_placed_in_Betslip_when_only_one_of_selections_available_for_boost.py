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
class Test_C59549180_Verify_that_each_way_bets_can_be_boosted_and_placed_in_Betslip_when_only_one_of_selections_available_for_boost(Common):
    """
    TR_ID: C59549180
    NAME: Verify that each way bets can be boosted and placed in Betslip when only one of selections available for boost
    DESCRIPTION: This test case verifies that each way bet can be boosted and placed in Betslip for Multiple selection when only not all selections are appropriate for boost token
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens and Redemption Values use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 1) CREATE Adhoc Odds Boost token in Backoffice
    PRECONDITIONS: 2) CREATE Redemption Value in Backoffice for available racing event
    PRECONDITIONS: 3) ADD created odds boost token with created Redemption Value to user
    PRECONDITIONS: 4) Login with user to related environment
    PRECONDITIONS: 5) Make sure that user doesn't have any other Odds Boost available (so that added token would be used)
    """
    keep_browser_open = True

    def test_001_add_one_selection_from_horse_racinggreyhounds_with_lp_available_to_betslip_which_is_not_the_one_mentioned_in_redemption_value(self):
        """
        DESCRIPTION: Add one selection from Horse Racing/Greyhounds (with LP available) to Betslip which is NOT the one mentioned in Redemption Value
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Boost is not available for this selection
        """
        pass

    def test_002_add_one_more_selection_from_horse_racinggreyhounds_ew_market_with_lp_available_to_betslip_which_is_the_one_mentioned_in_redemption_value(self):
        """
        DESCRIPTION: Add one more selection from Horse Racing/Greyhounds (E/W market with LP available) to Betslip which is the ONE mentioned in Redemption Value
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Both selections are present in Betslip
        EXPECTED: * Boost button is available in Betslip
        """
        pass

    def test_003_presstap_on_boost_button(self):
        """
        DESCRIPTION: Press/Tap on 'Boost' button
        EXPECTED: * 'Boost' button is changed to 'Boosted'
        EXPECTED: * Selection mentioned in Redemption Value has boosted price displayed
        EXPECTED: * Selection NOT mentioned in Redemption Value has tooltip about N/A boost for it
        EXPECTED: * Double bet has boosted price displayed
        """
        pass

    def test_004_add_any_stake_and_tick_each_way_checkbox_for_selections_and_double_option(self):
        """
        DESCRIPTION: Add any stake and tick 'Each Way' checkbox for selections and Double option
        EXPECTED: * Selection mentioned in Redemption Value has boosted price displayed and Potential Returns re-calculated
        EXPECTED: * Selection NOT mentioned in Redemption Value has tooltip about N/A boost for it and regular Potential Returns calculated
        EXPECTED: * Double bet has boosted price displayed and Potential Returns shown as *N/A*
        """
        pass

    def test_005_presstap_on_place_bet_button(self):
        """
        DESCRIPTION: Press/tap on 'Place bet' button
        EXPECTED: Bet receipt is shown with appropriate elements for for boosted SINGLE bet:
        EXPECTED: * Odds boost title
        EXPECTED: * Boosted odds
        EXPECTED: * 2 Lines at (Amount) per line
        EXPECTED: Bet receipt is shown with appropriate elements for for boosted DOUBLE bet:
        EXPECTED: * Odds boost title
        EXPECTED: * 2Lines at (Amount) per line
        EXPECTED: * Potential returns calculated
        """
        pass

    def test_006_repeat_steps_1_5_when_first_selection_added_to_betslip_is_the_one_mentioned_in_redemption_value_and_available_for_boost_second_selection_added_to_betslip_is_from_horse_racinggreyhounds_with_lp_available_and_is_not_the_one_mentioned_in_redemption_value(self):
        """
        DESCRIPTION: Repeat steps 1-5, when:
        DESCRIPTION: * first selection added to Betslip is the ONE mentioned in Redemption Value and available for boost
        DESCRIPTION: * second selection added to Betslip is from Horse Racing/Greyhounds (with LP available) and is NOT the one mentioned in Redemption Value
        EXPECTED: Results are the same
        """
        pass
