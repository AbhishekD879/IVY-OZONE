import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


# @pytest.mark.tst2 # Tote wont available in qa envs
# @pytest.mark.stg2 # Tote wont available in stg envs
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C2320910_Verify_Bet_Builder_for_Jackpot_Pool_Type(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2320910
    NAME: Verify Bet Builder for Jackpot Pool Type
    DESCRIPTION: This test case verifies UK Tote Bet Builder for Jackpot Pool Type
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-28479 UK Tote: HR Placepot pool bet builder] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28479
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Jackpot pool type is available for HR Event
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
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- endpoint .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    currency = '£'
    amount = 1
    bet_amount = '0.00'

    def test_001_navigate_to_the_jackpot_pool_type_tab(self):
        """
        DESCRIPTION: Navigate to the Jackpot pool type tab
        EXPECTED: * Jackpot pool type is opened and underlined
        EXPECTED: * Leg1 is opened and underlined by default
        EXPECTED: * Checkboxes are present (for every selection)
        """
        event = self.get_uk_tote_event(uk_tote_jackpot=True)
        self.navigate_to_edp(event_id=event.event_id, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        jackpot_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.jackpot)
        self.assertTrue(jackpot_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.jackpot}" tab is not opened')

    def test_002_select_checkboxes_for_some_selections_from_leg1(self):
        """
        DESCRIPTION: Select checkboxes for some selections from Leg1
        EXPECTED: * Checkboxes are selected for current selections
        EXPECTED: * All others are available for all other selections
        EXPECTED: * Tote Bet Builder appears
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, self.__class__.section = list(sections.items())[0]
        self.__class__.pool = self.section.pool
        self.__class__.pool_legs = self.pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(self.pool_legs, 'Pool section: "%s" not contains any leg' % section_name)
        pool_leg_name = 'LEG 1' if tests.settings.brand == 'bma' else 'Leg 1'

        self.pool.grouping_buttons.click_button(button_name=pool_leg_name)
        outcomes = self.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg: "%s"' % pool_leg_name)
        for outcome_name, outcome in list(outcomes.items())[:3]:
            outcome.select()
            self.assertTrue(self.section.bet_builder.summary.no_lines.value,
                            msg='"No. Lines" values is: "%s"' % self.section.bet_builder.summary.no_lines.value)
        self.__class__.bet_builder = self.section.bet_builder
        self.assertTrue(self.bet_builder, msg='"Bet Builder" not opened')

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
        total_stake = self.bet_builder.summary.add_to_betslip_button.label
        self.assertTrue(total_stake, msg=' "Total Stake" text not present')
        expected_value = '{0}{1}'.format(self.currency, self.bet_amount)
        self.assertEqual(self.bet_builder.summary.add_to_betslip_button.value, expected_value,
                         msg=f'Actual total stake value: "{self.bet_builder.summary.add_to_betslip_button.value}", '
                             f'expected: "{expected_value}"')
        self.assertFalse(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                         msg='"ADD TO SLIP" button is disabled')

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
        self.bet_builder.summary.open.click()
        is_expanded = self.section.is_bet_builder_expanded
        self.assertTrue(is_expanded, msg='Bet Buider not expanded')
        self.__class__.selections = self.bet_builder.selections.items_as_ordered_dict
        for leg_number, selection in list(self.selections.items()):
            self.assertTrue(selection.leg_number, msg='"Leg number" is not shown')
            self.assertTrue(selection.name, msg='"Horse Name" is not shown')
            self.assertTrue(selection.remove, msg='"Remove button" is not shown')
        close_name = self.bet_builder.summary.open.text
        self.assertEqual(close_name, vec.uk_tote.CLOSE,
                         msg=f'Acutal Name: "{close_name}" is not same as '
                             f'Expected Name: "{vec.uk_tote.CLOSE}"')

    def test_005_click_on_remove_icon_near_some_selection(self):
        """
        DESCRIPTION: Click on 'Remove' icon near some selection
        EXPECTED: * Current selection is removed from BetBuilder
        EXPECTED: * Checkbox for current selection is unchecked
        """
        selection_1_name, selection_1 = list(self.selections.items())[0]
        selection_1.remove.click()
        sleep(3)
        selection_names = self.bet_builder.selections.items_as_ordered_dict.keys()
        self.assertNotIn(selection_1_name, selection_names, msg=f'Selection name : "{selection_1_name}" is in "{selection_names}"')
        self.bet_builder.summary.open.click()
        outcomes = self.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg:')
        outcome = list(outcomes.values())[0]
        self.assertFalse(outcome.is_selected(expected_result=False),
                         msg='"Outcome" is selected')

    def test_006_add_a_selection_click_on_open_and_click_on_close_option(self):
        """
        DESCRIPTION: Add a selection, click on 'Open' and click on Close option
        EXPECTED: * 'Selections Overview Widget' is collapsed
        EXPECTED: * List with selected selection per each Leg is hidden
        """
        self.bet_builder.summary.open.click()
        outcomes = self.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg:')
        outcome = list(outcomes.values())[3]
        outcome.select()
        self.bet_builder.summary.open.click()
        sleep(2)
        is_expanded = self.section.is_bet_builder_expanded
        self.assertFalse(is_expanded, msg=f' "Bet builder " is expanded')

    def test_007_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: * All selections are selected for each Leg
        EXPECTED: * 'No. Lines' value is updated accordingly
        """
        for pool_leg_name, pool_leg in list(self.pool_legs.items())[0:]:
            self.pool.grouping_buttons.click_button(button_name=pool_leg_name)
            outcomes = self.pool.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcomes found for pool leg: "%s"' % pool_leg_name)
            outcome_name, outcome = list(outcomes.items())[0]
            outcome.select()
            self.assertTrue(self.section.bet_builder.summary.no_lines.value,
                            msg='"No. Lines" values is: "%s"' % self.section.bet_builder.summary.no_lines.value)
        self.__class__.bet_builder = self.section.bet_builder
        for pool_leg_name, pool_leg in self.pool_legs.items():
            pool_leg.scroll_to()
            self.assertTrue(pool_leg.is_filled(),
                            msg='Pool leg switch button: "%s" not selected after adding selection' % pool_leg_name)

    def test_008_enter_some_stake_amount_into_stake_per_line_input_field(self):
        """
        DESCRIPTION: Enter some stake amount into 'Stake per line' input field
        EXPECTED: * Stake amount is shown in the 'Stake per line' input field
        EXPECTED: * Stake amount is shown in format <currency symbol> <stake amount value>
        EXPECTED: * '<currency symbol> <stake amount> TOTAL STAKE' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: * 'TOTAL STAKE' value is updated accordingly
        """
        self.bet_builder.summary.input.value = self.amount
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO SLIP" button is disabled')
        self.assertEqual(self.bet_builder.summary.add_to_betslip_button.label, vec.quickbet.STAKE_LABEL.upper(),
                         msg=f'Actual label: "{self.bet_builder.summary.add_to_betslip_button.label}" is not same as'
                             f'Expected label: "{vec.quickbet.STAKE_LABEL.upper()}"')

    def test_009_click_on_currency_symbol_stake_amount_total_stake_button(self):
        """
        DESCRIPTION: Click on '<currency symbol> <stake amount> TOTAL STAKE' button
        EXPECTED: * Jackpot bet is added to the BetSlip
        EXPECTED: * All Jackpot checkboxes are cleared (for each Leg)
        EXPECTED: * Jackpot Bet Builder disappears
        """
        self.bet_builder.summary.add_to_betslip_button.click()
        self.assertFalse(self.section.bet_builder.is_displayed(expected_result=False),
                         msg='Bet builder not disappears')

    def test_010_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selection pool is displayed in Betslip
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

    def test_011_remove_selection_from_betslip_or_place_bet(self):
        """
        DESCRIPTION: Remove selection from betslip or place bet
        EXPECTED: * Betslip is closed
        EXPECTED: * User is on racecard
        """
        singles_sections = self.get_betslip_sections().Singles
        stake = list(singles_sections.values())[0]
        stake.remove_button.click()

    def test_012_make_few_selections_and_click_on_open_option(self):
        """
        DESCRIPTION: Make few selections and click on Open option
        EXPECTED: All selections are displayed in the Selections Overview Widget
        """
        self.test_002_select_checkboxes_for_some_selections_from_leg1()

    def test_013_uncheck_few_selections_in_race_card(self):
        """
        DESCRIPTION: Uncheck few selections in race card
        EXPECTED: Selections that are unchecked in race card disappear from Selections Overview Widget
        """
        self.bet_builder.summary.open.click()
        self.__class__.selections = self.bet_builder.selections.items_as_ordered_dict
        self.test_005_click_on_remove_icon_near_some_selection()
