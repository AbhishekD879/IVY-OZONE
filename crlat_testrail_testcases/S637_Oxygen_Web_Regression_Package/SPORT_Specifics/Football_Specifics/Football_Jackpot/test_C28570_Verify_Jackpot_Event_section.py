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
class Test_C28570_Verify_Jackpot_Event_section(Common):
    """
    TR_ID: C28570
    NAME: Verify Jackpot Event section
    DESCRIPTION: This test case verifies Event section of active Football Jackpot
    DESCRIPTION: AUTOTEST [C9647698]
    PRECONDITIONS: 1) To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive&translationLang=LL
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

    def test_004_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED: 
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: Event name corresponds to '**name**' attribute of event
        """
        pass

    def test_006_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event start time
        EXPECTED: *   Event start time corresponds to '**startTime**' attribute of event
        EXPECTED: *   Event start time is shown in** ****"<name of the day>, DD-****MMM-YY. 12 hours AM/PM"** format
        """
        pass

    def test_007_verify_event_selection_buttons_outcomes(self):
        """
        DESCRIPTION: Verify Event selection buttons (outcomes)
        EXPECTED: *   Each event has 3 buttons that are shown in one row next to the Event name and start time
        EXPECTED: *   Buttons are named and ordered in the following way: **'Home'**/**'Draw'**/**'Away', **where
        EXPECTED: 'Home' - home team win (outcomeMeaningMinorCode="H")
        EXPECTED: 'Draw' - draw (outcomeMeaningMinorCode="D")
        EXPECTED: 'Away' - away team win (outcomeMeaningMinorCode="A")
        """
        pass
