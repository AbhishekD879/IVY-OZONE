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
class Test_C2594382_REMOVED_not_valid_Verify_YourCall_Promo_Icon(Common):
    """
    TR_ID: C2594382
    NAME: [REMOVED-not valid] Verify "#YourCall" Promo Icon
    DESCRIPTION: This test case verifies adding and displaying new promotion
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: [BMA-35277 Expose new #YC icon when Flag: 'YourCall Selections Available' is selected in Openbet (Event Level)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-35277
    PRECONDITIONS: **Link to TST2 TI** (where is configurable promotions on event/market levels):
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/xxxxxxx
    PRECONDITIONS: WHERE:
    PRECONDITIONS: xxxxxxx - OpenBet event ID
    PRECONDITIONS: **Link to response on TST2 endpoints:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE:
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    PRECONDITIONS: The variable is containing promotion flags for the event: <drilldownTagNames>
    PRECONDITIONS: Market-level flag for **#YourCall** - YOUR_CALL (YourCall is not configurable in OpenBet TI on market lvl)
    PRECONDITIONS: Event-level flag - **#YourCall** - EVFLAG_YC
    PRECONDITIONS: **Preconditions**
    PRECONDITIONS: * 'Your Call Selections Available' flag is **NOT** enabled in Openbet TI on event level for some Sport event
    PRECONDITIONS: * User navigated to the current Sport landing page -> Matches tab
    PRECONDITIONS: * Current event is present
    """
    keep_browser_open = True

    def test_001_check_presen_of_yourcall_icon_on_leagues_accordions_sport_landing_page___matches_tab_(self):
        """
        DESCRIPTION: Check presenсе of #YourCall icon on Leagues accordions (Sport landing page -> Matches tab )
        EXPECTED: * #YourCall icon is **NOT** present on Leagues accordions (Sport landing page -> Matches tab)
        """
        pass

    def test_002_check_if_yourcall_icon_is_not_present_on_homepage___featured_tab_on_leagues_accordions_homepage___byb_tab_on_leagues_accordions_sport_landing_page___matches_tab_on_leagues_accordions_sport_landing_page___competitions_tab_on_leagues_headers_sport_landing_page___coupons_page_on_leagues_headers(self):
        """
        DESCRIPTION: Check if #YourCall icon is NOT present on:
        DESCRIPTION: * Homepage -> Featured tab (on Leagues accordions)
        DESCRIPTION: * Homepage -> BYB tab (on Leagues accordions)
        DESCRIPTION: * Sport landing page -> Matches tab (on Leagues accordions)
        DESCRIPTION: * Sport landing page -> Competitions tab (on Leagues headers)
        DESCRIPTION: * Sport landing page -> Coupons page (on Leagues headers)
        EXPECTED: * #YourCall icon is **NOT** present on listed places
        """
        pass

    def test_003_enable_your_call_selections_available_flag_in_openbet_ti_on_event_level_for_same_sport_event(self):
        """
        DESCRIPTION: Enable 'Your Call Selections Available' flag in Openbet TI on event level for same Sport event
        EXPECTED: 'Your Call Selections Available' flag is enabled in Openbet TI on event level for same Sport event
        """
        pass

    def test_004_check_presence_of_yourcall_icon_on_leagues_accordions_sport_landing_page___matches_tab(self):
        """
        DESCRIPTION: Check presence of #YourCall icon on Leagues accordions (Sport landing page -> Matches tab)
        EXPECTED: * #YourCall icon is present on Leagues accordions (Sport landing page -> Matches tab)
        EXPECTED: * #YourCall icon is placed on the right side of accordions
        EXPECTED: * #YourCall icon is placed before CashOut icon (if available)
        """
        pass

    def test_005_check_if_yourcall_icon_is_present_on_homepage___featured_tab_on_leagues_accordions_homepage___byb_tab_on_leagues_accordions_sport_landing_page___matches_tab_on_leagues_accordions_sport_landing_page___competitions_tab_on_leagues_headers_sport_landing_page___coupons_page_on_leagues_headers(self):
        """
        DESCRIPTION: Check if #YourCall icon is present on:
        DESCRIPTION: * Homepage -> Featured tab (on Leagues accordions)
        DESCRIPTION: * Homepage -> BYB tab (on Leagues accordions)
        DESCRIPTION: * Sport landing page -> Matches tab (on Leagues accordions)
        DESCRIPTION: * Sport landing page -> Competitions tab (on Leagues headers)
        DESCRIPTION: * Sport landing page -> Coupons page (on Leagues headers)
        EXPECTED: * #YourCall icon is present on listed places
        """
        pass
