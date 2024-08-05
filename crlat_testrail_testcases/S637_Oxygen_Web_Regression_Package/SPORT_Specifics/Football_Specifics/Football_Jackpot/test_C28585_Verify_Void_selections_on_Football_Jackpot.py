import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28585_Verify_Void_selections_on_Football_Jackpot(Common):
    """
    TR_ID: C28585
    NAME: Verify 'Void' selections on Football Jackpot
    DESCRIPTION: This test case verifies 'Void' selections on Football Jackpot page
    PRECONDITIONS: 1) To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: 2) To view all events being used within the Football Jackpot please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForMarket/YYY&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   YYY - comma separated list of 15 market id's of Football Jackpot pool
    PRECONDITIONS: 3) Make sure there is at least one active pool available to be displayed on front-end
    PRECONDITIONS: **NOTE: Changes (buttons' graying out) are available on PAGE REFRESH only**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: Football Jackpot Page is opened
        """
        pass

    def test_004_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED: 
        """
        pass

    def test_005_go_to_event_section_with_suspendedvoid_outcome_outcomestatuscodes(self):
        """
        DESCRIPTION: Go to event section with suspended/void outcome (outcomeStatusCode="S")
        EXPECTED: Outcome is disabled with label 'Unavailable' above it
        """
        pass

    def test_006_go_to_event_section_with_suspendedvoid_market_marketstatuscodes(self):
        """
        DESCRIPTION: Go to event section with suspended/void market (marketStatusCode="S")
        EXPECTED: *   Whole Event section is disabled
        EXPECTED: *   'This market is no longer available' text is shown
        EXPECTED: *   Number of events displayed in page header is decreased by number of events with unavailable markets
        """
        pass

    def test_007_go_to_event_section_of_suspendedvoid_event_eventstatuscodes(self):
        """
        DESCRIPTION: Go to event section of suspended/void event (eventStatusCode="S")
        EXPECTED: *   Whole Event section is disabled
        EXPECTED: *   'This event is no longer available' text is shown
        EXPECTED: *   Number of events displayed in page header is decreased by number of unavailable events
        """
        pass
