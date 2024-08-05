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
class Test_C2987413_Verify_hierarchy_sorting_of_Odds_Boost_tokens_with_ANY_Bet_Type_on_Odds_Boost_page(Common):
    """
    TR_ID: C2987413
    NAME: Verify hierarchy sorting of Odds Boost tokens with ANY Bet Type on Odds Boost page
    DESCRIPTION: This test case verifies that Odds Boost tokens are sorted on Odds Boost page according to the hierarchy after it is sorted by category
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Redemption Values, Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Create Redemption Values in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: For Example:
    PRECONDITIONS: Value1 = Category1 (e.g Football);
    PRECONDITIONS: Value2 = Class1 (e.g. Football England);
    PRECONDITIONS: Value3 = Type1 (e.g. Premier League);
    PRECONDITIONS: Value4 = Event1 (e.g. Brighton vs Chelsea);
    PRECONDITIONS: Value5= Market1 (e.g. Match Result);
    PRECONDITIONS: Value6 = Selection1 (e.g. Draw)
    PRECONDITIONS: CREATE 6 (Six) Odds Boost tokens with different names with Bet type = ANY
    PRECONDITIONS: ADD created Odds Boost tokens to USER1 selecting the appropriate Redemption Value
    PRECONDITIONS: ![](index.php?/attachments/get/7078854)
    PRECONDITIONS: **Token1** use Value1 (Token for Category);
    PRECONDITIONS: **Token2** use Value2 (Token for Class)
    PRECONDITIONS: **Token3** use Value3 (Token for Type);
    PRECONDITIONS: **Token4** use Value 4 (Token for Event);
    PRECONDITIONS: **Token5** use Value5 (Token for Market);
    PRECONDITIONS: **Token6** use Value6 (Token for Selection);
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_navigate_to_odds_boost_pageverify_that_tokens_are_sorted_under_the_category_by_hierarchy_token_at_the_lowest_hierarchy_level_is_first(self):
        """
        DESCRIPTION: Navigate to Odds Boost Page
        DESCRIPTION: Verify that tokens are sorted under the category by hierarchy (token at the lowest hierarchy level is first)
        EXPECTED: Tokens are sorted under the Football category:
        EXPECTED: - Token6
        EXPECTED: - Token5
        EXPECTED: - Token4
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass
