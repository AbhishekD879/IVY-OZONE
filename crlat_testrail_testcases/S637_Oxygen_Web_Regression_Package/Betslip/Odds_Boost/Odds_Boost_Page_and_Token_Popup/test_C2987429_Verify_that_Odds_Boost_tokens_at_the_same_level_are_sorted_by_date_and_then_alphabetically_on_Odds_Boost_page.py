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
class Test_C2987429_Verify_that_Odds_Boost_tokens_at_the_same_level_are_sorted_by_date_and_then_alphabetically_on_Odds_Boost_page(Common):
    """
    TR_ID: C2987429
    NAME: Verify that Odds Boost tokens at the same level are sorted by date and then alphabetically on Odds Boost page
    DESCRIPTION: This test case verifies that Odds Boost tokens at the same level are sorted by date and then alphabetically on Odds Boost page
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Redemption Values, Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Create Redemption Values in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: For Example:
    PRECONDITIONS: ValueA1 = Class1 (e.g. Football England);
    PRECONDITIONS: ValueB1 = Class2 (e.g Football Spain);
    PRECONDITIONS: ValueC1 = Class3 (e.g Football Australia);
    PRECONDITIONS: CREATE 6 (Six) Odds Boost tokens with different names with Bet type = ANY
    PRECONDITIONS: ADD created Odds Boost tokens to USER1
    PRECONDITIONS: ![](index.php?/attachments/get/7078854)
    PRECONDITIONS: Without Redemption Value:
    PRECONDITIONS: - Token1 where Expiration Date = Today+1 at 12:01;
    PRECONDITIONS: - Token2 where Expiration Date = Today+1 at 12:00;
    PRECONDITIONS: - Token3 where Expiration Date = Today+1 at 12:00;
    PRECONDITIONS: With Redemption Value:
    PRECONDITIONS: - Token4 use Value1, where Expiration Date = Today+1 at 12:01;
    PRECONDITIONS: - Token5 use Value2, where Expiration Date = Today+1 at 12:00;
    PRECONDITIONS: - Token6 use Value3, where Expiration Date = Today+1 at 12:00;
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_navigate_to_odds_boost_pageverify_that_tokens_are_sorted_by_the_category_and_then1_token_at_the_lowest_hierarchy_level2_earliest_expiry_date3_earliest_alphabetical_letter_of_the_first_word_in_the_token_title(self):
        """
        DESCRIPTION: Navigate to Odds Boost Page
        DESCRIPTION: Verify that tokens are sorted by the category and then:
        DESCRIPTION: 1. token at the lowest hierarchy level
        DESCRIPTION: 2. earliest expiry date
        DESCRIPTION: 3. earliest alphabetical letter of the first word in the token title
        EXPECTED: Tokens are shown in the appropriate order:
        EXPECTED: Without category:
        EXPECTED: - Token2
        EXPECTED: - Token3
        EXPECTED: - Token1
        EXPECTED: Football category:
        EXPECTED: - Token5
        EXPECTED: - Token6
        EXPECTED: - Token4
        """
        pass
