from time import sleep

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.crl_stg2
@pytest.mark.quick_bet
@pytest.mark.smoke
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.safari
@vtest
class Test_C717034_C811305_C717043_C15392869_Verify_Quick_Bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C717034
    TR_ID: C811305
    TR_ID: C717043
    TR_ID: C15392869
    VOL_ID: C9697830
    NAME: Verify Quick Bet.
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: The layout of Quick Bet:
    PRECONDITIONS: ![](index.php?/attachments/get/115468133)                           ![](index.php?/attachments/get/115468132)
    PRECONDITIONS: Load Oxygen app
    """
    keep_browser_open = True
    price = None
    quick_bet_title = 'Quick Bet'
    odds_label = vec.quickbet.ODDS_LABEL
    stake_label = vec.quickbet.STAKE_LABEL
    each_way_label = 'Each Way'
    bet_amount = 0.03
    est_returns_label = vec.quickbet.TOTAL_EST_RETURNS_LABEL
    login_and_place_bet_button_name = vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION
    start_date_minus = get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S", hours=-2)
    outcome_name = None
    total_estimate_returns = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active horseracing event
        """
        if tests.settings.backend_env == 'prod':
            ew_available_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=ew_available_filter)[0]
            self._logger.debug(f'*** Found Horse racing event "{event}"')
            self.__class__.eventID = event['event']['id']
            self.__class__.created_event_name = normalize_name(event['event']['name'])
            self.__class__.market_name = event['event']['children'][0]['market']['name']
            outcomes_resp = event['event']['children'][0]['market']['children']
            # gets outcome name and LP, if there's no LP returns first outcome and sets empty price response
            self.__class__.outcome_name, price_resp = next(
                ((i['outcome']['name'], i['outcome']['children'][0]['price']) for i in outcomes_resp
                 if 'Unnamed' not in i['outcome']['name'] and i['outcome'].get('children') and 'price' in
                 i['outcome']['children'][0].keys()),
                (next((i['outcome']['name'] for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']), None), ''))
            self.assertTrue(self.outcome_name, msg='Horseracing outcome is not present')
            self.__class__.price = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}' if price_resp else 'SP'  # if price response is empty -> SP
            self.__class__.total_estimate_returns = '0.00' if price_resp else 'N/A'  # if price response is empty -> total est returns is N/A
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            self.__class__.selection_ids = event.selection_ids
            self.__class__.eventID = event.event_id
            name_pattern = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
            self.__class__.created_event_name = f'{event.event_off_time} {name_pattern}'
            self.__class__.market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.replace(
                '|', '')
            self.__class__.price = 'SP'
            self.__class__.outcome_name = list(self.selection_ids.keys())[0]
            self.__class__.total_estimate_returns = 'N/A'

    def test_001_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any Selection
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * Betslip counter does NOT increase by one
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.add_selection_to_quick_bet(outcome_name=self.outcome_name)
        self.verify_betslip_counter_change(expected_value=0)

    def test_002_verify_quick_bet_opening(self):
        """
        DESCRIPTION: Verify Quick Bet opening
        EXPECTED: * Quick Bet is opened with slide-in animation that begins from the bottom of the page
        EXPECTED: * Greyed-out overlay is displayed under Quick Bet
        """
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.assertEqual(self.quick_bet.header.title, self.quick_bet_title,
                         msg=f'Actual title "{self.quick_bet.header.title}" does not match expected "{self.quick_bet_title}"')

    def test_003_verify_quick_bet_displaying(self):
        """
        DESCRIPTION: Verify Quick Bet displaying
        EXPECTED: Quick Bet consists of:
        EXPECTED: * Selection name
        EXPECTED: * Market name / event name
        EXPECTED: * Promo icon (LADBROKES ONLY)
        EXPECTED: * Estimated Returns ( **CORAL**) / Potential Returns ( **LADBROKES** ) for that individual bet
        EXPECTED: * Total Stake for that individual bet
        """
        self.assertTrue(self.quick_bet.header.close_button.is_displayed(), msg='Quick Bet close button is not shown')
        self.assertEqual(self.quick_bet.selection.content.odds, self.price,
                         msg=f'Actual price "{self.quick_bet.selection.content.odds}" does not match expected "{self.price}"')
        self.assertEqual(self.quick_bet.selection.content.event_name, self.created_event_name,
                         msg=f'Actual Event Name "{self.quick_bet.selection.content.event_name}" does not '
                             f'match expected "{self.created_event_name}"')
        self.assertEqual(self.quick_bet.selection.content.market_name, self.market_name,
                         msg=f'Actual Market Name "{self.quick_bet.selection.content.market_name}" does not '
                             f'match expected "{self.market_name}"')
        self.assertEqual(self.quick_bet.selection.content.outcome_name, self.outcome_name,
                         msg=f'Actual Outcome Name "{self.quick_bet.selection.content.outcome_name}" does not '
                             f'match expected "{self.outcome_name}"')
        self.assertTrue(self.quick_bet.selection.content.has_each_way_checkbox(), 'Each Way checkbox is not shown')
        self.assertEqual(self.quick_bet.selection.content.each_way_checkbox.each_way_label, self.each_way_label,
                         msg=f'Actual EW label "{self.quick_bet.selection.content.each_way_checkbox.each_way_label}" does not '
                             f'match expected "{self.each_way_label}"')

        self.assertEqual(self.quick_bet.selection.content.amount_form.default_value, 'Stake',
                         msg=f'Actual default amount value "{self.quick_bet.selection.content.amount_form.default_value}" '
                             f'does not match expected "Stake"')
        self.assertTrue(self.quick_bet.selection.quick_stakes.is_enabled(), msg='Quick Stakes buttons are not shown')

        self.assertEqual(self.quick_bet.selection.bet_summary.stake_label, self.stake_label,
                         msg=f'Actual Total Stake label "{self.quick_bet.selection.bet_summary.stake_label}" does not '
                             f'match expected "{self.stake_label}"')

        self.assertEqual(self.quick_bet.selection.bet_summary.est_returns_label, self.est_returns_label,
                         msg=f'Actual Est Returns label "{self.quick_bet.selection.bet_summary.est_returns_label}" does not '
                             f'match expected "{self.est_returns_label}"')
        self.assertEqual(self.quick_bet.selection.bet_summary.total_stake, '0.00',
                         msg=f'Actual default Total Stake amount value "{self.quick_bet.selection.bet_summary.total_stake}" '
                             f'does not match expected "0.00"')
        self.assertEqual(self.quick_bet.selection.bet_summary.total_estimate_returns, self.total_estimate_returns,
                         msg=f'Actual default Est Returns "{self.quick_bet.selection.bet_summary.total_estimate_returns}" '
                             f'does not match expected "{self.total_estimate_returns}"')

    def test_004_verify_greyed_out_overlay_behind_quick_bet(self):
        """
        DESCRIPTION: Verify greyed-out overlay behind Quick Bet
        EXPECTED: * Any options behind Quick Bet can not be selected
        """
        self.assertFalse(self.site.quick_bet_overlay.is_hidden(), msg='Quick Bet overlay is not shown')

    def test_005_verify_add_to_betslip_button(self):
        """
        DESCRIPTION: Verify 'ADD TO BETSLIP' button
        EXPECTED: * Quick Bet is closed after tapping 'Add to Betslip' button
        """
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.site.wait_quick_bet_overlay_to_hide()

    def test_006_verify_login__place_betplace_bet_button(self):
        """
        DESCRIPTION: Verify 'LOGIN & PLACE BET'/'PLACE BET' button
        EXPECTED: * 'LOGIN & PLACE BET'/'PLACE BET' button is disabled by default
        EXPECTED: * 'LOGIN & PLACE BET'/'PLACE BET' button becomes enabled after entering value in 'Stake' field or using Quick Stakes
        """
        self.site.header.bet_slip_counter.click()
        result = self.get_betslip_content()
        self.assertTrue(result, msg='Betslip widget not displayed')
        self.clear_betslip()

        self.add_selection_to_quick_bet()
        quick_bet = self.site.quick_bet_panel
        self.assertFalse(quick_bet.place_bet.is_enabled(expected_result=False), msg='Place Bet button is not disabled')
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        self.assertTrue(quick_bet.place_bet.is_enabled(), msg='Place Bet button is not enabled')

    def test_007_verify_x_icon(self):
        """
        DESCRIPTION: Verify 'X' icon
        EXPECTED: * Quick Bet section is closed after tapping 'X' icon
        EXPECTED: * Selection is NOT added to Betslip
        EXPECTED: After release of BMA-54870 Expected Result will be:
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)

        self.site.header.bet_slip_counter.click()
        result = self.get_betslip_content()
        self.assertTrue(result, msg='Betslip widget not displayed')
        self.clear_betslip()

    def test_008_enter_value_in_stake_field_and_check_ew_checkbox(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'E/W' checkbox is selected
        """
        self.add_selection_to_quick_bet()

        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.each_way_checkbox.input.click()
        quick_bet.amount_form.input.value = self.bet_amount
        self.__class__.amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(quick_bet.amount_form.input.value, self.amount,
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not match '
                             f'expected "{self.amount}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        sleep(1)  # this to save ticked checkbox

    def test_009_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Quick Bet is opened
        EXPECTED: * 'Stake' field is pre-populated with the same value as on step 7
        EXPECTED: * 'E/W' checkbox is selected
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

        quick_bet = self.site.quick_bet_panel.selection.content
        self.assertEqual(quick_bet.amount_form.input.value, str(self.amount),
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not match '
                             f'expected "{self.amount}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')

    def test_010_duplicate_current_tab_and_verify_the_second_tab(self):
        """
        DESCRIPTION: Duplicate current tab and verify the second tab
        EXPECTED: Quick Bet is opened in the second tab
        """
        self.device.open_new_tab()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown in the second tab')
