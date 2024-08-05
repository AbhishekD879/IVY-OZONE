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
class Test_C2321112_Verify_Bet_Builder_for_Trifecta_Pool_Type(Common):
    """
    TR_ID: C2321112
    NAME: Verify Bet Builder for Trifecta Pool Type
    DESCRIPTION: This test case verifies UK Tote Bet Builder for Exacta Pool Type
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [UK Tote: Implement HR Trifecta pool type] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28445
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Trifecta pool type is available for HR Event
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
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_navigate_to_the_trifecta_pool_type_in_hr_event_with_uk_tote_pools_available(self):
        """
        DESCRIPTION: Navigate to the Trifecta pool type in HR Event with UK Tote pools available
        EXPECTED: * Trifecta pool type is opened and underlined
        EXPECTED: * '1st' Place Trifecta checkboxes are present (for every selection)
        EXPECTED: * '2nd' Place Trifecta checkboxes are present (for every selection)
        EXPECTED: * '3rd' Place Trifecta checkboxes are present (for every selection)
        EXPECTED: * 'Any' Place Trifecta checkboxes are present (for every selection)
        """
        pass

    def test_002_select_1st_place_checkbox_for_some_selection(self):
        """
        DESCRIPTION: Select '1st' Place checkbox for some selection
        EXPECTED: * '1st' Place checkbox is selected for current selection
        EXPECTED: * All others '1st' Place checkboxes are disabled for all other selections
        EXPECTED: * '2nd' checkbox is disabled for current selection
        EXPECTED: * '2nd' checkboxes are remains available for all other selections
        EXPECTED: * "3rd" check box for this runner is disabled
        EXPECTED: * "3rd" checkboxes are remains available for all other selections
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
        EXPECTED: * 3rd' checkbox is disabled for current selection
        EXPECTED: * All other '3rd' checkboxes are remains available for all other selections
        EXPECTED: * 'Any' Place checkboxes are remains disabled for all selections
        EXPECTED: * 'ADD TO BETSLIP' button is displayed on Tote Bet Builder
        """
        pass

    def test_006_select_3rd_place_checkbox_for_some_selection(self):
        """
        DESCRIPTION: Select '3rd' Place checkbox for some selection
        EXPECTED: * All other '3rd' Place checkboxes are disabled for every selection
        EXPECTED: * 'Any' Place checkboxes are remains disabled for all selections
        EXPECTED: * 'ADD TO BETSLIP' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: * **1 Trifecta Bet** name is shown on the left side of Tote Bet Builder
        """
        pass

    def test_007_click_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Click on 'ADD TO BETSLIP' button
        EXPECTED: * Tote Trifecta bet is added to the BetSlip
        EXPECTED: * '1st' Place Trifecta checkboxes are cleared and active (for every selection)
        EXPECTED: * '2nd' Place Trifecta checkboxes are cleared and active (for every selection)
        EXPECTED: * 'Any' Place Trifecta checkboxes are cleared and active (for every selection)
        EXPECTED: * Tote Bet Builder has disappeared
        EXPECTED: * Betslip gets the indicator 1
        """
        pass

    def test_008_select_1st_place_2nd_and_3rd_place_checkboxes_for_selections(self):
        """
        DESCRIPTION: Select '1st' Place, '2nd' and '3rd' Place checkboxes for selections
        EXPECTED: * All other '1st' Place, '2nd' Place and '3rd' Place checkboxes are disabled for every selection
        EXPECTED: * 'Any' Place checkboxes are disabled for all selections
        EXPECTED: * Tote Bet Builder is displayed at the bottom of the app
        """
        pass

    def test_009_click_on_clear_selections_button_underlined_link_on_tote_bet_builder(self):
        """
        DESCRIPTION: Click on 'Clear Selections' button (underlined link) on Tote Bet Builder
        EXPECTED: * '1st' Place Trifecta checkboxes are cleared and active (for every selection)
        EXPECTED: * '2nd' Place Trifecta checkboxes are cleared and active (for every selection)
        EXPECTED: * 'Any' Place Trifecta checkboxes are cleared and active (for every selection)
        EXPECTED: * Tote Bet Builder disappears
        """
        pass

    def test_010_select_three_selections_checkboxes_for_any_place(self):
        """
        DESCRIPTION: Select three selections (checkboxes) for 'Any' Place
        EXPECTED: * All '1st' Place, '2nd' Place and '3rd' Place checkboxes are disabled for every selection
        EXPECTED: * All other 'Any' Place checkboxes are enabled
        EXPECTED: * 'ADD TO BETSLIP' button is clickable (enabled) on Tote Bet Builder
        EXPECTED: * **6 Combination Trifecta Bets** name is shown on the left side of Tote Bet Builder
        """
        pass

    def test_011_select_more_than_three_selections_checkboxes_for_any_place(self):
        """
        DESCRIPTION: Select more than three selections (checkboxes) for 'Any' Place
        EXPECTED: * All '1st' Place, '2nd' Place and '3rd' Place checkboxes are disabled for every selection
        EXPECTED: * All other 'Any' Place checkboxes are enabled
        EXPECTED: * 'ADD TO BETSLIP' button is clickable (enabled) on Tote Bet Builder
        EXPECTED: * **X** **Combination Trifecta bets** name is shown on the left side of Tote Bet Builder
        """
        pass

    def test_012_verify_calculation_of_combination_exacta(self):
        """
        DESCRIPTION: Verify calculation of Combination Exacta
        EXPECTED: Combination Exacta is calculated by the formula:
        EXPECTED: * No of selections **x** next lowest number **x** next lowest number-1 (eg 5 Selections picked: 5 x 4 x 3  = 60 Combination Trifecta bets)
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
