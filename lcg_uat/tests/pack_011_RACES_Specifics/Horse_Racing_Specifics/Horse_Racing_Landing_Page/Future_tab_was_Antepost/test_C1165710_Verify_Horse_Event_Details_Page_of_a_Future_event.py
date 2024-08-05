from datetime import datetime
from fractions import Fraction

import pytest
from crlat_ob_client.utils.date_time import strftime_add_day_suffix
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - liveserv updates are needed
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.racing_antepost
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.bet_placement
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C1165710_Verify_Horse_Event_Details_Page_of_an_Antepost_event(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C1165710
    NAME: Verify Horse Event Details Page of a Future event
    DESCRIPTION: This test case verifies Horse Racing 'Future' event details page
    PRECONDITIONS: 1) In order to create HR Future event use TI tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: a) 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: - 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    PRECONDITIONS: b) 'Antepost' check box should be checked on market level (Market Template= 'Outright' with name 'Ante-post')
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: - If flags 'Flat', 'National Hunt', 'International'  are not checked on event level, events are not displayed on the landing page
    PRECONDITIONS: - If flag 'Antepost' is not checked on market level, new designs do not apply on HR EDP
    PRECONDITIONS: 2) To observe LiveServe changes make sure:
    PRECONDITIONS: - LiveServ updates is checked on 'Class' and 'Type' levels in TI
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: 3) For checking info regarding event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    """
    keep_browser_open = True
    lp = {0: '1/10',
          1: '1/2',
          2: '1/20'}
    outcomes = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Antepost event
        DESCRIPTION: Login
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=3, is_flat=True, ew_terms=self.ew_terms,
                                                   cashout=True, lp_prices=self.lp,
                                                   start_time=self.get_date_time_formatted_string(days=2)
                                                   )
        self.ob_config.add_UK_racing_event(number_of_runners=3, is_national_hunt=True, ew_terms=self.ew_terms,
                                           cashout=True, lp_prices=self.lp,
                                           start_time=self.get_date_time_formatted_string(days=2)
                                           )
        self.ob_config.add_UK_racing_event(number_of_runners=3, is_international=True, ew_terms=self.ew_terms,
                                           cashout=True, lp_prices=self.lp,
                                           start_time=self.get_date_time_formatted_string(days=2)
                                           )
        self.__class__.eventID = event.event_id
        self.__class__.name_pattern = self.horseracing_autotest_uk_name_pattern.upper() if self.device_type == 'mobile' \
            else self.horseracing_autotest_uk_name_pattern

        pattern = '%d-%m-%Y | %H:%M ' if self.brand != 'ladbrokes' else '%Y-%m-%d %H:%M:%S'
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern='%Y-%m-%d %H:%M:%S',
                                                               date_time_str=event.event_date_time,
                                                               future_datetime_format=pattern
                                                               )  # need convert to local time (BMA-46066)
        event_date = datetime.strptime(event_time_resp_converted, pattern).strftime('%d-%m-%Y | %H:%M ')
        if self.brand != 'ladbrokes':
            self.__class__.event_name = event_time_resp_converted + self.name_pattern
        else:
            self.__class__.event_name = event_date + self.horseracing_autotest_uk_name_pattern if self.device_type == 'desktop' \
                else strftime_add_day_suffix(datetime_string=event_time_resp_converted,
                                             format_pattern='%A %-d %B %Y - %H:%M')
        self.__class__.marketID = event.market_id
        self.__class__.selection_ids = event.selection_ids
        self.site.login()

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: Horse Racing landing page is opened
        EXPECTED: 'Featured' tab is opened by default
        EXPECTED: 'Future' tab is available and located right after 'Featured' tab
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        tabs_menu = self.site.horse_racing.tabs_menu
        current_tab_name = tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')
        tabs = tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tabs found on Horse racing page')
        tab_names = list(tabs.keys())
        self.assertIn(vec.racing.RACING_FUTURE_TAB_NAME, tab_names,
                      msg=f'Tab {vec.racing.RACING_FUTURE_TAB_NAME} should be displayed on Horse Racing page. Current list of tabs is {tab_names}')

        if self.brand != 'ladbrokes':
            self.assertEqual(tab_names.index(vec.racing.RACING_DEFAULT_TAB_NAME) + 1, tab_names.index(vec.racing.RACING_FUTURE_TAB_NAME),
                             msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not located right after "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

    def test_002_tap_future_tab(self):
        """
        DESCRIPTION: Tap on 'Future' tab.
        EXPECTED: 'Future' tab is opened
        EXPECTED: Switchers are displayed: 'Flat Races', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions)
        """
        tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_FUTURE_TAB_NAME)
        self.assertTrue(tab, msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not selected after click')
        switchers = self.site.horse_racing.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(switchers, msg='No switchers present on page')
        self.assertListEqual(list(switchers.keys()), vec.racing.RACING_ANTEPOST_SWITCHERS,
                             msg=f'Incorrect switchers are displayed in Future tab. '
                             f'\nActual: {list(switchers.keys())}.\nExpected: {vec.racing.RACING_ANTEPOST_SWITCHERS}')

    def test_003_tap_event(self):
        """
        DESCRIPTION: Tap on one of the available events
        EXPECTED: Horse Racing Future event details page is opened
        EXPECTED: isAntepost="true" attribute is received in response on market level
        EXPECTED: 'Horse Racing' header with 'Back' icon (navigates back to Future landing page, where first available switcher is opened) and 'Bet Filter' link
        EXPECTED: 'Meetings' subheader: 'Horse Racing / [Event Name]' breadcrumb + 'Down' arrow
        EXPECTED: Time switcher
        EXPECTED: RaceCard area:
        EXPECTED: ANTEPOST
        EXPECTED: Event 'name' (taken from event 'name' from SS response)
        EXPECTED: Each Way: <nom>/<den> Odds - Places e.g. 1, 2, 3 (if available)
        EXPECTED: List of selections with fractional Odds (taken from 'Antepost' market only, see Preconditions)
        EXPECTED: Selections are ordered by prices (from lowest to highest), if prices are the same then by selection name in ascending order
        EXPECTED: On tablet/desktop:
        EXPECTED: - ANTEPOST Event 'name' (located on separate area below the time switcher)
        EXPECTED: - EACH WAY: <nom>/<den> ODDS - PlACES e.g. 1, 2, 3, CLASS # (if available) (located in the selections area)
        EXPECTED: On tablet:
        EXPECTED: - Selections are displayed in 2 columns view
        EXPECTED: On desktop:
        EXPECTED: - Selections are displayed in 3 columns view
        """
        type_sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(type_sections, msg='No type sections are present')
        section = type_sections.get(self.horseracing_autotest_uk_name_pattern.upper())
        self.assertTrue(section,
                        msg=f'Cannot found "{self.horseracing_autotest_uk_name_pattern.upper()}" '
                        f'section in "{type_sections.keys()}"')
        section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No event found for "{self.horseracing_autotest_uk_name_pattern.upper()}" section')

        self.assertIn(self.event_name, events.keys(), msg=f'Event "{self.event_name}"" is not displayed among "{events.keys()}"')
        events[self.event_name].click()
        self.site.wait_content_state(state_name='RacingEventDetails')

        query_params = self.ss_query_builder.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.ID, OPERATORS.EQUALS, self.eventID))
        resp = self.ss_req.ss_event_to_outcome_for_class(query_builder=query_params)
        self.assertEqual(resp[0]['event']['children'][0]['market']['isAntepost'], 'true',
                         msg='Failed to receive "true" on market level for "isAntepost" attribute from SS response')

        edp = self.site.racing_event_details
        if self.brand != 'ladbrokes':
            self.assertTrue(edp.is_back_button_displayed(), msg='Back button was not found')
        else:
            self.assertTrue(self.site.has_back_button, msg='Back button was not found')
        self.assertTrue(edp.has_meeting_selector(), msg='Meeting selector was not found')
        self.assertTrue(edp.has_bet_filter_link, msg='Bet filter link was not found')
        self.assertTrue(edp.tab_content.has_event_off_times_list(), msg='Event off times list was not found')

        sections = edp.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        self.assertEqual(section_name, 'Antepost',
                         msg=f'Incorrect title on RaceCard area.\nExpected: "Antepost"\nActual: "{section_name}')
        event_title = section.event_title if self.device_type != 'desktop' else edp.event_title
        self.assertEqual(event_title, self.horseracing_autotest_uk_name_pattern,
                         msg=f'Incorrect event name is displayed.\nActual: "{event_title}'
                         f'\nExpected: "{self.horseracing_autotest_uk_name_pattern}')
        self.check_each_way_terms_format(each_way_terms=section.section_header.each_way_terms, future_tab=True)

        self.__class__.outcomes = section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes was found')
        sorted_outcomes = [outcome.name for outcome in
                           sorted(self.outcomes.values(), key=lambda x: Fraction(x.bet_button.outcome_price_text))]
        self.assertListEqual(list(self.outcomes.keys()), sorted_outcomes,
                             msg=f'Incorrect order of selections: '
                             f'Actual: {list(self.outcomes.keys())} \nExpected: {sorted_outcomes}')

    def test_004_in_ti_change_price_for_one_of_the_selections_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections > Navigate to application and observe changes
        EXPECTED: Corresponding 'Price/Odds' buttons immediately display new prices
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        selection_name, selection = list(self.outcomes.items())[0]
        expected_old_price = selection.bet_button.outcome_price_text
        expected_new_price = '7/1'
        self.ob_config.change_price(selection_id=self.selection_ids[selection_name], price=expected_new_price)

        if self.brand != 'ladbrokes':
            result = wait_for_result(lambda: selection.previous_price,
                                     name='Previous price to appear',
                                     timeout=40)
            self.assertTrue(result, msg='Price update is not shown on page')
            old_price = selection.previous_price

            self.assertEqual(old_price, expected_old_price,
                             msg=f'Old price is "{old_price}" not as expected "{expected_old_price}"')
        new_price = selection.bet_button.outcome_price_text

        result = wait_for_result(lambda: selection.bet_button.outcome_price_text == new_price,
                                 name='Price to change',
                                 timeout=3)
        self.assertTrue(result,
                        msg=f'New price is "{selection.bet_button.outcome_price_text}" not as expected "{expected_new_price}"')

    def test_005_in_ti_suspend_selection_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend market/one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: If market is suspended: All Price/Odds buttons are displayed immediately as greyed out and become disabled for selected market but still displaying the prices
        EXPECTED: If some selections are suspended: Price/Odds button of changed outcome are displayed immediately as greyed out and become disabled on Event Details page. The rest outcomes and market tabs are not changed
        """
        selection_name, selection = list(self.outcomes.items())[0]
        self.ob_config.change_selection_state(selection_id=self.selection_ids[selection_name], displayed=True)
        self.assertFalse(selection.bet_button.is_enabled(timeout=40, expected_result=False),
                         msg=f'"{selection_name}" button is not disabled')

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)
        for selection_name, selection in list(self.outcomes.items()):
            self.assertFalse(selection.bet_button.is_enabled(timeout=5, expected_result=False),
                             msg=f'"{selection_name}" button is not disabled')

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=True, displayed=True)
        for selection_name, selection in list(self.outcomes.items())[1:]:
            self.assertTrue(selection.bet_button.is_enabled(timeout=5), msg=f'"{selection_name}" button is not disabled')

    def test_006_add_selections_with_lp_sp_prices_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) with LP/SP prices to the Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        selection_name, selection = list(self.outcomes.items())[1]
        selection.bet_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick bet is not opened')
            self.site.add_first_selection_from_quick_bet_to_betslip()

    def test_007_enter_stake_for_a_single_bet_tap_place_bet(self):
        """
        DESCRIPTION: Enter 'Stake' for a Single/Multiple/Forecast/Tricast bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet' in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: Bet is successfully placed
        EXPECTED: Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: Balance is decreased accordingly
        """
        balance = self.site.header.user_balance

        self.site.header.bet_slip_counter.click()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        self.verify_user_balance(page='betreceipt', expected_user_balance=balance - self.bet_amount)

    def test_008_change_price_format_and_repeat_steps_3_7(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and Repeat steps 3 - 7
        EXPECTED: All Prices/Odds are displayed in Decimal format
        """
        self.site.bet_receipt.footer.click_done()
        self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.test_001_navigate_to_horse_racing_landing_page()
        self.test_002_tap_future_tab()

        type_sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(type_sections, msg='No type sections are present')
        section = type_sections.get(self.horseracing_autotest_uk_name_pattern.upper())

        self.assertTrue(section, msg=f'Cannot found "{self.horseracing_autotest_uk_name_pattern.upper()}" section')
        section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No event found for "{self.horseracing_autotest_uk_name_pattern.upper()}" section')

        self.assertIn(self.event_name, events.keys(), msg=f'Event "{self.event_name}" is not displayed among "{events.keys()}"')
        events[self.event_name].click()
        self.site.wait_content_state(state_name='RacingEventDetails')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        self.assertEqual(section_name, 'Antepost',
                         msg=f'Incorrect title on RaceCard area.\nExpeced: "Antepost"\nActual: "{section_name}')

        outcomes = section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes was found')

        for _, selection in list(outcomes.items()):
            self.assertRegexpMatches(selection.bet_button.outcome_price_text, self.decimal_pattern,
                                     msg=f'Selection odds value "{selection.bet_button.outcome_price_text}" not match '
                                     f'decimal pattern: "{self.decimal_pattern}"')

        sorted_outcomes = [outcome.name for outcome in
                           sorted(outcomes.values(), key=lambda x: x.bet_button.outcome_price_text)]
        self.assertListEqual(list(outcomes.keys()), sorted_outcomes,
                             msg=f'Incorrect order of selections: '
                             f'Actual: {list(self.outcomes.keys())} \nExpected: {sorted_outcomes}')
