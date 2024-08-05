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
class Test_C2912302_Verify_bet_type_and_hierarchy_sorting_together_of_Odds_Boost_tokens_to_be_used_in_the_Quick_Bet(Common):
    """
    TR_ID: C2912302
    NAME: Verify bet type and hierarchy sorting together of Odds Boost tokens to be used in the Quick Bet
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the Bet Type and then by hierarchy to be used in the Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create Odds Boost tokens with different Bet type using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Token1a**: Bet Type = ANY (expiration date = Tomorrow at 12:01)
    PRECONDITIONS: **Token1b**: Bet Type = ANY (expiration date = Tomorrow at 12:01)
    PRECONDITIONS: **Token2**: Bet Type = SINGLE (expiration date = Tomorrow at 12:00)
    PRECONDITIONS: **Token3**: Bet Type = DOUBLE
    PRECONDITIONS: Create Redemption Values in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: For Example:
    PRECONDITIONS: **Value1** = Football;
    PRECONDITIONS: **Value2** = Premier League;
    PRECONDITIONS: Add this tokens for USER1 in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Adhoc Tokens)
    PRECONDITIONS: Add **Token1a** (Bet Type=ANY) with Remediation value = Value2
    PRECONDITIONS: Add **Token1b** (Bet Type=ANY) with Remediation value = Value2
    PRECONDITIONS: Add **Token2** (Bet Type=SINGLE) with Remediation value = Value2
    PRECONDITIONS: Add **Token3** (Bet Type=DOUBLE) with Remediation value = Value1
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet_appropriate_to_value2_selection_from_premier_leagueverify_that_odds_boost_button_is_available(self):
        """
        DESCRIPTION: Add selection to Quick Bet appropriate to Value2 (selection from Premier League)
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_receipt_with_boosted_odds_is_shown(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that receipt with boosted odds is shown
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown
        """
        pass

    def test_003_navigate_to_odds_boost_pageverify_that_token_with_earlier_expiration_date_is_usedtoken2_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that token with earlier expiration date is used
        DESCRIPTION: **Token2** is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        EXPECTED: - Token3
        """
        pass

    def test_004_add_selection_one_more_time_to_quick_betverify_that_odds_boost_button_is_available(self):
        """
        DESCRIPTION: Add selection one more time to Quick Bet
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_005_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_receipt_with_boosted_odds_is_shown(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that receipt with boosted odds is shown
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown
        """
        pass

    def test_006_navigate_to_odds_boost_pageverify_that_token_with_alphabetical_priorities_is_usedtoken1a_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that token with alphabetical priorities is used
        DESCRIPTION: **Token1a** is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1b
        EXPECTED: - Token3
        """
        pass

    def test_007_add_selection_from_any_other_category_than_in_value1_eg_tennisverify_that_odds_boost_button_is_available(self):
        """
        DESCRIPTION: Add selection from any other Category than in Value1 (e.g. Tennis)
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is NOT shown
        """
        pass

    def test_008_remove_selection_and_add_selection_from_value2_premier_leagueverify_that_odds_boost_button_is_available(self):
        """
        DESCRIPTION: Remove selection and Add selection from Value2 (Premier League)
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_009_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_receipt_with_boosted_odds_is_shown(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that receipt with boosted odds is shown
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown
        """
        pass

    def test_010_navigate_to_odds_boost_pageverify_that_token_for_any_is_usedtoken1b_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that token for ANY is used
        DESCRIPTION: **Token1b** is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token3
        """
        pass

    def test_011_add_selection_one_more_time_to_quick_betverify_that_odds_boost_button_is_available(self):
        """
        DESCRIPTION: Add selection one more time to Quick Bet
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is NOT shown
        """
        pass
