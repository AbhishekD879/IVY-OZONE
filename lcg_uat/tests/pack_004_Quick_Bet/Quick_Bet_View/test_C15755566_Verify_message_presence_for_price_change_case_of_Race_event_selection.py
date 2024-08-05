import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # involves event creation and price change through OB
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C15755566_Verify_message_presence_for_price_change_case_of_Race_event_selection(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C15755566
    NAME: Verify message presence for price change case of Race event selection
    DESCRIPTION: This test case verifies presence of a warning message about price change within QuickBet while interaction with fields shown before bet placement
    PRECONDITIONS: To get SiteServer info about event use the following URL: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Race> Event should be LiveServed:
    PRECONDITIONS: Event should not be 'Live' ('isStarted' - absent)
    PRECONDITIONS: Event, Market, Outcome should be Active
    PRECONDITIONS: Price format should be Fractional
    PRECONDITIONS: Link to backoffice tool for price changing: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Price updates are received in Quick Bet microservice:
    PRECONDITIONS: Development tool> Network> WS> remotebetslip/?EIO=3&transport=websocket
    """
    keep_browser_open = True
    prices = {0: '1/5'}
    increased_price = '1/4'
    decreased_price = '1/8'

    def test_000_preconditions(self):
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                          time_to_start=20, sp=True, lp=True,
                                                          lp_prices=self.prices)
        self.__class__.event_id = event_params.event_id
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.meeting_name = self.horseracing_autotest_uk_name_pattern if self.brand == 'ladbrokes' \
            else self.horseracing_autotest_uk_name_pattern.upper()

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Home')

    def test_002_tap_race_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports ribbon
        EXPECTED: <Race> Landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing', timeout=20)

    def test_003_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: Events for current day are displayed
        """
        # Covered in step# 4

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_005_make_single_selection_where_price_has_both_lp_and_sp_values(self):
        """
        DESCRIPTION: Make single selection where price has both LP and SP values
        EXPECTED: * Quick Bet is opened with selection added
        EXPECTED: * LP Price is shown in drop down
        """
        event_name = self.site.racing_event_details.tab_content.race_details.event_title
        self._logger.debug(f'*** Race event name: "{event_name}"')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No one section was found')
        first_section_name, first_section = list(sections.items())[0]
        outcomes = first_section.items_as_ordered_dict
        self.assertTrue(len(outcomes) == 1, msg=f'Found "{len(outcomes)}" racing outcomes but expected 1')
        self._logger.debug(f'*** Outcomes {list(outcomes.keys())}')
        outcome_name, outcome = list(outcomes.items())[0]
        self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Racing outcome "{outcome_name}" is disabled')
        outcome.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
        self.device.driver.implicitly_wait(1)
        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content

    def test_006_increasedecrease_price_for_the_selection_in_backoffice_tool(self, changed_price=increased_price):
        """
        DESCRIPTION: Increase/Decrease price for the selection in Backoffice tool
        EXPECTED:
        """
        self.__class__.old_price = self.site.quick_bet_panel.selection.content.odds_value
        self.ob_config.change_price(selection_id=self.selection_id, price=changed_price)

    def test_007_check_price_displaying_in_quick_bet(self, changed_price=increased_price):
        """
        DESCRIPTION: Check price displaying in Quick Bet
        EXPECTED: Old Odds(Price) are instantly changed to New Odds(Price)
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.selection_id}" is not received')

        quick_bet = self.site.quick_bet_panel.selection.content
        result = wait_for_result(lambda: changed_price in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=5)
        self.assertTrue(result,
                        msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{changed_price}"')

        odds = self.quick_bet.odds
        self.assertEqual(odds, changed_price,
                         msg=f'Actual price "{odds}" is not the same as expected "{changed_price}"')

        odds_dropdown = self.site.quick_bet_panel.selection.content.odds_dropdown
        self.assertTrue(odds_dropdown, msg='No odds dropdown found in Quick Bet')
        odds_dropdown.click()
        self.assertTrue(odds_dropdown.is_expanded(), msg='Odds dropdown is not expanded')
        values = odds_dropdown.items_as_ordered_dict
        for odd in [changed_price, 'SP']:
            self.assertIn(odd, values.keys(), msg=f'Odd value "{odd}" is not selectable option in "{values.keys()}"')
        odds_dropdown.click()
        self.assertFalse(odds_dropdown.is_expanded(expected_result=False), msg='Odds dropdown is not expanded')

    def test_008_click_into_dropdown(self, changed_price=increased_price):
        """
        DESCRIPTION: Click into dropdown
        EXPECTED: * Both updated Odds value and 'SP' value are shown as selectable options
        EXPECTED: * Warning message remains shown below 'QUICK BET' header
        """
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        self.device.driver.implicitly_wait(0)  # VOL-1107
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=self.old_price, new=changed_price)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.site.quick_bet_panel.close()
        self.site.open_betslip()
        self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0

    def test_009_repeat_steps_2_8_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-8 for Logged In User
        EXPECTED: As per steps
        """
        self.test_000_preconditions()
        self.site.login(username=tests.settings.betplacement_user)
        self.test_002_tap_race_icon_from_the_sports_ribbon()
        self.test_003_go_to_the_today_tab()
        self.test_004_go_to_the_event_details_page()
        self.test_005_make_single_selection_where_price_has_both_lp_and_sp_values()
        self.test_006_increasedecrease_price_for_the_selection_in_backoffice_tool(changed_price=self.decreased_price)
        self.test_007_check_price_displaying_in_quick_bet(changed_price=self.decreased_price)
        self.test_008_click_into_dropdown(changed_price=self.decreased_price)
