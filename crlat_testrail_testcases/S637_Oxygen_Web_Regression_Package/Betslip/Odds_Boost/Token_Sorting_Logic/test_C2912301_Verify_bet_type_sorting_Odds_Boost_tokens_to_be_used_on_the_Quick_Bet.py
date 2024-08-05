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
class Test_C2912301_Verify_bet_type_sorting_Odds_Boost_tokens_to_be_used_on_the_Quick_Bet(Common):
    """
    TR_ID: C2912301
    NAME: Verify bet type sorting Odds Boost tokens to be used on the Quick Bet
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the Bet Type to be used in the Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create THREE Odds Boost tokens with different Bet type using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Token1**: Bet Type = ANY (where expiration date = Tomorrow 12:01)
    PRECONDITIONS: **Token2**: Bet Type = SINGLE (where expiration date = Tomorrow 12:00)
    PRECONDITIONS: **Token3**: Bet Type = DOUBLE
    PRECONDITIONS: Add this tokens for User1 in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Adhoc Tokens)
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betverify_that_boost_button_is_shown(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Verify that 'BOOST' button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_add_stake_tap_boost_button_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap Place Bet button
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown
        """
        pass

    def test_003_navigate_to_odds_boost_pageverify_that_token2_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token2** is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token3
        """
        pass

    def test_004_add_selection_to_quick_betverify_that_boost_button_is_shown(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Verify that 'BOOST' button is shown
        EXPECTED: BOOST button is shown
        """
        pass

    def test_005_add_stake_and_tap_boost_buttontap_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and tap 'BOOST' button
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown
        """
        pass

    def test_006_navigate_to_odds_boost_pageverify_that_token1_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token1** is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token3
        """
        pass

    def test_007_add_selection_to_quick_betverify_that_boost_button_is_not_shown(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Verify that BOOST button is NOT shown
        EXPECTED: 'BOOST' button is NOT shown
        """
        pass
