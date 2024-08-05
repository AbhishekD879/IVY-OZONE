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
class Test_C1500089_Verify_Bet_Builder_for_Exacta_Pool_Type(Common):
    """
    TR_ID: C1500089
    NAME: Verify Bet Builder for Exacta Pool Type
    DESCRIPTION: This test case verifies UK Tote Bet Builder for Exacta Pool Type
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-28915 UK Tote: Tote Bet Builder for Exacta Pool Type] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28915
    DESCRIPTION: AUTOTEST [C2080980]
    DESCRIPTION: AUTOTEST [C2089452]
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Exacta pool type is available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_navigate_to_the_exacta_pool_type_in_hr_event_with_uk_tote_pools_available(self):
        """
        DESCRIPTION: Navigate to the Exacta pool type in HR Event with UK Tote pools available
        EXPECTED: * HR Event Details page is opened
        EXPECTED: * TOTEPOOL tab is opened
        EXPECTED: * Exacta pool type is opened and underlined
        EXPECTED: * '1st' Place exacta checkboxes are present (for every selection)
        EXPECTED: * '2nd' Place exacta checkboxes are present (for every selection)
        EXPECTED: * 'Any' Place exacta checkboxes are present (for every selection)
        """
        pass

    def test_002_select_1st_place_checkbox_for_some_selection(self):
        """
        DESCRIPTION: Select '1st' Place checkbox for some selection
        EXPECTED: * '1st' Place checkbox is selected for current selection
        EXPECTED: * All others '1st' Place checkboxes are disabled for all other selections
        EXPECTED: * '2nd' Place checkbox is disabled for current selection
        EXPECTED: * '2nd' Place checkboxes are remains available for all other selections
        EXPECTED: * 'Any' Place checkboxes are disabled for all selections
        EXPECTED: * Tote Bet Builder has appeared
        """
        pass

    def test_003_verify_tote_bet_builder(self):
        """
        DESCRIPTION: Verify Tote Bet Builder
        EXPECTED: * Tote Bet Builder is placed at the bottom of the page
        EXPECTED: * 'ADD TO BETSLIP' button is displayed on the right side of Tote Bet Builder
        EXPECTED: * 'ADD TO BETSLIP' button is unclickable (disabled) on Tote Bet Builder
        EXPECTED: * 'Clear Selections' button (underlined link) is placed near 'ADD TO BETSLIP' button (on the left side)
        """
        pass

    def test_004_scroll_the_page(self):
        """
        DESCRIPTION: Scroll the page
        EXPECTED: * Tote Bet Builder is sticky at the bottom of the page (instead of the app footer on mobile)
        EXPECTED: * Tote Bet Builder is sticky at the bottom of the markets section on HR EDP (tablet/desktop)
        """
        pass

    def test_005_select_2nd_place_checkbox_for_some_selection(self):
        """
        DESCRIPTION: Select '2nd' Place checkbox for some selection
        EXPECTED: * All other '2nd' Place checkboxes are disabled for every selection
        EXPECTED: * 'Any' Place checkboxes are remains disabled for all selections
        EXPECTED: * 'ADD TO BETSLIP' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: * **1 Exacta Bet** name is shown on the left side of Tote Bet Builder
        """
        pass

    def test_006_click_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Click on 'ADD TO BETSLIP' button
        EXPECTED: * Tote Exacta bet is added to the BetSlip
        EXPECTED: * '1st' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: * '2nd' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: * 'Any' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: * Tote Bet Builder has disappeared
        EXPECTED: * Betslip gets the indicator 1
        """
        pass

    def test_007_select_1st_place_and_2nd_place_checkboxes_for_selections(self):
        """
        DESCRIPTION: Select '1st' Place and '2nd' Place checkboxes for selections
        EXPECTED: * All other '1st' Place and '2nd' Place checkboxes are disabled for every selection
        EXPECTED: * 'Any' Place checkboxes are disabled for all selections
        EXPECTED: * Tote Bet Builder is displayed at the bottom of the app
        """
        pass

    def test_008_click_on_clear_selections_button_underlined_link_on_tote_bet_builder(self):
        """
        DESCRIPTION: Click on 'Clear Selections' button (underlined link) on Tote Bet Builder
        EXPECTED: * '1st' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: * '2nd' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: * 'Any' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: * Tote Bet Builder disappears
        """
        pass

    def test_009_select_two_selections_checkboxes_for_any_place(self):
        """
        DESCRIPTION: Select two selections (checkboxes) for 'Any' Place
        EXPECTED: * All '1st' Place and '2nd' Place checkboxes are disabled for every selection
        EXPECTED: * All other 'Any' Place checkboxes are enabled
        EXPECTED: * 'ADD TO BETSLIP' button is clickable (enabled) on Tote Bet Builder
        EXPECTED: * **1 Reverse Exacta Bet ** name is shown on the left side of Tote Bet Builder
        """
        pass

    def test_010_select_more_than_two_selections_checkboxes_for_any_place(self):
        """
        DESCRIPTION: Select more than two selections (checkboxes) for 'Any' Place
        EXPECTED: * All '1st' Place and '2nd' Place checkboxes are disabled for every selection
        EXPECTED: * All other 'Any' Place checkboxes are enabled
        EXPECTED: * 'ADD TO BETSLIP' button is clickable (enabled) on Tote Bet Builder
        EXPECTED: * **X** **Combination Exacta bets** name is shown on the left side of Tote Bet Builder
        """
        pass

    def test_011_verify_calculation_of_combination_exacta(self):
        """
        DESCRIPTION: Verify calculation of Combination Exacta
        EXPECTED: Combination Exacta is calculated by the formula:
        EXPECTED: * No. of selections **x** next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        """
        pass

    def test_012_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step 7
        EXPECTED: 
        """
        pass

    def test_013_suspend_one_selected_selection(self):
        """
        DESCRIPTION: Suspend one selected selection
        EXPECTED: * Suspended selection is unselected
        EXPECTED: * Active selection remains selected
        EXPECTED: * Tote Bet Builder is shown (with disabled 'ADD TO BETSLIP' button)
        """
        pass

    def test_014_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step 7
        EXPECTED: 
        """
        pass

    def test_015_suspend_current_exacta_pool(self):
        """
        DESCRIPTION: Suspend current Exacta pool
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder is disappeared
        """
        pass
