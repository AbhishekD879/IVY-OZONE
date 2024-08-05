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
class Test_C1474022_Verify_Specials_module_within_Featured_Tab(Common):
    """
    TR_ID: C1474022
    NAME: Verify 'Specials' module within Featured Tab
    DESCRIPTION: This test case verifies Specials module section within Featured Tab
    PRECONDITIONS: CMS configs:
    PRECONDITIONS: * 'Featured' tab is created, set up and enabled in CMS  (e.g. 'Big Competitions'-> 'World Cup' -> 'Featured')
    PRECONDITIONS: * 'Featured-Specials' module ("SPECIALS_OVERVIEW" type) is created, set up and enabled in CMS -> 'Specials' tab
    PRECONDITIONS: * Url to 'Specials' tab is set in "Link URL" in 'Featured-Specials' module ("SPECIALS_OVERVIEW" type) > defines availability of "All Specials" link
    PRECONDITIONS: * List of events is predefined in 'Featured-Specials' module
    PRECONDITIONS: OB TI configs:
    PRECONDITIONS: * Events are created in backoffice: http://backoffice-tst2.coral.co.uk/ti:Category (e.g. Football) >
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_big_competition_eg_world_cup_page(self):
        """
        DESCRIPTION: Go to Big Competition (e.g. World Cup) page
        EXPECTED: * Competition page is opened
        EXPECTED: * 'Featured' page is opened
        """
        pass

    def test_003_scroll_down_to_specials_module_section(self):
        """
        DESCRIPTION: Scroll down to 'Specials' module section
        EXPECTED: 'Specials' section is shown as accordion panel (all expended by default):
        EXPECTED: * 'Specials' tab (first panel)
        EXPECTED: *  'Type Name' corresponds to TypeId sub tab (second panel)
        EXPECTED: *  List of events that predefined in CMS
        EXPECTED: *  'All Specials' link
        """
        pass

    def test_004_verify_typeid_accordion_with_the_list_of_events_egworld_cup_specials(self):
        """
        DESCRIPTION: Verify TypeID accordion with the list of events (e.g.World Cup Specials)
        EXPECTED: - Events are displayed within 'TypeID' accordion (e.g. World Cup Specials)
        EXPECTED: - Order of events is based on event "startTime" from SS response (closest first)
        EXPECTED: - If events "startTime" is equal events are shown alphabetically in asc order
        EXPECTED: - Selection (selection is not shown if event has more that one selection)
        """
        pass

    def test_005_verify_typeid_ordering(self):
        """
        DESCRIPTION: Verify TypeID ordering
        EXPECTED: Order of accordions is based on "typeDisplayOrder" from SS response
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

    def test_008_verify_type_id_accordion_for_enhanced_multiple(self):
        """
        DESCRIPTION: Verify Type ID accordion for Enhanced Multiple
        EXPECTED: *  'Enhanced Multiple' Type name sub tab (second panel)
        EXPECTED: * 'Today' section is shown
        EXPECTED: *  List of events that predefined in CMS
        EXPECTED: * Time for each event is shown
        """
        pass

    def test_009_click_on_the_all_specials_linkcms_configurable_see_preconditions(self):
        """
        DESCRIPTION: Click on the 'All Specials' link
        DESCRIPTION: (CMS configurable, see preconditions)
        EXPECTED: User is redirected to the 'World Cup' -> 'Specials' page
        """
        pass
