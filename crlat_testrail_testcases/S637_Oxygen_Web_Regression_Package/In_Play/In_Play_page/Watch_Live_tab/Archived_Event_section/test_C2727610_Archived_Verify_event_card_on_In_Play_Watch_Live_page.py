import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C2727610_Archived_Verify_event_card_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727610
    NAME: [Archived] Verify event card on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies event card on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load Oxygen application
    PRECONDITIONS: 3. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_choose_live_now_switcher(self):
        """
        DESCRIPTION: Choose 'Live Now' switcher
        EXPECTED: The list of live events is displayed on the page
        """
        pass

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in format:
        EXPECTED: &lt;Team1/Player1&gt; and &lt;Team2/Player2&gt; below
        EXPECTED: *   Name of outright/race event is displayed in format: '&lt;Name&gt; 'LIVE' label'
        """
        pass

    def test_003_verify_match_timesetslive_labelevent_start_time(self):
        """
        DESCRIPTION: Verify 'Match Time'/'Sets'/'Live' label/'Event Start Time'
        EXPECTED: *   'Event start time' corresponds to 'startTime' attribute
        EXPECTED: *   For events that occur **Today** date format is: **24 hours, Today**
        EXPECTED: *   For events that occur **Tomorrow** date format is: **24 hours, DD-MMM**
        EXPECTED: *   For events that occur in the **Future** (including tomorrow) date format is: **24 hours, DD-MMM**
        EXPECTED: *   Event **'Match Time'/'Sets'/'Live' label** is shown if available instead of event Start Time
        EXPECTED: *   **'Match Time'/'Sets'/'Live' label/'Event Start Time'** is displayed below the Event name for Coral and Under Event name for Ladbrokes.
        """
        pass

    def test_004_verify_watch_live_icon_and_inscription(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and inscription
        EXPECTED: * 'Watch live' icon and inscription (inscription and 'Watch Live' icon **for Desktop**) are shown if ‘drilldownTagNames’ attribute is available (one or more of following flags):
        EXPECTED: - EVFLAG_AVA
        EXPECTED: - EVFLAG_IVM
        EXPECTED: - EVFLAG_PVM
        EXPECTED: - EVFLAG_RVA
        EXPECTED: - EVFLAG_RPM
        EXPECTED: - EVFLAG_GVM
        EXPECTED: * 'Watch live' icon and inscription are displayed next to 'Match Time'/'Sets'/'Live' label/'Event Start Time'
        """
        pass

    def test_005_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        pass

    def test_006_choose_upcoming_switcher(self):
        """
        DESCRIPTION: Choose 'Upcoming' switcher
        EXPECTED: The list of pre-match events is displayed on the page
        """
        pass

    def test_007_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in the next format:
        EXPECTED: &lt;Team1/Player1&gt;
        EXPECTED: &lt;Team2/Player2&gt;
        EXPECTED: *   Name of outright/race event is displayed in format: '&lt;Name&gt;'
        """
        pass

    def test_008_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        pass
