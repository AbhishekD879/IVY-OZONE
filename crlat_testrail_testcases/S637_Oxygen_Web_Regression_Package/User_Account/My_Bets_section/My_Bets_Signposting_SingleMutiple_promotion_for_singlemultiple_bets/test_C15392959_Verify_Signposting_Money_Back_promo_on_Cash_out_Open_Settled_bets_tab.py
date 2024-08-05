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
class Test_C15392959_Verify_Signposting_Money_Back_promo_on_Cash_out_Open_Settled_bets_tab(Common):
    """
    TR_ID: C15392959
    NAME: Verify Signposting Money Back promo on Cash out/Open/Settled bets tab
    DESCRIPTION: 
    PRECONDITIONS: In OB(back office) signposting Money Back promo flag is configured.
    PRECONDITIONS: Configuration steps for Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Admin
    PRECONDITIONS: Expand Betting set up from LHs-->Enter a valid event ID and click Search
    PRECONDITIONS: In the event display page select Market
    PRECONDITIONS: In the Market display page scroll down to see Flags section
    PRECONDITIONS: Select Money Back promo(tick the check box)
    PRECONDITIONS: Click on Update Market button.
    PRECONDITIONS: Money Back Promo signposting is enabled in cms
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User has placed Single/ Multiple bets where Cash Out offer and Money Back Promo is available on market level.
    PRECONDITIONS: User have some open/settled bets
    """
    keep_browser_open = True

    def test_001_1navigate_to_my_bets___go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets--> Go to Cash out tab
        EXPECTED: Cash out tab should be opened
        """
        pass

    def test_002_2verify_signposting_money_back_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting Money Back Promo
        EXPECTED: The Signpost Money Back promo should be displayed in Cash out section below and above the overall  bet.![](index.php?/attachments/get/33493)
        EXPECTED: ![](index.php?/attachments/get/33494)
        EXPECTED: ![](index.php?/attachments/get/33495)
        """
        pass

    def test_003_3navigate_to_my_bets__go_to_open_bet_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Go to Open bet tab
        EXPECTED: Open bets tab should be Opened.
        """
        pass

    def test_004_4verify_signposting_money_back_promo(self):
        """
        DESCRIPTION: 4.Verify Signposting Money Back promo
        EXPECTED: The Signpost Money Back promo should be displayed in Open bet section below and above of the overall the bet .![](index.php?/attachments/get/33496)
        EXPECTED: ![](index.php?/attachments/get/33497)
        """
        pass

    def test_005_5navigate_to_my_bets__go_to_settled_bets_tab(self):
        """
        DESCRIPTION: 5.Navigate to My Bets-->Go to Settled bets tab
        EXPECTED: Settled bets tab should be opened.
        """
        pass

    def test_006_6verify_signposting_money_back_promo(self):
        """
        DESCRIPTION: 6.Verify Signposting Money Back promo
        EXPECTED: The Signpost Money Back promo should be displayed in Settled bets section (Sport)below and above the overall the bet.![](index.php?/attachments/get/33498)
        EXPECTED: ![](index.php?/attachments/get/33499)
        """
        pass
