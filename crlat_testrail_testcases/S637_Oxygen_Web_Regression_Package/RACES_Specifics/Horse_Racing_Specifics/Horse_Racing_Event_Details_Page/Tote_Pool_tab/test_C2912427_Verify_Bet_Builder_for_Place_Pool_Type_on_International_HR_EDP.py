import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2912427_Verify_Bet_Builder_for_Place_Pool_Type_on_International_HR_EDP(Common):
    """
    TR_ID: C2912427
    NAME: Verify Bet Builder for Place Pool Type on International HR EDP
    DESCRIPTION: This test case verifies International Tote Bet Builder for Place Pool Type
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * International Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool type is available for International HR Event
    PRECONDITIONS: * User should have a  International HR EDP open ("Tote" tab)
    """
    keep_browser_open = True

    def test_001_navigate_to_the_place_pool_type_in_hr_event_with_international_tote_pools_available(self):
        """
        DESCRIPTION: Navigate to the Place pool type in HR Event with International Tote pools available
        EXPECTED: * HR Event Details page is opened
        EXPECTED: * TOTEPOOL tab is opened
        EXPECTED: * Place pool type is opened and underlined
        EXPECTED: * Place selections are available for each runner
        """
        pass

    def test_002_select_1_selection_press_place_button(self):
        """
        DESCRIPTION: Select 1 selection (press Place button)
        EXPECTED: * 1 Place selection is selected for current runner
        EXPECTED: * All others are unselected
        EXPECTED: * Tote Bet Builder appears
        """
        pass

    def test_003_verify_tote_bet_builder(self):
        """
        DESCRIPTION: Verify Tote Bet Builder
        EXPECTED: * Tote Bet Builder is placed at the bottom of the page
        EXPECTED: * 'ADD TO BETSLIP' green active button is displayed on the right side
        EXPECTED: * 'Clear Selections' button (underlined link) is placed near 'ADD TO BETSLIP' button (on the left side)
        EXPECTED: * Number of Place selections is displayed on the left of bet builder
        """
        pass

    def test_004_scroll_the_page(self):
        """
        DESCRIPTION: Scroll the page
        EXPECTED: * Tote Bet Builder is sticky at the bottom of the page (instead of the app footer on mobile)
        EXPECTED: * Tote Bet Builder is sticky at the bottom of the markets section on HR EDP (tablet/desktop)
        """
        pass

    def test_005_unselect_the_selected_place_button(self):
        """
        DESCRIPTION: Unselect the selected Place button
        EXPECTED: * Button becomes unselected (grey)
        EXPECTED: * Bet builder disappears
        """
        pass

    def test_006_select_some_buttons_and_click_on_clear_selections_link_in_bet_builder(self):
        """
        DESCRIPTION: Select some buttons and click on 'Clear Selections' link in bet builder
        EXPECTED: * Button becomes unselected (grey)
        EXPECTED: * Bet builder disappears
        """
        pass

    def test_007_select_several_selections_once_again(self):
        """
        DESCRIPTION: Select several selections once again
        EXPECTED: * Corresponding selection buttons become green (selected)
        EXPECTED: * Bet builder appears with all previously mentioned components
        EXPECTED: * Number of Place buttons selected is updated in bet builder on the left (eg. 2 Place Selections)
        """
        pass

    def test_008_click_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Click on 'ADD TO BETSLIP' button
        EXPECTED: * Tote Place bet is added to the BetSlip
        EXPECTED: * Selected buttons become unselected
        EXPECTED: * Tote Bet Builder has disappeared
        EXPECTED: * Betslip gets the indicator 1
        """
        pass
