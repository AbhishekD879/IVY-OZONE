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
class Test_C9770772_Transition_of_upcoming_event_to_In_Play_module_within_Matches_tab(Common):
    """
    TR_ID: C9770772
    NAME: Transition of upcoming event to In-Play module within Matches tab
    DESCRIPTION: This test case verifies transition of event from League(s) section with upcoming events to 'Live now' module when upcoming event becomes live.
    PRECONDITIONS: 1) Following Tabs should be enabled in Sports Pages - SPORT CATEGORIES - #TIER_2_SPORT_NAME within CMS: Matches, Competitions, Outrights
    PRECONDITIONS: 2) Following Modules should be enabled in Sports Pages - SPORT CATEGORIES - #TIER_2_SPORT_NAME within CMS:In play module, Featured events
    PRECONDITIONS: 3) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value = 'Current Date_Current Time' + 10M
    PRECONDITIONS: Aforementioned event should have:
    PRECONDITIONS: 4) a Primary Market being set with 'Bet-in-running' active status ('isMarketBetInRun="true")
    PRECONDITIONS: 5) its Primary Market not resulted (there is no attribute 'isResulted="true")
    PRECONDITIONS: 6) 'Bet in Playlist' Flag being checked(set) in TI
    PRECONDITIONS: 7) 'is off' parameter set to 'NO' in TI
    PRECONDITIONS: 8) User is on Tier 2 Sport Landing page of the chosen Sport
    PRECONDITIONS: 9) 'Matches' tab is opened by default
    PRECONDITIONS: To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Testing on tst2 endpoint refer to TI (http://backoffice-tst2.coral.co.uk/ti) with credentials available on https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_navigate_to_eventcreated_in_pre_conditions_in_leagues_section_with_upcoming_events(self):
        """
        DESCRIPTION: Navigate to event(created in pre-conditions) in League(s) section with upcoming events
        EXPECTED: Event is displayed in 'Today' list of events within the League
        """
        pass

    def test_002_wait_till_the_start_time_value_of_eventfrom_pre_conditions_becomes_current_date_current_time_and_change_is_off_parameter_for_the_event_to_yes(self):
        """
        DESCRIPTION: Wait till the 'Start Time' value of event(from pre-conditions) becomes 'Current Date_Current Time' and change 'is off' parameter for the event to: 'YES'
        EXPECTED: Event remains in the League(s) section with upcoming events
        EXPECTED: Web response in XHR contains a Push request regarding changes within the event: is_off: "Y"
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: - Event disappears from League(s) section with upcoming events and appears in the 'In-Play' module, under the 'League' list of events
        EXPECTED: - Counter shown in 'SEE ALL (#)' link is updated accordingly
        """
        pass
