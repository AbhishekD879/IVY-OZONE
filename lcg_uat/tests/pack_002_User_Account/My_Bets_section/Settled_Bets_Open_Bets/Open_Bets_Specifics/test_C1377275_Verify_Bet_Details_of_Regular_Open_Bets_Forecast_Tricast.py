import re
import pytest
import tests
from time import sleep
from collections import OrderedDict
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.critical
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.forecast_tricast
@pytest.mark.tricast
@pytest.mark.racing
@pytest.mark.bet_history_open_bets
@pytest.mark.pipelines
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1377275_Verify_Bet_Details_of_Regular_Open_Bets_Forecast_Tricast(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C1377275
    NAME: Verify Bet Details of Regular Open Bets Forecast/Tricast
    DESCRIPTION: This test case verifies bet details of Regular Open bets
    PRECONDITIONS: 1. User should be logged in to view their open bets.
    PRECONDITIONS: 2. User should have a few open bets
    PRECONDITIONS: 3. User should have "My Bets" page opened
    """
    keep_browser_open = True
    expected_market_name = 'Win or Each Way'
    price = '1/2'
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast, PROD: Find racing event with Tricast/Forecast
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT,
                                              simple_filter(LEVELS.MARKET,
                                                            ATTRIBUTES.NCAST_TYPE_CODES,
                                                            OPERATORS.INTERSECTS,
                                                            'CT,TC'))

            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)

            outcomes = None
            for event in events:
                market = next((market for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Win or Each Way'), None)
                if market:
                    outcomes = market['market']['children']
                    break

            if not outcomes:
                raise SiteServeException('There are no events with "Win or Each Way" market')

            selection_ids_all = [(i['outcome']['name'], i['outcome']['id']) for i in outcomes
                                 if 'Unnamed' not in i['outcome']['name']]
            self.__class__.selection_ids = OrderedDict(selection_ids_all)

            start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern,
                                                          ss_data=True,
                                                          future_datetime_format=self.event_card_future_time_format_pattern)
            search = re.search('[aA-zZ\'\-\s]+', event['event']['name'])
            type_name = search.group(0).lstrip() if search else ''

            self.__class__.created_event_name = f'{type_name} {start_time_local}'
            self.__class__.eventID = event['event']['id']
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=3,
                                                              forecast_available=True,
                                                              tricast_available=True,
                                                              lp_prices={0: self.price,
                                                                         1: self.price,
                                                                         2: self.price}
                                                              )
            self.__class__.event_start_time = event_params.event_date_time
            self.__class__.selection_ids = event_params.selection_ids
            start_time_local = self.convert_time_to_local(date_time_str=self.event_start_time)
            self.__class__.created_event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
            self.__class__.eventID = event_params.event_id
        self.__class__.selection_names = self.selection_ids.keys()

    def test_001_login_and_place_bet(self):
        """
        DESCRIPTION: Log in user
        DESCRIPTION: Place a bet
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', tricast=True)
        self.site.open_betslip()
        sleep(2)
        self.__class__.betslip_info = self.place_and_validate_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_002_verify_bet_details_of_a_single_horse_racing_bet_each_way(self):
        """
        DESCRIPTION: Verify bet details of a **Forecast/Tricast bet**
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "SINGLE - TRICAST")
        EXPECTED: * Selection names (3 names for Tricast bet, 4 names for Forecast bets)
        EXPECTED: * Market name user has bet on - e.g., "Win or Each Way - Tricast")
        EXPECTED: * Event name and start time (e.g., "1:40 Greyville")
        EXPECTED: * Date when bet was placed
        EXPECTED: * Bet Receipt number
        EXPECTED: * Stake (e.g., £10.00) and Est. Returns ("N/A" if not available)
        """
        self.site.open_my_bets_open_bets()
        bet_name, self.__class__.forecast_tricast = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=f'SINGLE - TRICAST', number_of_bets=1)
        bet_legs = self.forecast_tricast.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: {bet_name}')
        betleg_name, betleg = list(bet_legs.items())[0]
        outcome_names = betleg.outcome_names
        actual_selection_name = f'1st.{outcome_names[0]}\n2nd.{outcome_names[1]}\n3rd.{outcome_names[2]}'
        self.assertEqual(actual_selection_name, self.expected_selection_name,
                         msg=f'Actual bet leg "{actual_selection_name}" does not match expected "{self.expected_selection_name}"')
        self.assertEqual(betleg.market_name, self.expected_market_name,
                         msg=f'Actual bet leg name "{betleg.market_name}" '
                         f'does not match expected "{self.expected_market_name}"')
        self.assertEqual(betleg.odds_value, 'SP')
        self.assertTrue(betleg.event_time, msg='Can not find event time')
        self.assertFalse(betleg.has_link, msg='Event is hyperlinked')
        expected_total_stake_per_line = f'{self.bet_amount:.2f}'
        self.assertEqual(str(self.forecast_tricast.stake.stake_value), expected_total_stake_per_line,
                         msg=f'Stake amount "{self.forecast_tricast.stake.stake_value}" is not equal to expected '
                         f'"{expected_total_stake_per_line}" for bet "{self.forecast_tricast.name}"')

        self.assertEqual(self.forecast_tricast.est_returns.value, self.betslip_info['total_estimate_returns'],
                         msg=f'Estimated returns: "{self.forecast_tricast.est_returns.value,}" '
                         f'does not match with required: "{self.betslip_info["total_estimate_returns"]}"')

    def test_003_repeat_steps_for_betslip_widget_tablet_desktop(self):
        """
        DESCRIPTION: Repeat steps for Betslip widget (Tablet & Desktop)
        """
        pass
