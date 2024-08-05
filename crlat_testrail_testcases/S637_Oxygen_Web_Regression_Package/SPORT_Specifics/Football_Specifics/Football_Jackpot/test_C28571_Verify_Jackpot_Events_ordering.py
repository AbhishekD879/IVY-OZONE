import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28571_Verify_Jackpot_Events_ordering(Common):
    """
    TR_ID: C28571
    NAME: Verify Jackpot Events ordering
    DESCRIPTION: This test case verifies ordering of events within displayed Football Jackpot
    DESCRIPTION: AUTOTEST [C9698637]
    PRECONDITIONS: 1) To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?translationLang=LL&simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To view all events being used within the Football Jackpot please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForMarket/YYY?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   YYY - comma separated list of 15 market id's of Football Jackpot pool
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Make sure there is at least one active pool available to be displayed on front-end
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

    def test_004_verify_events_ordering(self):
        """
        DESCRIPTION: Verify Events ordering
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **startTime **- chronological order in the first instance
        EXPECTED: 2.  **Class displayOrder**
        EXPECTED: 3.  **Type displayOrder**
        EXPECTED: 4.  **Event displayOrder**
        EXPECTED: 5.  **Alphabetical order**
        """
        pass
