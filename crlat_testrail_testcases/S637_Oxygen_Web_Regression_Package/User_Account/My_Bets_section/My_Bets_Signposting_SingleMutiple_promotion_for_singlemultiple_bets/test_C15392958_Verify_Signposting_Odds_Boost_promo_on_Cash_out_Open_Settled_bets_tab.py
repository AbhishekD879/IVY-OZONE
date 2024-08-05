import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C15392958_Verify_Signposting_Odds_Boost_promo_on_Cash_out_Open_Settled_bets_tab(Common):
    """
    TR_ID: C15392958
    NAME: Verify  Signposting Odds Boost promo on Cash out/Open/Settled bets tab
    DESCRIPTION: 
    PRECONDITIONS: In OB(back office) signposting->Odds Boost promo flag is configured.
    PRECONDITIONS: Configuration steps for Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Campaign Manager
    PRECONDITIONS: Expand Offers set up from LHs
    PRECONDITIONS: Create Odds Boosts offer
    PRECONDITIONS: In Cms PromoSignPosting should be enabled.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User has placed Single /Multiple bets where Cash Out offer and Odds Boost is available in My Bets Section.
    PRECONDITIONS: User have some open and settled bets.
    """
    keep_browser_open = True

    def test_001_1navigate_to_my_bets___go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets--> Go to Cash out tab
        EXPECTED: Cash out tab should be opened
        """
        pass

    def test_002_2verify_signposting_odds_boost_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting Odds boost Promo
        EXPECTED: The Signpost Odds Boost should be displayed above the overall bet
        EXPECTED: ![](index.php?/attachments/get/33461)
        EXPECTED: ![](index.php?/attachments/get/33463)
        """
        pass

    def test_003_3navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Open bets tab
        EXPECTED: Open bets tab should be Opened
        """
        pass

    def test_004_4verify_signposting_odds_boost_promo(self):
        """
        DESCRIPTION: 4.Verify Signposting Odds Boost promo
        EXPECTED: The Signpost Odds Boost promo should be displayed  above the overall bet
        EXPECTED: ![](index.php?/attachments/get/33469)
        EXPECTED: ![](index.php?/attachments/get/33470)
        """
        pass

    def test_005_5navigate_to_my_bets___go_to_settled_bets_tab(self):
        """
        DESCRIPTION: 5.Navigate to My Bets--> Go to Settled bets tab
        EXPECTED: Settled bets tab should be opened
        """
        pass

    def test_006_6verify_signposting_odds_boost_promo(self):
        """
        DESCRIPTION: 6.Verify Signposting Odds Boost promo
        EXPECTED: The Signpost odds Boost promo should be displayed  above the overall the bet .
        EXPECTED: ![](index.php?/attachments/get/33473)
        EXPECTED: ![](index.php?/attachments/get/33474)
        """
        pass
