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
class Test_C15392957_Verify_Signposting_Promotions_on_Settled_bets_tab_when_more_than_two_Promos_are_available(Common):
    """
    TR_ID: C15392957
    NAME: Verify Signposting Promotions on Settled bets tab when more than two Promos are available
    DESCRIPTION: MyBets Signposting
    PRECONDITIONS: In OB(back office) signposting( promo) flags are configured.
    PRECONDITIONS: Configuration steps for Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Admin
    PRECONDITIONS: Expand Betting set up from LHs-->Enter a valid event ID and click Search
    PRECONDITIONS: In the event display page select Market
    PRECONDITIONS: In the Market display page scroll down to see Flags section
    PRECONDITIONS: Select desired flags (Extra place, Odds Boost, Money back, etc)
    PRECONDITIONS: Click on Update Market button.
    PRECONDITIONS: In Cms PromoSignPosting should be enabled.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User has placed Single/Multiple bets where Signposting Promos are available.
    PRECONDITIONS: User have should have Settled bets.
    """
    keep_browser_open = True

    def test_001_1navigate_to_my_bets____go_to_settled_bets_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets --> Go to Settled bets tab
        EXPECTED: Settled bet tab should be opened.
        """
        pass

    def test_002_2verify_signposting_promos(self):
        """
        DESCRIPTION: 2.Verify Signposting Promos
        EXPECTED: The SignPosting promos are:
        EXPECTED: Odds Boost -  should be displayed above the overall bet.
        EXPECTED: Money Back -  should be displayed above the overall bet.
        EXPECTED: Extra Place - should be displayed under the selection.
        EXPECTED: Note:If number of Signposting Promos available for the bet ,then maximum 2 promos displayed on Settled bet tab.In Ladbrokes bet boosted speedo meter is displayed.In Coral bet boosted flash is displayed.
        EXPECTED: ![](index.php?/attachments/get/33488)
        EXPECTED: ![](index.php?/attachments/get/33489)
        """
        pass
