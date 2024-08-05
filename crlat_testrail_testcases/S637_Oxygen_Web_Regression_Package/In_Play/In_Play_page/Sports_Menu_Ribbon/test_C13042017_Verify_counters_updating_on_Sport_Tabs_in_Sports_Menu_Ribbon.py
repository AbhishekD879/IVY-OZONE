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
class Test_C13042017_Verify_counters_updating_on_Sport_Tabs_in_Sports_Menu_Ribbon(Common):
    """
    TR_ID: C13042017
    NAME: Verify counters updating on Sport Tabs in Sports Menu Ribbon
    DESCRIPTION: This test case verifies counters updating on Sport Tabs in Sports Menu Ribbon
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 1) Load the app
    PRECONDITIONS: 2) Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop)
    PRECONDITIONS: 3) Select any sport
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check value that is displayed in Counter use the following instruction:
    PRECONDITIONS: Dev Tools->Network->WS
    PRECONDITIONS: Open 'INPLAY_SPORTS_RIBBON_CHANGED' response
    PRECONDITIONS: Look at **liveEventCount** attribute for live now events and **upcomingEventCount** attribute for upcoming events
    PRECONDITIONS: **Counters are NOT displayed for Ladbrokes mobile Inplay page. There is "Live" label next to Sport icon instead of counter.**
    """
    keep_browser_open = True

    def test_001_in_ti_undisplayset_results_to_any_inplay_event_for_any_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: In TI undisplay/set results to any inplay event for any sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** attribute in WS
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        """
        pass

    def test_002_trigger_starting_of_inplay_event_for_any_sport(self):
        """
        DESCRIPTION: Trigger starting of inplay event for any sport
        EXPECTED: * Started event appears on front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** attribute in WS
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        """
        pass

    def test_003_step_for_desktopclick_on_upcoming_switcher(self):
        """
        DESCRIPTION: **Step for desktop:**
        DESCRIPTION: Click on 'Upcoming' switcher
        EXPECTED: 
        """
        pass

    def test_004_in_ti_undisplayset_results_to_any_upcoming_event_for_any_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: In TI undisplay/set results to any upcoming event for any sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: **For mobile/tablet:**
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter remains unchanged for respective Sport in Sports Menu Ribbon
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        EXPECTED: **For desktop:**
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **upcomingEventCount** attribute in WS
        """
        pass

    def test_005_trigger_appearing_of_upcoming_event_for_any_sport(self):
        """
        DESCRIPTION: Trigger appearing of upcoming event for any sport
        EXPECTED: **For mobile/tablet:**
        EXPECTED: * Event appears on front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter remains unchanged for respective Sport in Sports Menu Ribbon
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        EXPECTED: **For desktop:**
        EXPECTED: * Event appears on front-end automatically
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **upcomingEventCount** attribute in WS
        """
        pass
