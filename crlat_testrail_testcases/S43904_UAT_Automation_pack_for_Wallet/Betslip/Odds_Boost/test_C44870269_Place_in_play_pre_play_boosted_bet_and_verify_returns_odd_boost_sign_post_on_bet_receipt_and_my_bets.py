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
class Test_C44870269_Place_in_play_pre_play_boosted_bet_and_verify_returns_odd_boost_sign_post_on_bet_receipt_and_my_bets(Common):
    """
    TR_ID: C44870269
    NAME: Place in play , pre play boosted bet and verify returns, odd boost sign post on bet receipt and my bets.
    DESCRIPTION: 
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_odds_boost_token_page(self):
        """
        DESCRIPTION: Navigate to the Odds Boost token page
        EXPECTED: User is navigated to the OB token page
        EXPECTED: The tokens are displayed
        EXPECTED: Tokens are segmented by available now & upcoming
        """
        pass

    def test_002_verify_that_tokens_for_any_event_are_displayed_at_the_top_of_appropriate_available_now__upcoming_segments(self):
        """
        DESCRIPTION: Verify that tokens for ANY event are displayed at the top of appropriate available now & upcoming segments
        EXPECTED: Available now boosts tokens with ANY category are displayed at the top of 'available now' segment
        EXPECTED: Upcoming boosts tokens with ANY category are displayed at the top of 'upcoming' segment
        """
        pass

    def test_003_place_in_playpre_play_boosted_bet_and_verify_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Place in-play/Pre play boosted bet and verify bet receipt and my bets
        EXPECTED: odds are boosted and signposting is displayed in the bet receipt.
        """
        pass
