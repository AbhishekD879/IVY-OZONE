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
class Test_C9770773_Archived_from_102_Coral_and_Ladbrokes_Transition_of_events_from_Preplay_to_In_Play(Common):
    """
    TR_ID: C9770773
    NAME: [Archived from 102 Coral and Ladbrokes]  Transition of events from Preplay to In-Play
    DESCRIPTION: This test case verifies transition of events from 'Upcoming' module to 'Live now' module when upcoming event becomes live.
    DESCRIPTION: **It will be archived from 102 Coral and Ladbrokes**
    PRECONDITIONS: User is on tier 3 Sport Landing page
    PRECONDITIONS: Outright events are available for this sport
    PRECONDITIONS: Upcoming events are available for the this sport (Attribute 'isNext24HourEvent="true"' is present
    PRECONDITIONS: At least one market contains attribute 'isMarketBetInRun="true"'
    PRECONDITIONS: At least one market is not resulted (there is no attribute 'isResulted="true")
    PRECONDITIONS: Testing on tst2 endpoint refer to TI (http://backoffice-tst2.coral.co.uk/ti) with credentials available on https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: To trigger event goes live in TI set the real time to event and set 'is off - yes' parameter
    """
    keep_browser_open = True

    def test_001_on_sport_landing_page_scroll_to_upcoming_section(self):
        """
        DESCRIPTION: On Sport landing page scroll to 'Upcoming' section
        EXPECTED: Upcoming events are available for this sport
        """
        pass

    def test_002_trigger_the_upcoming_event_goes_live_in_ti(self):
        """
        DESCRIPTION: Trigger the upcoming event goes live (in TI)
        EXPECTED: - Event disappears from 'Upcoming' section and appears in 'Live now' section in real time
        EXPECTED: - Counters of 'Live now'/'Upcoming ' sections are updated accordingly
        """
        pass

    def test_003_find_the_outright_market_section_on_sport_landing_page(self):
        """
        DESCRIPTION: Find the 'Outright market' section on sport landing page
        EXPECTED: Events are available in this section
        """
        pass

    def test_004_trigger_outright_event_goes_live_observe_outright_section(self):
        """
        DESCRIPTION: Trigger outright event goes live, observe Outright section
        EXPECTED: When outright event starts it does not disappear from Outright section
        """
        pass
