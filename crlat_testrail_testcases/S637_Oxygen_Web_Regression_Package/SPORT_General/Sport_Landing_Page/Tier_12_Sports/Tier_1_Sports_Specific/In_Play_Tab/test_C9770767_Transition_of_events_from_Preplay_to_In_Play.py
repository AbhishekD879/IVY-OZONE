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
class Test_C9770767_Transition_of_events_from_Preplay_to_In_Play(Common):
    """
    TR_ID: C9770767
    NAME: Transition of events from Preplay to In-Play
    DESCRIPTION: This test case verifies transition of events from 'Upcoming' module to 'Live now' module when upcoming event becomes live.
    PRECONDITIONS: User is on Sport Landing page
    PRECONDITIONS: Upcoming events are available for the this sport (Attribute 'isNext24HourEvent="true"' is present
    PRECONDITIONS: At least one market contains attribute 'isMarketBetInRun="true"'
    PRECONDITIONS: At least one market is not resulted (there is no attribute 'isResulted="true")
    PRECONDITIONS: Testing on tst2 endpoint refer to TI (http://backoffice-tst2.coral.co.uk/ti) with credentials available on https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: To trigger event goes live in TI set the real time to event and set 'is off - yes' parameter
    """
    keep_browser_open = True

    def test_001_on_sport_landing_page_navigate_to_in_play_tab(self):
        """
        DESCRIPTION: On Sport landing page navigate to In-Play tab
        EXPECTED: In-Play tab content loads with
        EXPECTED: - Live now section
        EXPECTED: - Upcoming section
        """
        pass

    def test_002_scroll_down_to_upcoming_section_trigger_the_event_goes_live_in_ti(self):
        """
        DESCRIPTION: Scroll down to Upcoming section, trigger the event goes live in TI
        EXPECTED: - Event disappears from Upcoming section and appears in Live now section in real time
        EXPECTED: - Counters of 'Live now'/'Upcoming' sections are updated accordingly
        """
        pass

    def test_003_change_market_in_market_selector_football_only_to_any_other_available(self):
        """
        DESCRIPTION: Change market in Market selector (football only) to any other available
        EXPECTED: Available events are displayed
        """
        pass

    def test_004_trigger_event_transition_from_preplay_to_inplay(self):
        """
        DESCRIPTION: Trigger event transition from preplay to inplay
        EXPECTED: - Event disappears from upcoming section and appears in live now
        EXPECTED: - Counters of 'Live now'/'Upcoming' sections are updated accordingly
        """
        pass
