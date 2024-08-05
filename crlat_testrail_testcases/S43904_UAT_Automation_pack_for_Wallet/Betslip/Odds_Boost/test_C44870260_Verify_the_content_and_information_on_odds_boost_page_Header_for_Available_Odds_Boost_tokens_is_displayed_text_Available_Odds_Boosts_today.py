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
class Test_C44870260_Verify_the_content_and_information_on_odds_boost_page_Header_for_Available_Odds_Boost_tokens_is_displayed_text_Available_Odds_Boosts_today(Common):
    """
    TR_ID: C44870260
    NAME: "Verify the content and information on odds boost page -Header for Available Odds Boost tokens is displayed, text: 'Available Odds Boost(s) today'
    DESCRIPTION: Place a bet on using Odds boost token and verify the count has been decreased after placing the bet.
    PRECONDITIONS: Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Odds Boost' item is enabled in Right menu in CMS
    PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
    """
    keep_browser_open = True

    def test_001_navigate_to_my_accounts__offers__free_bets__odds_boost(self):
        """
        DESCRIPTION: Navigate to 'My accounts' > Offers & Free bets > Odds boost
        EXPECTED: My account' (User menu) menu is expanded > Offer & Free bets
        EXPECTED: Odds Boost item is available in the menu
        EXPECTED: Summary value 1 of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        pass

    def test_002_place_a_bet_with_available_information_page_odds_boost_token(self):
        """
        DESCRIPTION: Place a bet with available information page Odds boost token
        EXPECTED: Bet is placed
        EXPECTED: Odds Boost token is used
        EXPECTED: number of Odds boost will be decreased as user had placed another bet.
        """
        pass
