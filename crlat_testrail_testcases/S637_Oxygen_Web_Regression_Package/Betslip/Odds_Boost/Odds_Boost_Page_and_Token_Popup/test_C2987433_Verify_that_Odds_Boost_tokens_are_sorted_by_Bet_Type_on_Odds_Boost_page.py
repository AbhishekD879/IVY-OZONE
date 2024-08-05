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
class Test_C2987433_Verify_that_Odds_Boost_tokens_are_sorted_by_Bet_Type_on_Odds_Boost_page(Common):
    """
    TR_ID: C2987433
    NAME: Verify that Odds Boost tokens are sorted by Bet Type on Odds Boost page
    DESCRIPTION: This test case verifies that Odds Boost tokens are sorted by Bet Type on Odds Boost page. The highest bet type should be first
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Use instructions:
    PRECONDITIONS: How to create Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: CREATE Odds Boost tokens with different names with different Bet Type
    PRECONDITIONS: Token1 - Bet Type = ANY
    PRECONDITIONS: Token2 - Bet Type = DOUBLE
    PRECONDITIONS: Token3 - Bet Type = TREBLE
    PRECONDITIONS: Token4 - Bet Type = ACCA4
    PRECONDITIONS: ADD just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_navigate_to_odds_boost_pageverify_that_tokens_are_sorted_by_the_bet_type(self):
        """
        DESCRIPTION: Navigate to Odds Boost Page
        DESCRIPTION: Verify that tokens are sorted by the Bet Type
        EXPECTED: Tokens are shown in the appropriate order:
        EXPECTED: - Token4
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass
