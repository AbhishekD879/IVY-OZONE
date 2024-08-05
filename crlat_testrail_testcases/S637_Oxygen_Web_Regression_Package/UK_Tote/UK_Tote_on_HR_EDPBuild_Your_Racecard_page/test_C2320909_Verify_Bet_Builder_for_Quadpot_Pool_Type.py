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
class Test_C2320909_Verify_Bet_Builder_for_Quadpot_Pool_Type(Common):
    """
    TR_ID: C2320909
    NAME: Verify Bet Builder for Quadpot Pool Type
    DESCRIPTION: This test case verifies UK Tote Bet Builder for Quadpot Pool Type
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-28479 UK Tote: HR Placepot pool bet builder] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28479
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Quadpot pool type is available for HR Event
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
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- endpoint .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_navigate_to_the_quadpot_pool_type_tab(self):
        """
        DESCRIPTION: Navigate to the Quadpot pool type tab
        EXPECTED: * Quadpot pool type is opened and underlined
        EXPECTED: * Leg1 is opened and underlined by default
        EXPECTED: * Checkboxes are present (for every selection)
        """
        pass

    def test_002_select_checkboxes_for_some_selections_from_leg1(self):
        """
        DESCRIPTION: Select checkboxes for some selections from Leg1
        EXPECTED: * Checkboxes are selected for current selections
        EXPECTED: * All others are available for all other selections
        EXPECTED: * Tote Bet Builder appears
        """
        pass

    def test_003_verify_tote_bet_builder(self):
        """
        DESCRIPTION: Verify Tote Bet Builder
        EXPECTED: * Tote Bet Builder is placed at the bottom of the page
        EXPECTED: * '<currency symbol> <stake amount> TOTAL STAKE' button is displayed on the right side of Tote Bet Builder
        EXPECTED: * '<currency symbol> <stake amount> TOTAL STAKE' button is unclickable (disabled) on Tote Bet Builder
        EXPECTED: * 'Open' option is placed near 'TOTAL STAKE' button (on the left side)
        EXPECTED: * Number of lines (for example: 'No. Lines 1') is shown on the left side of BetBuilder
        EXPECTED: * 'Stake per line' text is shown after Number of lines
        EXPECTED: * 'Stake per line' input field is shown next to text
        """
        pass

    def test_004_click_on_open_option(self):
        """
        DESCRIPTION: Click on 'Open' option
        EXPECTED: * 'Selections Overview Widget' is expanded
        EXPECTED: * List with selected selection per each Leg is shown
        EXPECTED: * 'Leg <number>' is shown for each selection (on the left side)
        EXPECTED: * Runner number is shown for each selection
        EXPECTED: * 'Remove' icon is shown for each selection (on the right side of list)
        EXPECTED: * Open option is named as Close
        """
        pass

    def test_005_click_on_remove_icon_near_some_selection(self):
        """
        DESCRIPTION: Click on 'Remove' icon near some selection
        EXPECTED: * Current selection is removed from BetBuilder
        EXPECTED: * Checkbox for current selection is unchecked
        """
        pass

    def test_006_add_a_selection_click_on_open_and_click_on_close_option(self):
        """
        DESCRIPTION: Add a selection, click on 'Open' and click on Close option
        EXPECTED: * 'Selections Overview Widget' is collapsed
        EXPECTED: * List with selected selection per each Leg is hidden
        """
        pass

    def test_007_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: * All selections are selected for each Leg
        EXPECTED: * 'No. Lines' value is updated accordingly
        """
        pass

    def test_008_enter_some_stake_amount_into_stake_per_line_input_field(self):
        """
        DESCRIPTION: Enter some stake amount into 'Stake per line' input field
        EXPECTED: * Stake amount is shown in the 'Stake per line' input field
        EXPECTED: * Stake amount is shown in format <currency symbol> <stake amount value>
        EXPECTED: * '<currency symbol> <stake amount> TOTAL STAKE' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: * 'TOTAL STAKE' value is updated accordingly
        """
        pass

    def test_009_click_on_currency_symbol_stake_amount_total_stake_button(self):
        """
        DESCRIPTION: Click on '<currency symbol> <stake amount> TOTAL STAKE' button
        EXPECTED: * Quadpot bet is added to the BetSlip
        EXPECTED: * All Quadpot checkboxes are cleared (for each Leg)
        EXPECTED: * Quadpot Bet Builder disappears
        """
        pass

    def test_010_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selection pool is displayed in Betslip
        """
        pass

    def test_011_remove_selection_from_betslip_or_place_bet(self):
        """
        DESCRIPTION: Remove selection from betslip or place bet
        EXPECTED: * Betslip is closed
        EXPECTED: * User is on racecard
        """
        pass

    def test_012_make_few_selections_and_click_on_open_option(self):
        """
        DESCRIPTION: Make few selections and click on Open option
        EXPECTED: All selections are displayed in the Selections Overview Widget
        """
        pass

    def test_013_uncheck_few_selections_in_race_card(self):
        """
        DESCRIPTION: Uncheck few selections in race card
        EXPECTED: Selections that are unchecked in race card disappear from Selections Overview Widget
        """
        pass
