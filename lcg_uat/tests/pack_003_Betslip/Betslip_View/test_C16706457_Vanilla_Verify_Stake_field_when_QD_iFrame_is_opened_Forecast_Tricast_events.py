import tests
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.reg156_fix
@vtest
class Test_C16706457_Vanilla_Verify_Stake_field_when_QD_iFrame_is_opened_Forecast_Tricast_events(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C16706457
    NAME: [Vanilla] Verify 'Stake' field when QD iFrame is opened ( Forecast/Tricast events)
    DESCRIPTION: This test case verifies that stake becomes disabled at once QD iFrame opens (Tote events)
    PRECONDITIONS: Login into Application
    """
    keep_browser_open = True
    additional_amount = 5.0
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def click_on_deposit(self):
        deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{deposit_button.name}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is not displayed')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast, PROD: Find racing event with Tricast/Forecast
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.horseracing_config.category_id
            class_ids = self.get_class_ids_for_category(category_id=category_id)
            events_filter = self.ss_query_builder \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'SF,CF,RF,'))) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT,TC,'))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))
            ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            events = [event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')]
            if not events:
                raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')
            event = choice(events)
            start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern,
                                                          future_datetime_format=self.my_bets_event_future_time_format_pattern,
                                                          ss_data=True)
            event_name = f'{event["event"]["name"]} {start_time_local}'
            self.__class__.event_id = event['event']['id']
            self._logger.info(
                f'*** Found Horse Racing Forecast/Tricast event "{event_name}" with id "{self.event_id}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=5,
                                                              forecast_available=True,
                                                              tricast_available=True)
            event_start_time = event_params.event_date_time
            start_time_local = self.convert_time_to_local(date_time_str=event_start_time)
            event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
            self.__class__.event_id = event_params.event_id
            self._logger.info(
                f'*** Created Horse Racing Forecast/Tricast event "{event_name}" with id "{self.event_id}"')
        self.site.login(tests.settings.quick_deposit_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_navigate_to_hrgreyhounds_pagechoose_event_with_forecasttricast_tab_available(self):
        """
        DESCRIPTION: Navigate to 'HR/Greyhounds' page
        DESCRIPTION: Choose event with Forecast/Tricast Tab available
        EXPECTED: Event with available Forecast/Tricast Tab is opened
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        tabs = market_tabs.items_as_ordered_dict
        self.assertTrue(tabs, msg='No market tabs found')
        self.assertIn(vec.racing.RACING_EDP_FORECAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_FORECAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')
        self.assertIn(vec.racing.RACING_EDP_TRICAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_TRICAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')

    def test_002_select_two_selections_in_forecasttricast_tab_and_tap_add_to_bet_slip_button(self):
        """
        DESCRIPTION: Select two Selections in Forecast/Tricast Tab and tap "Add to bet slip" button.
        EXPECTED: Sections are added to the Betslip (No Quick Bet)
        """
        self.place_forecast_tricast_bet_from_event_details_page(forecast=True)

    def test_003_navigate_to_betslip_viewenter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Navigate to Betslip view
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(singles_section, msg='No stakes found')
        self.__class__.stake_value = self.user_balance + self.additional_amount
        self.stake.amount_form.input.click()
        self.__class__.keyboard = self.get_betslip_content().keyboard
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.keyboard.enter_amount_using_keyboard(value=self.stake_value)
        self.click_on_deposit()

    def test_004_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        # Covered in step 3

    def test_005_tap_on_stake_textbox(self):
        """
        DESCRIPTION: Tap on 'Stake' textbox
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: 'Stake' textbox is editable
        """
        self.stake.amount_form.input.click()
        self.assertFalse(self.get_betslip_content().has_deposit_form(timeout=10), msg='"Quick Deposit" section is displayed')
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
        default_stake_value = self.stake.amount_form.input.value
        self.assertEqual(self.bet_amount, float(default_stake_value), msg='stake value is not editable')
        self.clear_input_using_keyboard()
        self.keyboard.enter_amount_using_keyboard(value=self.stake_value)

    def test_006_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        self.click_on_deposit()

    def test_007_tap_on_any_space_inside_betslip_except_stake_textbox(self):
        """
        DESCRIPTION: Tap on any space inside Betslip except 'Stake' textbox
        EXPECTED: 'Quick Deposit' iFrame overlay is still displayed, nothing is changed
        """
        self.get_betslip_content().remove_all_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is not displayed')
