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
class Test_C15392960_Verify_Signposting_Extra_Place_promo_on_Cash_out_Open_Settled_bets_tab(Common):
    """
    TR_ID: C15392960
    NAME: Verify Signposting Extra Place promo on Cash out/Open/Settled bets tab
    DESCRIPTION: 
    PRECONDITIONS: In OB(back office) signposting Extra Place promo flag is configured.
    PRECONDITIONS: Configuration steps for Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Admin
    PRECONDITIONS: Expand Betting set up from LHs-->Enter a valid event ID and click Search
    PRECONDITIONS: In the event display page select Market
    PRECONDITIONS: In the Market display page scroll down to see Flags section
    PRECONDITIONS: Select Extra Place Promo(tick the check box)
    PRECONDITIONS: Click on Update Market button.
    PRECONDITIONS: In Cms PromoSignPosting should be enabled.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User placed Single/ Multiple bets where Cash Out offer and Extra Place Promo is available on Market level.
    PRECONDITIONS: User have some open/settled bets.
    """
    keep_browser_open = True

    def test_001_1navigate_to_my_bets__go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets-->Go to Cash out tab
        EXPECTED: Cash out tab should be opened
        """
        pass

    def test_002_2verify_signposting_extra_place_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting 'Extra Place' Promo
        EXPECTED: The Signpost Extra Place promo should be displayed in Cash out section below the Market/Event name.
        EXPECTED: ![](index.php?/attachments/get/33475)
        EXPECTED: ![](index.php?/attachments/get/33476)
        """
        pass

    def test_003_3navigate_to_my_bets__go_to_open_bets_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Go to Open bets tab
        EXPECTED: Open bets tab should be Opened.
        EXPECTED: ![](index.php?/attachments/get/33477)
        EXPECTED: ![](index.php?/attachments/get/33478)
        """
        pass

    def test_004_4verify_signposting_extra_place_promo(self):
        """
        DESCRIPTION: 4.Verify Signposting Extra Place promo
        EXPECTED: The Signpost Extra Place promo should be displayed in Open bets section below the Market/Event name.
        """
        pass

    def test_005_5navigate_to_my_bets___go_to_settled_bet_tab(self):
        """
        DESCRIPTION: 5.Navigate to My Bets--> Go to Settled bet tab
        EXPECTED: Settled bets tab should be opened
        """
        pass

    def test_006_6verify_signposting_extra_place_promo(self):
        """
        DESCRIPTION: 6.Verify Signposting Extra Place Promo
        EXPECTED: The Signpost Extra Place promo should be displayed in Settled bets section below , below the Market/Event name.
        EXPECTED: ![](index.php?/attachments/get/33471)
        EXPECTED: ![](index.php?/attachments/get/33472)
        """
        pass
