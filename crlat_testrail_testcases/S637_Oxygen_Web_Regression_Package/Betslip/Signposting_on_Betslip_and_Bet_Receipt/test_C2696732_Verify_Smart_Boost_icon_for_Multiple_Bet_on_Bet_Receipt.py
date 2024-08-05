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
class Test_C2696732_Verify_Smart_Boost_icon_for_Multiple_Bet_on_Bet_Receipt(Common):
    """
    TR_ID: C2696732
    NAME: Verify Smart Boost icon for Multiple Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the Smart Boost icon is displayed for Multiple Bet on the Bet Receipt within BetSlip
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-33500]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Smart Boost promo is available for event on Market level
    PRECONDITIONS: * Smart Boost promo is available for Specials
    """
    keep_browser_open = True

    def test_001_add_few_selections_with_and_without_smart_boost_promo_available_to_betslip(self):
        """
        DESCRIPTION: Add few selections with and without Smart Boost promo available to betslip
        EXPECTED: Selection are added
        """
        pass

    def test_002_enter_value_in_stake_field_for_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for Multiple bet and place a bet
        EXPECTED: * Multiple bet is placed
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_003_verify_smart_boost_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Smart Boost' icon on the Bet Receipt
        EXPECTED: * 'Smart Boost' icon is displayed under each selection (under market name/event name section) which has this promo available
        EXPECTED: * If there are some other signposting icons they go in one line one by one (eg. 'Cashout' icon coming first).
        """
        pass

    def test_004_add_few_selections_with_smart_boost_promo_available_to_betslip_and_place_multiple_bet(self):
        """
        DESCRIPTION: Add few selections with Smart Boost promo available to betslip and place multiple bet
        EXPECTED: 'Smart Boost' icon is displayed under each selection
        """
        pass

    def test_005_add_few_selections_without_smart_boost_promo_available_to_betslip_and_place_multiple_bet(self):
        """
        DESCRIPTION: Add few selections without Smart Boost promo available to betslip and place multiple bet
        EXPECTED: No 'Smart Boost' icon is displayed in receipt.
        """
        pass
