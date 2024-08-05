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
class Test_C15392955_Verify_Signposting_Promotions_on_Cash_out_tab_when_more_than_two_Promos_are_available(Common):
    """
    TR_ID: C15392955
    NAME: Verify Signposting Promotions on Cash-out tab when more than two Promos are available
    DESCRIPTION: My Bets Signposting
    PRECONDITIONS: In OB(back office) signposting( promo) flags are configured.
    PRECONDITIONS: Configuration steps for  Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Admin
    PRECONDITIONS: Expand Betting set up from LHs-->Enter a valid event ID and click Search
    PRECONDITIONS: In the event display page select Market
    PRECONDITIONS: In the Market display page scroll down to see Flags section
    PRECONDITIONS: Select desired flags (Extra place, Odds Boost, Money back, etc)
    PRECONDITIONS: Click on Update Market button.
    PRECONDITIONS: In Cms PromoSignPosting should be enabled.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User has placed Singles and Multiple bets where Cash Out Offer and Signposting Promos is available.
    """
    keep_browser_open = True

    def test_001_1navigate_my_bets___go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate My Bets--> Go to Cash out tab
        EXPECTED: Cash out tab should be opened
        """
        pass

    def test_002_2verify_promosoffers_on_cashout_tab(self):
        """
        DESCRIPTION: 2.Verify promos(offers) on Cashout tab
        EXPECTED: The SignPosting promos are:
        EXPECTED: Odds Boost - should be displayed above the overall bet.
        EXPECTED: Money Back - should be displayed above the overall bet.
        EXPECTED: Extra Place - should be displayed under the selection .
        EXPECTED: Note:If multiple signposting Promos are available for bet then maximum 2 promos displayed on Cash out tab.In Ladbrokes bet boosted speedo meter is displayed.In Coral bet boosted flash is displayed.
        EXPECTED: ![](index.php?/attachments/get/33480)
        EXPECTED: ![](index.php?/attachments/get/33481)
        """
        pass
