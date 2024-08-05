import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C2696856_Verify_Smart_Boost_icon_for_Single_Bet_on_Quick_Bet(Common):
    """
    TR_ID: C2696856
    NAME: Verify Smart Boost icon for Single Bet on Quick Bet
    DESCRIPTION: This test case verifies that the Smart Boost icon is displayed within Quick Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [Promo / Signposting: QuickBet for SmartBoost]
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-36230
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Smart Boost promo is available for event on Market lvl.
    """
    keep_browser_open = True

    def test_001_add_selection_with_available_smart_boost_promo_on_market_level_to_the_quick_bet(self):
        """
        DESCRIPTION: Add selection with available Smart Boost promo on Market level to the Quick Bet
        EXPECTED: Quick Bet has shown up and Selection is successfully added
        """
        pass

    def test_002_verify_the_smart_boost_icon_for_the_bet_added_to_quick_bet(self):
        """
        DESCRIPTION: Verify the 'Smart Boost' icon for the bet added to Quick Bet
        EXPECTED: Smart Boost icon is displayed below the bet
        EXPECTED: ![](index.php?/attachments/get/53285793)
        EXPECTED: ![](index.php?/attachments/get/53285798)
        """
        pass

    def test_003__enter_value_in_stake_field_and_place_a_bet_verify_smart_boost_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: * Enter value in 'Stake' field and place a bet
        DESCRIPTION: * Verify 'Smart Boost' icon on the Bet Receipt
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        EXPECTED: * 'Smart Boost' icon is displayed below market name/event name section
        EXPECTED: ![](index.php?/attachments/get/53285795)
        EXPECTED: ![](index.php?/attachments/get/53285797)
        """
        pass

    def test_004_add_selection_with_no_promo_available_to_quick_bet_and_check_the_icon(self):
        """
        DESCRIPTION: Add selection with no promo available to Quick Bet and check the icon
        EXPECTED: No icon is displayed for bet without promo available
        """
        pass

    def test_005__enter_value_in_stake_field_and_place_a_bet_verify_smart_boost_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: * Enter value in 'Stake' field and place a bet
        DESCRIPTION: * Verify 'Smart Boost' icon on the Bet Receipt
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        EXPECTED: * 'Smart Boost' icon is NOT displayed
        """
        pass

    def test_006_add_selection_with_smart_boost_and_cashout_promo_available_to_the_quick_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection with Smart Boost and Cashout promo available to the Quick Bet and place a bet
        EXPECTED: * Smart Boost and Cashout icons are displayed for the bet one by one in one line
        EXPECTED: * 'Cashout' icon is placed first, 'Smart Boost' is second one
        EXPECTED: ![](index.php?/attachments/get/53285794)
        EXPECTED: ![](index.php?/attachments/get/53285796)
        """
        pass
