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
class Test_C884421_Verify_Double_Your_Winnings_Promo_Icon_on_Football_market_level(Common):
    """
    TR_ID: C884421
    NAME: Verify "Double Your Winnings" Promo Icon on Football market level
    DESCRIPTION: This test case verifies "Double Your Winnings" Promo Icon on Football event details page.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-34455 Promo/Signposting: Pop-up: Customer no longer sees pop-ups appear as a Footer Banner] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-34455
    PRECONDITIONS: * There has to be a Football event with "Double Your Winnings" promotion available.
    PRECONDITIONS: * **NOTE:** Promotions are not available for **Combined Markets** during phase 1 of Signposting Promotions
    PRECONDITIONS: Make sure that there are promotion created in CMS and linked to active signposting promotions (Market Flags)
    PRECONDITIONS: **NOTE:** Information about promotions, available for the event, is received in <drilldownTagNames> attribute in SiteServer response for the event
    PRECONDITIONS: Parameters:
    PRECONDITIONS: * **MKTFLAG_DYW** - Double Your Winnings
    PRECONDITIONS: Link to response on TST2 endpoints:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_an_event_with_double_your_winnings_promotion_available_and_check_the_accordion_of_the_market_for_which_the_promotion_is_available(self):
        """
        DESCRIPTION: Open event details page of an event with **Double Your Winnings** promotion available and check the accordion of the Market, for which the promotion is available
        EXPECTED: * Event details page is opened
        EXPECTED: * The promo icon is displayed on corresponding Market accordion
        """
        pass

    def test_002_tap_on_the_double_your_winnings_icon(self):
        """
        DESCRIPTION: Tap on the 'Double Your Winnings' icon
        EXPECTED: Promo pop-up is displayed after tapping the icon
        """
        pass

    def test_003_verify_that_in_case_there_are_both_cashout_and_promo_icon_displayed_for_a_market_at_the_same_time(self):
        """
        DESCRIPTION: Verify that in case there are both cashout and promo icon displayed for a market at the same time
        EXPECTED: 'Double Your Winnings' icon is displayed after CashOut icon on Market accordion (Cashout icon is ALWAYS displayed at the left side of the other icons)
        """
        pass
