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
class Test_C1474616_Verify_Specials_tab__Specials_module(Common):
    """
    TR_ID: C1474616
    NAME: Verify Specials tab - Specials module
    DESCRIPTION: This test case verifies Special tab and its content for a Big Competition
    PRECONDITIONS: CMS configs:
    PRECONDITIONS: - 'Specials' tab is created
    PRECONDITIONS: - 'Specials' module with 'Specials' type is created within Specials tab
    PRECONDITIONS: - 'Special' module contains TypeIDs of: e.g. World Cup Specials, Yourcall Specials, Enhanced Multiples Specials
    PRECONDITIONS: OB TI configs:
    PRECONDITIONS: - Events are created in backoffice: http://backoffice-tst2.coral.co.uk/ti:
    PRECONDITIONS: Category (e.g. Football) >
    PRECONDITIONS: **Class** (e.g. Football Specials) >
    PRECONDITIONS: **Type** (e.g. World Cup Specials; Yourcall Specials; Enhanced Multiples Specials) >
    PRECONDITIONS: **Event** (e.g. England Specials; YourCall World Cup Semi Finalist Special; Enhanced Multiples Special event)>
    PRECONDITIONS: **Market** (e.g. Team Specials; YourCall Special; Enhanced Multiples) >
    PRECONDITIONS: **Outcome(s)** (e.g. Harry Kane to score in all three World Cup group matches; Brazil, Germany, France, Spain to be the semi finalists at the world cup 2018; Albania and Finland and Bulgaria all to win )
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded
        """
        pass

    def test_002_go_to_big_competition_eg_world_cup_page(self):
        """
        DESCRIPTION: Go to Big Competition (e.g. World Cup) page
        EXPECTED: Big Competition (e.g. World Cup) page is opened
        """
        pass

    def test_003_verify_specials_tab(self):
        """
        DESCRIPTION: Verify Specials tab
        EXPECTED: * Specials tab is available and displayed after 'Featured' and 'Groups'
        EXPECTED: * 'Specials' tab is NOT selected by default
        EXPECTED: * 'No events found' text is shown for 'Specials' tab, if no events are loaded for 'Specials' tab > 'Specials' module in CMS, or 'Specials' module is not created within 'Specials' tab
        """
        pass

    def test_004_tap_on_specials_tab__verify_content_on_specials_tab(self):
        """
        DESCRIPTION: Tap on 'Specials' tab > Verify content on 'Specials' tab
        EXPECTED: * 'Specials' tab is opened
        EXPECTED: * TypeID accordions are available with corresponding event(s) (e.g. World Cup Specials type) or selection(s) (e.g. Yourcall Specials, Enhanced Multiples Specials types)
        EXPECTED: * First TypeID accordion is expanded, the rest ones are collapsed
        EXPECTED: * All accordions are expandable/collapsible
        EXPECTED: * Order of accordions is based on "typeDisplayOrder" from SS response
        EXPECTED: * 10 events or selections are shown within one TypeID accordion, if events are 10 > 'Show More' link is displayed
        EXPECTED: * Tapping on 'Show More' link, all available events or selection(s) within TypeID accordion are displayed, the link becomes 'Show Less' and vice versa
        """
        pass

    def test_005_verify_typeid_accordion_with_the_list_of_events_egworld_cup_specials(self):
        """
        DESCRIPTION: Verify TypeID accordion with the list of events (e.g.World Cup Specials)
        EXPECTED: * Events are displayed within 'TypeID' accordion (e.g. World Cup Specials)
        EXPECTED: * Order of events is based on event "startTime" from SS response (closest first)
        EXPECTED: * If events "startTime" is equal events are shown alphabetically in asc order
        """
        pass

    def test_006_tap_on_any_event_within_typeid_accordion_egworld_cup_specials(self):
        """
        DESCRIPTION: Tap on any event within TypeID accordion (e.g.World Cup Specials)
        EXPECTED: Corresponding event details page is opened
        """
        pass

    def test_007_place_a_bet(self):
        """
        DESCRIPTION: Place a bet
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_008_go_back_to_big_competition_eg_world_cup__specials_tab__verify_typeid_accordion_with_the_list_of_selections_that_have_event_details_page_eg_yourcall_specials(self):
        """
        DESCRIPTION: Go back to Big Competition (e.g. World Cup) > Specials tab > Verify TypeID accordion with the list of selections that have Event Details Page (e.g. YourCall Specials)
        EXPECTED: * Events are displayed within 'TypeID' accordion (e.g. YourCall Specials)
        EXPECTED: * Order of selections is based on corresponding events "startTime" from SS response (closest first)
        EXPECTED: * If events "startTime" is equal events are shown alphabetically in asc order
        """
        pass

    def test_009_tap_on_any_event_within_typeid_accordion_eg_yourcall_specials(self):
        """
        DESCRIPTION: Tap on any event within TypeID accordion (e.g. YourCall Specials)
        EXPECTED: Corresponding event details page is opened
        """
        pass

    def test_010_place_a_bet(self):
        """
        DESCRIPTION: Place a bet
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_011_go_back_to_big_competition_eg_world_cup__specials_tab____verify_typeid_accordion_with_the_list_of_selections_that_do_not_have_event_details_page_eg_enhanced_multiples_specials(self):
        """
        DESCRIPTION: Go back to Big Competition (e.g. World Cup) > Specials tab >   Verify TypeID accordion with the list of selections that do NOT have Event Details Page (e.g. Enhanced Multiples Specials)
        EXPECTED: * Outcomes are grouped by Start Date, that is shown above an Outcome name for a group of outcomes (NOTE: applies only for Enhanced Multiples)
        EXPECTED: * Outcome Start Time is shown below Outcome name (NOTE: applies only for Enhanced Multiples)
        EXPECTED: * Order of selections is based on corresponding events "startTime" from SS response (closest first)
        EXPECTED: * If events "startTime" is equal events are shown alphabetically in asc order
        """
        pass

    def test_012_place_a_bet(self):
        """
        DESCRIPTION: Place a bet
        EXPECTED: Bet is successfully placed
        """
        pass
