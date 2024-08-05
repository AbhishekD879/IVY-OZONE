import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C62255599_Verify_Free_Bets_section_after_placing_a_bet_with_Bet_Pack_free_bet(Common):
    """
    TR_ID: C62255599
    NAME: Verify Free Bets section after placing a bet with Bet Pack free bet
    DESCRIPTION: This test case verifies display of Free Bets section after placing a bet with Bet Pack free bet
    PRECONDITIONS: 1: User has purchased Bet Pack
    PRECONDITIONS: 2: User has Bet Pack Free Bet(s) available with next 'Single/Multiple Redemption Values' on any 'Category'/'Class'/'Type'/'Event'/'Market'/'Selection'
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

    def test_002_check_the_amount_balance__list_of_bet_packfree_bets(self):
        """
        DESCRIPTION: Check the Amount, balance & list of Bet Pack'Free Bets'
        EXPECTED: 
        """
        pass

    def test_003_go_to_any_sport_page_where_bet_pack_free_bets_from_preconditions_apply(self):
        """
        DESCRIPTION: Go to any <Sport> page where Bet Pack 'Free Bets' from preconditions apply
        EXPECTED: Corresponding <Sport> page is opened
        """
        pass

    def test_004___add_selection_to_quick_betbetslip__place_a_bet_using_bet_pack_free_bets(self):
        """
        DESCRIPTION: - Add selection to 'Quick Bet'/'Betslip'
        DESCRIPTION: - Place a bet using Bet Pack 'Free Bets'
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
        EXPECTED: Free Bets amount and balance are updated according to available Bet Pack Free Bets
        """
        pass

    def test_006_verify_the_list_of_bet_pack_free_bets(self):
        """
        DESCRIPTION: Verify the list of Bet Pack Free Bets
        EXPECTED: List of Bet Pack Free Bets are updated according to available Free Bets
        """
        pass
