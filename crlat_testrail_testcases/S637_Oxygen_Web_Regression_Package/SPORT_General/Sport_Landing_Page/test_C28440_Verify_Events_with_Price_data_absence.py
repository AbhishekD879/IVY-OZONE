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
class Test_C28440_Verify_Events_with_Price_data_absence(Common):
    """
    TR_ID: C28440
    NAME: Verify Events with Price data absence
    DESCRIPTION: This test case verifies that events without Price data are absent on <Sport> Landing Pages.
    PRECONDITIONS: 1. In order to retrieve the list of all **Classes **and **Types **use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XX Category ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. In order to retrieve all **Events** outcomes for the **Classes **use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *   XXXX is a comma separated list of **Class ID's**
    PRECONDITIONS: *   YYYY1-MM1-DD1 is lower time bound
    PRECONDITIONS: *   YYYY2-MM2-DD2 is higher time bound
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XX - Sport Category ID
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. There are events without Price data
    """
    keep_browser_open = True

    def test_001_retrieve_the_list_of_events_for_verified_tab_use_time_intervalspecial_events_identifier(self):
        """
        DESCRIPTION: Retrieve the list of events for verified tab (use time interval/special event's identifier)
        EXPECTED: List of events are returned from siteserver
        """
        pass

    def test_002_find_event_withoutpricenumpricedenpricedec_in_outcome_section(self):
        """
        DESCRIPTION: Find event without priceNum/priceDen/priceDec in outcome section
        EXPECTED: 
        """
        pass

    def test_003_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_004_tap_sport_icon_on_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is selected by default
        """
        pass

    def test_005_go_to_verified_tabin_play_matches_matcheseventsracesfightstournaments__coupons_outrights(self):
        """
        DESCRIPTION: Go to verified tab:
        DESCRIPTION: 'In-Play', <Matches> ('Matches'/'Events'/'Races'/'Fights'/'Tournaments'),  'Coupons', 'Outrights'
        EXPECTED: *   The tab is shown
        EXPECTED: *   Navigation is carried out smoothly
        """
        pass

    def test_006_check_list_of_events_on_event_landing_page_when_leaguescompetitions_sorting_type_is_selected(self):
        """
        DESCRIPTION: Check list of events on Event Landing Page when 'Leagues&Competitions' sorting type is selected
        EXPECTED: All events have Price/Odds buttons
        """
        pass

    def test_007_check_list_of_events_on_event_landing_page_when_by_time_sorting_type_is_selected(self):
        """
        DESCRIPTION: Check list of events on Event Landing Page when 'By Time' sorting type is selected
        EXPECTED: All events have Price/Odds buttons
        """
        pass

    def test_008_try_to_find_event_from_step_2(self):
        """
        DESCRIPTION: Try to find event from step №2
        EXPECTED: Event is not shown on the <Sport> Landing Page
        """
        pass
