import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1489742_Verify_Outright_Module(Common):
    """
    TR_ID: C1489742
    NAME: Verify Outright Module
    DESCRIPTION: This test case verifies Outright Module
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * 3 Module with type = 'OUTRIGHTS' and GRID, CARD, LIST views should be created, enabled and set up in CMS
    PRECONDITIONS: * Only one market should be added to each Outrights Modules
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_outright_module(self):
        """
        DESCRIPTION: Go to Outright Module
        EXPECTED: * Outright Module has only one panel if one market is received in **'market'** array in GET tab/sub tab response
        EXPECTED: * Outright Module has Sub Panel(s) if two and more markets are received in **'market'** array in GET tab/sub tab response
        """
        pass

    def test_004_verify_outright_module_panelsub_panel_content_set_up_in_grid_view(self):
        """
        DESCRIPTION: Verify Outright Module Panel/Sub Panel content set up in **Grid** view
        EXPECTED: Outright Module Panel/Sub Panel consists of:
        EXPECTED: * Each-way terms (if available)
        EXPECTED: * Date
        EXPECTED: * Country flag
        EXPECTED: * Selection name
        EXPECTED: * Price/odds button with the associated price
        EXPECTED: * 'Show more' option
        """
        pass

    def test_005_verify_each_way_terms(self):
        """
        DESCRIPTION: Verify Each-way terms
        EXPECTED: * Each-way terms is displayed if **competitionModules.[i].markets.[j].data.markets.[k].isEachWayAvailable=true** from GET tab/sub tab response
        EXPECTED: * Each-way terms are displayed above the list of selection
        EXPECTED: * Each-way terms are displayed in the next format:
        EXPECTED: Each Way: x/y odds - places z,j,k
        EXPECTED: e.g. Each Way: 1/2 odds - places 1,2,3
        """
        pass

    def test_006_verify_date(self):
        """
        DESCRIPTION: Verify date
        EXPECTED: * Date is displayed if Each-way terms are NOT available for particular market
        EXPECTED: * Date is displayed above the list of selection in the next format:
        EXPECTED: DAY, DD-MM-YY, '12' hours AM/PM
        EXPECTED: e.g. SUNDAY, 13-MAY-18, 4:00 PM
        """
        pass

    def test_007_verify_the_number_of_selections_displayed_within_module(self):
        """
        DESCRIPTION: Verify the number of selections displayed within Module
        EXPECTED: Number of selections displayed within Module corresponds to **competitionModules.[i].markets.[j].maxDisplay** attribute from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j - the number of all Markets returned to Module
        """
        pass

    def test_008_verify_country_flag_for_each_selection(self):
        """
        DESCRIPTION: Verify country flag for each selection
        EXPECTED: * Country flag is displayed next to selection name
        EXPECTED: * Country flag is displayed if **competitionModules.[i].markets.[j].outcomes.[k].participants.HOME/AWAY.svgID** field is NOT empty
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j - the number of all Markets returned to Module
        EXPECTED: k - the number of all Outcomes returned to Market
        """
        pass

    def test_009_scroll_down_and_tap_on_show_more_option(self):
        """
        DESCRIPTION: Scroll down and tap on 'Show more' option
        EXPECTED: * All selections within the market are displayed after tapping  'Show more' option
        EXPECTED: * 'Show all selections' option becomes 'Show less' option after tapping on it
        """
        pass

    def test_010_go_to_outright_module_panelsub_panel_set_up_in_list_view(self):
        """
        DESCRIPTION: Go to Outright Module Panel/Sub Panel set up in **LIST** view
        EXPECTED: 
        """
        pass

    def test_011_verify_format_displaying_panelsub_panel_in_list_view(self):
        """
        DESCRIPTION: Verify format displaying Panel/Sub Panel in LIST view
        EXPECTED: * Outcome is displayed in the next format if 2 countries are received in outcome name:
        EXPECTED: country flag 1 country name 1 vs country flag 2 country name 2
        EXPECTED: e.g. flag 1 Iran vs flag 2 England
        """
        pass

    def test_012_repeat_steps_4_9(self):
        """
        DESCRIPTION: Repeat steps #4-9
        EXPECTED: 
        """
        pass

    def test_013_go_to_outright_module_panelsub_panel_set_up_in_card_view(self):
        """
        DESCRIPTION: Go to Outright Module Panel/Sub Panel set up in **CARD** view
        EXPECTED: 
        """
        pass

    def test_014_verify_outright_module_panelsub_panel_content_for_card_view(self):
        """
        DESCRIPTION: Verify Outright Module Panel/Sub Panel content for CARD view
        EXPECTED: Outright Module consists of:
        EXPECTED: * Selection name
        EXPECTED: * Price/odds button with the associated price
        EXPECTED: * 'Show next 'n' selection' option (if available)
        """
        pass

    def test_015_show_next_n_selection_option(self):
        """
        DESCRIPTION: 'Show next 'n' selection' option
        EXPECTED: * 'n' value corresponds to **competitionModules.[i].markets.[j].maxDisplay** attribute from from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j - the number of all Markets returned to Module
        EXPECTED: * 'Show next 'n' selection' option is displayed if there is more than 'n' outcomes returned within one market
        """
        pass

    def test_016_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step #7
        EXPECTED: 
        """
        pass
