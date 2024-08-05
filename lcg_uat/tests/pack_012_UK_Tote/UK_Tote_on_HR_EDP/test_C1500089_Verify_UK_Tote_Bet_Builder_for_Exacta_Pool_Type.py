import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.races
@vtest
class Test_C1500089_Verify_UK_Tote_Bet_Builder_for_Exacta_Pool_Type(BaseUKTote):
    """
    TR_ID: C1500089
    NAME: Verify UK Tote Bet Builder for Exacta Pool Type
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Exacta pool type is available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    uk_tote_pool_selection_id = None
    outcomes = None
    bet_builder = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        ob_config = cls.get_ob_config()
        if cls.uk_tote_pool_selection_id:
            ob_config.change_selection_state(selection_id=cls.uk_tote_pool_selection_id, displayed=True, active=True)

        if cls.eventID:
            ob_config.change_event_state(event_id=cls.eventID, displayed=True, active=True)

    def test_001_navigate_to_the_exacta_pool_type_in_hr_event_with_uk_tote_pools_available(self):
        """
        DESCRIPTION: Navigate to the Exacta pool type in HR Event with UK Tote pools available
        EXPECTED: HR Event Details page is opened
        EXPECTED: TOTEPOOL tab is opened
        EXPECTED: Exacta pool type is opened and underlined
        EXPECTED: '1st' Place exacta checkboxes are present (for every selection)
        EXPECTED: '2nd' Place exacta checkboxes are present (for every selection)
        EXPECTED: 'Any' Place exacta checkboxes are present (for every selection)
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')

    def test_002_select_1st_place_checkbox_for_some_selection(self):
        """
        DESCRIPTION: Select '1st' Place checkbox for some selection
        EXPECTED: '1st' Place checkbox is selected for current selection
        EXPECTED: All others '1st' Place checkboxes are disabled for all other selections
        EXPECTED: '2nd' Place checkbox is disabled for current selection
        EXPECTED: '2nd' Place checkboxes are remains available for all other selections
        EXPECTED: 'Any' Place checkboxes are disabled for all selections
        EXPECTED: Tote Bet Builder is appeared
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')

        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[0]
        checkbox.click()
        self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                    % (checkbox_name, outcome_name))

        result = wait_for_result(lambda: section.bet_builder.is_present() is True,
                                 name='Bet builder has not been shown', timeout=5)
        self.assertTrue(result, msg='Bet builder was not shown')

    def test_003_verify_tote_bet_builder(self):
        """
        DESCRIPTION: Verify Tote Bet Builder
        EXPECTED: Tote Bet Builder is placed at the bottom of the page
        EXPECTED: 'ADD TO BETSLIP' button is displayed on the right side of Tote Bet Builder
        EXPECTED: 'ADD TO BETSLIP' button is unclickable (disabled) on Tote Bet Builder
        EXPECTED: 'Clear Selections' button (underlined link) is placed near 'ADD TO BETSLIP' button (on the left side)
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.__class__.bet_builder = section.bet_builder
        self.assertFalse(self.bet_builder.summary.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='ADD TO BETSLIP button is not disabled')
        self.assertTrue(self.bet_builder.summary.clear_selection_button.is_displayed(), msg='Clear Selections button is not shown')

    def test_004_select_2nd_place_checkbox_for_some_selection(self):
        """
        DESCRIPTION: Select '2nd' Place checkbox for some selection
        EXPECTED: All other '2nd' Place checkboxes are disabled for every selection
        EXPECTED: 'Any' Place checkboxes are remains disabled for all selections
        EXPECTED: 'ADD TO BETSLIP' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: **1 Straight Exacta** bet type name is shown on the left side of Tote Bet Builder
        """
        outcome_name, outcome = self.outcomes[1]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[1]
        checkbox.click()
        self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                    % (checkbox_name, outcome_name))
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is disabled')

        self.assertEqual(self.bet_builder.summary.description_title, vec.uk_tote.STRAIGHT_EXACTA_BET)

    def test_005_click_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Click on 'ADD TO BETSLIP' button
        EXPECTED: Tote Exacta bet is added to the BetSlip
        EXPECTED: '1st' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: '2nd' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: 'Any' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: Tote Bet Builder is disappeared
        """
        self.bet_builder.summary.add_to_betslip_button.click()

        self.verify_betslip_counter_change(expected_value=1)

        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertTrue(checkbox.is_enabled(), msg='Checkbox "%s" is not enabled for "%s"'
                                                           % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.assertFalse(section.bet_builder.is_present(expected_result=False), msg='Tote Bet Builder was not disappeared')

    def test_006_select_1st_place_and_2nd_place_checkboxes_for_selections(self):
        """
        DESCRIPTION: Select '1st' Place and '2nd' Place checkboxes for selections
        EXPECTED: All other '1st' Place and '2nd' Place checkboxes are disabled for every selection
        EXPECTED: 'Any' Place checkboxes are disabled for all selections
        EXPECTED: Tote Bet Builder is appeared
        """
        self.test_002_select_1st_place_checkbox_for_some_selection()
        self.test_003_verify_tote_bet_builder()
        self.test_004_select_2nd_place_checkbox_for_some_selection()

    def test_007_click_on_clear_selections_button_underlined_link_on_tote_bet_builder(self):
        """
        DESCRIPTION: Click on 'Clear Selections' button (underlined link) on Tote Bet Builder
        EXPECTED: '1st' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: '2nd' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: 'Any' Place exacta checkboxes are cleared and active (for every selection)
        EXPECTED: Tote Bet Builder is disappeared
        """
        self.bet_builder.summary.clear_selection_button.click()
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.assertFalse(section.bet_builder.is_present(expected_result=False), msg='Tote Bet Builder was not disappeared')

    def test_008_select_two_selections_checkboxes_for_any_place(self):
        """
        DESCRIPTION: Select two selections (checkboxes) for 'Any' Place
        EXPECTED: All '1st' Place and '2nd' Place checkboxes are disabled for every selection
        EXPECTED: All other 'Any' Place checkboxes are remains enabled
        EXPECTED: 'ADD TO BETSLIP' button is clickable (enabled) on Tote Bet Builder
        EXPECTED: **1 Reverse Exacta** bet type name is shown on the left side of Tote Bet Builder
        """
        for outcome_name, outcome in self.outcomes[:2]:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[2]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.assertTrue(section.bet_builder.is_present(), msg='Tote Bet Builder was not found')
        self.__class__.bet_builder = section.bet_builder
        self.assertEqual(self.bet_builder.summary.description_title, vec.uk_tote.REVERSE_EXACTA_BET)

    def test_009_select_more_than_two_selections_checkboxes_for_any_place_and_verify_calculation_of_combination_exacta(self):
        """
        DESCRIPTION: Select more than two selections (checkboxes) for 'Any' Place
        DESCRIPTION: Verify calculation of Combination Exacta
        EXPECTED: All '1st' Place and '2nd' Place checkboxes are disabled for every selection
        EXPECTED: All other 'Any' Place checkboxes are remains enabled
        EXPECTED: 'ADD TO BETSLIP' button is clickable (enabled) on Tote Bet Builder
        EXPECTED: **X** **Combination Exacta** bet type name is shown on the left side of Tote Bet Builder
        EXPECTED: Combination Exacta is calculated by the formula:
        EXPECTED: No. of selections **x** next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        """
        for outcome_name, outcome in self.outcomes[2:4]:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[2]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        self.assertEqual(self.bet_builder.summary.description_title, vec.uk_tote.COMBINATION_EXACTA_BET.format(number=12))

    def test_010_repeat_step_6(self):
        """
        DESCRIPTION: Repeat step 6
        EXPECTED:
        """
        self.bet_builder.summary.clear_selection_button.click()

        self.test_006_select_1st_place_and_2nd_place_checkboxes_for_selections()

    def test_011_suspend_one_selected_selection(self):
        """
        DESCRIPTION: Suspend one selected selection
        EXPECTED: Suspended selection is unselected
        EXPECTED: Active selection remains selected
        EXPECTED: Tote Bet Builder is shown (with disabled 'ADD TO BETSLIP' button)
        """
        outcome_name, outcome = self.outcomes[0]
        ss_uk_tote_pool = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.eventID,
            query_builder=self.ss_query_builder)
        ss_uk_tote_pool_outcomes = ss_uk_tote_pool[0]['event']['children'][0]['market']['children']
        selection_id, selection_name = next(((outcome['outcome']['id'], outcome['outcome']['name']) for outcome in ss_uk_tote_pool_outcomes
                                             if outcome_name == outcome['outcome']['name']), (None, None))
        self.assertTrue(selection_id, msg='Cannot find selection "%s" from SS response' % outcome_name)
        self.__class__.uk_tote_pool_selection_id = selection_id
        self.ob_config.change_selection_state(selection_id=self.uk_tote_pool_selection_id)

        self.assertFalse(self.bet_builder.summary.add_to_betslip_button.is_enabled(expected_result=False, timeout=25),
                         msg='ADD TO BETSLIP button is not disabled')

    def test_012_suspend_current_exacta_pool(self):
        """
        DESCRIPTION: Suspend current Exacta pool
        EXPECTED: All suspended selections are unselected
        EXPECTED: Tote Bet Builder is disappeared
        """
        self.ob_config.change_event_state(event_id=self.eventID)
        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertFalse(checkbox.is_selected(timeout=5, expected_result=False),
                                 msg='Checkbox "%s" is not unselected for "%s"' % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.assertFalse(section.bet_builder.is_present(expected_result=False), msg='Tote Bet Builder was not disappeared')
