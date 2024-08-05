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
class Test_C59928279_Verify_selection_isnt_automatically_boosted_in_Quickbet_Betslip_after_placing_boosted_bet_from_Betslip(Common):
    """
    TR_ID: C59928279
    NAME: Verify selection isn't automatically boosted in Quickbet/Betslip after placing boosted bet from Betslip
    DESCRIPTION: This test case verifies selection in Quick Bet isn't boosted after placing boosted bet from Betslip
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has several Odds Boost tokens added (https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token)
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_quick_bet_skip_for_desktop(self):
        """
        DESCRIPTION: Add one selection to Quick Bet (skip for Desktop)
        EXPECTED: Selection is added to Quick Bet
        EXPECTED: Boost button is displayed unselected
        """
        pass

    def test_002_add_selection_from_quick_bet_to_betslip(self):
        """
        DESCRIPTION: Add selection from Quick Bet to Betslip
        EXPECTED: Selection is added to betslip
        EXPECTED: Boost button is displayed unselected
        """
        pass

    def test_003_click_boost_button_enter_stake_into_stake_field_and_place_bet(self):
        """
        DESCRIPTION: Click Boost button, enter stake into stake field and place bet
        EXPECTED: Slection is boosted after clicking  Boost sutton, new odds displayed
        EXPECTED: Bet is placed and Bet receipt displayed with boosted odds.
        """
        pass

    def test_004_mobile_close_bet_receipt_by_clicking_x_button_at_the_betslip_headerthen_add_same_or_different_selection_to_quick_betdesktop_dont_close_bet_receipt_add_same_or_other_selection_to_betslip(self):
        """
        DESCRIPTION: (Mobile): Close Bet Receipt by clicking 'X' button at the Betslip header
        DESCRIPTION: Then add same or different selection to Quick Bet
        DESCRIPTION: (Desktop): Don't Close Bet Receipt. Add same or other selection to betslip
        EXPECTED: Mobile: Selection is added to Quick Bet. Boost button is displayed unselected, odds are NOT boosted.
        EXPECTED: Desktop: Selection is added to Betslip. Boost button is displayed unselected, odds are NOT boosted
        """
        pass
