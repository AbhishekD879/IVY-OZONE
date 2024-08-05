import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28859_Verify_Suspended_markets(Common):
    """
    TR_ID: C28859
    NAME: Verify Suspended markets
    DESCRIPTION: This test case verifies <Race> events with suspended market/markets.
    PRECONDITIONS: Make sure there is event with at least one suspended market: **marketStatusCode="S"**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?racingForm=outcome&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   YYYYYY is an event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_taprace_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page_for_event_with_suspended_market(self):
        """
        DESCRIPTION: Go to the event details page for event with suspended market
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_go_to_suspended_market_section(self):
        """
        DESCRIPTION: Go to suspended Market section
        EXPECTED: Market section is shown
        """
        pass

    def test_005_verify_markets_selections(self):
        """
        DESCRIPTION: Verify Market's selections
        EXPECTED: *   All selections of verified market are greyed out
        EXPECTED: *   Selections of verified market are disabled
        EXPECTED: *   For the rest event's markets selections are enabled with prices
        """
        pass
