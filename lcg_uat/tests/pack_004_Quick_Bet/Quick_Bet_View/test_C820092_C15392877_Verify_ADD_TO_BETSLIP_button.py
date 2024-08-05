import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.quick_bet
@pytest.mark.each_way
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.safari
@vtest
class Test_C820092_C15392877_Verify_ADD_TO_BETSLIP_button(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C820092
    TR_ID: C15392877
    VOL_ID: C9698329
    NAME: Verify 'ADD TO BETSLIP' button
    DESCRIPTION: This test case verifies 'ADD TO BETSLIP' button within Quick Bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True
    outcomes = None
    first_selection_name, second_selection_name = None, None
    bet_amount = 0.03

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active horseracing event
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
            self._logger.debug(f'*** Found Horse racing event "{event}"')
            self.__class__.eventID = event['event']['id']
            self.__class__.created_event_name = normalize_name(event['event']['name'])
            outcomes_resp = event['event']['children'][0]['market']['children']
            self.__class__.selection_ids = {}

            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_resp if
                                 'Unnamed' not in i['outcome']['name']}
            self.__class__.selection_ids = dict(list(all_selection_ids.items())[:2])
            self.__class__.first_selection_name, self.__class__.second_selection_name = [key for key in self.selection_ids.keys() if 'Unnamed' not in key][:2]

        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=2, ew_terms=self.ew_terms)
            self.__class__.selection_ids = event.selection_ids
            self.__class__.eventID = event.event_id
            self.__class__.created_event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            self.__class__.market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.replace('|', '')
        self.__class__.first_selection_name, self.__class__.second_selection_name = list(self.selection_ids.keys())[:2]

    def test_001_open_event(self):
        """
        DESCRIPTION: Open created event
        EXPECTED: EDP of event is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

    def test_002_tap_one_race_selection(self):
        """
        DESCRIPTION: Tap one <Race> selection with Each Way option available
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox
        EXPECTED: Quick Bet appears at the bottom of the page
        EXPECTED: 'E/W' checkbox is displayed within Quick Bet
        EXPECTED: 'Stake' field is pre-populated with value
        EXPECTED: 'E/W' checkbox is selected
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.__class__.outcomes = outcomes
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        outcome = outcomes.get(self.first_selection_name)
        outcome.bet_button.click()

        self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet is not shown')
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = self.bet_amount
        quick_bet.each_way_checkbox.click()
        self.__class__.amount = f'{float(self.bet_amount):.2f}'
        self.assertEqual(quick_bet.amount_form.input.value, self.amount,
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not match '
                         f'expected "{self.amount}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')

    def test_003_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'ADD TO BETSLIP' button
        EXPECTED: Quick Bet is closed automatically
        EXPECTED: Selection is added to Betslip
        EXPECTED: Betslip counter is increased by 1
        EXPECTED: 'Stake' field is pre-populated with the same value as on step #7
        EXPECTED: 'E/W' checkbox is selected
        """
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

        self.verify_betslip_counter_change(expected_value=1)

        self.site.header.bet_slip_counter.click()
        result = self.get_betslip_content()
        self.assertTrue(result, msg='Betslip widget not displayed')
        section = self.get_betslip_sections().Singles
        stake = section.get(self.first_selection_name)
        self.assertTrue(stake, msg='Stake "{self.first_selection_name}" is not found in Betslip')
        self.assertEqual(stake.amount_form.input.value, str(self.amount),
                         msg=f'Actual amount "{stake.amount_form.input.value}" does not match expected "{str(self.amount)}"')
        self.assertTrue(stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')

        self.site.close_betslip()
        self.site.has_betslip_opened(expected_result=False)

    def test_004_tap_second_sport_race_selection(self):
        """
        DESCRIPTION: Tap second <Race> selection
        EXPECTED: Quick Bet is NOT opened
        EXPECTED: Selection is added to Betslip
        EXPECTED: Betslip counter is increased by 1
        """
        outcome = self.outcomes[self.second_selection_name]
        self.assertEqual(self.second_selection_name, list(self.selection_ids.keys())[1],
                         msg=f'Actual Outcome name "{self.second_selection_name}" does not match expected "{list(self.selection_ids.keys())[1]}"')
        outcome.bet_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet should not appear')

        self.verify_betslip_counter_change(expected_value=2)

        self.site.header.bet_slip_counter.click()
        result = self.get_betslip_content()
        self.assertTrue(result, msg='Betslip widget not displayed')
        section = self.get_betslip_sections().Singles
        self.assertEqual(sorted(section.keys()), sorted(list(self.selection_ids.keys())))
