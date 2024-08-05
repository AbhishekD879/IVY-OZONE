import tests
import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from random import choice
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.footer
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.high
@pytest.mark.mobile_only
@vtest
class Test_C16408295_Verify_My_Bets_counter_after_Race_Bet_Placement(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C16408295
    VOL_ID: C58628668
    NAME: Verify My Bets counter after Race Bet Placement
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Race Bet Placement
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Make sure My bets counter config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find/Create events
        DESCRIPTION: Load Oxygen/Roxanne Application and login
        DESCRIPTION: Make sure My bets counter config is turned on in CMS > System configurations
        DESCRIPTION: My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS
        """
        self.check_my_bets_counter_enabled_in_cms()

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         expected_template_market='Win or Each Way',
                                                         all_available_events=True)
            event1 = choice(events)
            events.remove(event1)
            outcomes1 = event1['event'].get('children')[0]['market'].get('children')
            if outcomes1 is None:
                raise SiteServeException('No outcomes available')
            all_selection_ids1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes1
                                  if 'Unnamed' not in i['outcome']['name']}
            self.__class__.selection_ids_single = list(all_selection_ids1.values())[:1]
            self._logger.debug(f'*** Found 1st Horse Racing event with selection ids:"{self.selection_ids_single}"')

            event2 = choice(events)
            outcomes2 = event2['event'].get('children')[0]['market'].get('children')
            if outcomes1 is None:
                raise SiteServeException('No outcomes available')
            all_selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2
                                  if 'Unnamed' not in i['outcome']['name']}
            self.__class__.selection_ids_multiple = [list(all_selection_ids1.values())[:1][0],
                                                     list(all_selection_ids2.values())[:1][0]]
            self._logger.debug(f'*** Found 2nd Horse Racing event with selection ids:"{self.selection_ids_multiple}"')

            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT,TC'))
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        expected_template_market='Win or Each Way',
                                                        additional_filters=additional_filter)[0]
            outcomes = event['event'].get('children')[0]['market'].get('children')
            if outcomes is None:
                raise SiteServeException('No outcomes available')
            all_selection_ids3 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes[:3]
                                  if 'Unnamed' not in i['outcome']['name']}
            self.__class__.selection_ids_forecast_tricast = list(all_selection_ids3.values())
            self._logger.info(f'*** Found Forecast/Tricast Horse Racing event with selection ids: "{self.selection_ids_forecast_tricast}"')
        else:
            event1 = self.ob_config.add_UK_racing_event(number_of_runners=1, is_tomorrow=True)
            self.__class__.selection_ids_single = list(event1.selection_ids.values())
            self._logger.info(f'*** Created 1st Horse Racing event with selection ids:"{self.selection_ids_single}"')

            event2 = self.ob_config.add_UK_racing_event(number_of_runners=1, is_tomorrow=True)
            self.__class__.selection_ids_multiple = [list(event1.selection_ids.values())[0],
                                                     list(event2.selection_ids.values())[0]]
            self._logger.info(f'*** Created 2nd Horse Racing event with selection ids:"{self.selection_ids_multiple}"')

            event = self.ob_config.add_UK_racing_event(number_of_runners=3,
                                                       forecast_available=True,
                                                       tricast_available=True,
                                                       is_tomorrow=True)
            self.__class__.selection_ids_forecast_tricast = list(event.selection_ids.values())
            self._logger.info(f'*** Created Forecast/Tricast Horse Racing event with selection ids:"{self.selection_ids_forecast_tricast}"')

        self.site.login(username=tests.settings.betplacement_user)
        if '+' in self.get_my_bets_counter_value_from_footer():
            self.__class__.initial_my_bets_counter = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        else:
            self.__class__.initial_my_bets_counter = int(self.get_my_bets_counter_value_from_footer())
        self.__class__.expected_counter = self.initial_my_bets_counter

    def test_001_add_race_selection_to_quickbet_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add race selection ( e.g. Horse racing) to Quickbet/Betslip and place bet
        EXPECTED: Bet is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_single)
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_002_close_quickbet_betslip_verify_my_bets_counter_on_the_footer_panel(self):
        """
        DESCRIPTION: * Close Quickbet/Betslip
        DESCRIPTION: * Verify 'My Bets' counter on the Footer panel
        EXPECTED: My bets counter icon is increased by one
        """
        self.site.close_betreceipt()
        if '+' in self.get_my_bets_counter_value_from_footer():
            actual_counter = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        else:
            self.__class__.expected_counter += 1
            actual_counter = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(actual_counter, self.expected_counter,
                         msg=f'Actual My Bets counter: "{actual_counter}" '
                             f'is not as expected: "{self.expected_counter}"')

    def test_003_repeat_steps_1_2_for_multiples(self):
        """
        DESCRIPTION: Repeat steps #1-2 for multiples
        EXPECTED: Results are the same:
        EXPECTED: My bets counter icon is increased by one
        """
        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=self.selection_ids_multiple)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.test_002_close_quickbet_betslip_verify_my_bets_counter_on_the_footer_panel()

    def test_004_repeat_steps_1_2_for_forecast_tricast(self):
        """
        DESCRIPTION: Repeat steps #1-2 for forecast/tricast
        EXPECTED: Results are the same:
        EXPECTED: My bets counter icon is increased by one
        """
        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=self.selection_ids_forecast_tricast)
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.test_002_close_quickbet_betslip_verify_my_bets_counter_on_the_footer_panel()
