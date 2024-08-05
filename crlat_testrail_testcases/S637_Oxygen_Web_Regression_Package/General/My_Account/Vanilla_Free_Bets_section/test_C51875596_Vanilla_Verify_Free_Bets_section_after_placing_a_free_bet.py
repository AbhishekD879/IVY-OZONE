import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C51875596_Vanilla_Verify_Free_Bets_section_after_placing_a_free_bet(Common):
    """
    TR_ID: C51875596
    NAME: [Vanilla] Verify Free Bets section after placing a free bet
    DESCRIPTION: This test case verifies updating list of Free Bets on the Sports Free Bets page: Amount, balance & disappearing from Free Bets list
    PRECONDITIONS: - User has FreeBet(s) available with next 'Single/Multiple Redemption Values' on any 'Category'/'Class'/'Type'/'Event'/'Market'/'Selection' Bet Levels
    PRECONDITIONS: - Instruction how to create a 'Redemption Value' & add a Free Bet to a user: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Event (Select Reward Token = 2428)
    """
    keep_browser_open = True

    def test_001_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: Sports Free Bets page is opened
        """
        pass

    def test_002_remember_the_amount_balance__list_of_free_bets(self):
        """
        DESCRIPTION: Remember the Amount, balance & list of 'Free Bets'
        EXPECTED: 
        """
        pass

    def test_003_go_to_any_sport_page_where_free_bets_from_preconditions_apply(self):
        """
        DESCRIPTION: Go to any <Sport> page where 'Free Bets' from preconditions apply
        EXPECTED: Corresponding <Sport> page is opened
        """
        pass

    def test_004___add_selection_to_quick_betbetslip__place_a_bet_using_free_bets(self):
        """
        DESCRIPTION: - Add selection to 'Quick Bet'/'Betslip'
        DESCRIPTION: - Place a bet using 'Free Bets'
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_005_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets__verify_free_bets_amount_and_balance(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        DESCRIPTION: - Verify 'Free Bets' amount and balance
        EXPECTED: Free Bets amount and balance are updated according to available Free Bets
        """
        pass

    def test_006_verify_the_list_of_free_bets(self):
        """
        DESCRIPTION: Verify the list of Free Bets
        EXPECTED: List of Free Bets is updated according to available Free Bets
        """
        pass
