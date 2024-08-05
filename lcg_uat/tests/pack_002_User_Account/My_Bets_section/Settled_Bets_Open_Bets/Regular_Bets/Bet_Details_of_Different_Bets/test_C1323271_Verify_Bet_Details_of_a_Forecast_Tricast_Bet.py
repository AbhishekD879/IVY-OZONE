from datetime import datetime

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # We cannot result events on hl/prod
# @pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.forecast_tricast
@pytest.mark.bet_history_open_bets
@pytest.mark.my_bets
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C1323271_Verify_Bet_Details_of_a_Forecast_Tricast_Bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C1323271
    NAME: Verify Bet Details of a Forecast/Tricast Bet
    DESCRIPTION: This test case verifies bet details of a Forecast/Tricast bet
    PRECONDITIONS: 1. User should be logged in to view their Settled Bets.
    PRECONDITIONS: 2. User should have few open/won/settled/void/cashed out Forecast/Tricast bets
    """
    keep_browser_open = True
    bet_amount = 0.5

    def verify_bet_details_of_a_forecast_tricast_bet(self, bet_name, tab=vec.bet_history.OPEN_BETS_TAB_NAME):
        """
        This method is used to verify bet details of a forecast / tricast bet
        :param bet_name: name (type) of the bet (e.g., "SINGLE - TRICAST")
        :param tab: tab on which perform verifications
        """
        event_name = self.event_name if tab == vec.bet_history.OPEN_BETS_TAB_NAME \
            else f'{self.event_off_time} {self.greyhound_autotest_name_pattern}'
        bet_legs = self.forecast_tricast.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: {bet_name}')
        betleg_name, betleg = list(bet_legs.items())[0]
        outcome_names = betleg.outcome_names
        actual_selection_name = f'1st.{outcome_names[0]}\n2nd.{outcome_names[1]}'
        self.assertEqual(actual_selection_name, self.expected_selection_name,
                         msg=f'Actual names "{actual_selection_name} '
                             f'does not match expected "{self.expected_selection_name}"')
        expected_market_name = self.ob_config.horseracing_config.default_market_name.replace('|', '')
        self.assertEqual(betleg.market_name, expected_market_name,
                         msg=f'Actual market name: {betleg.market_name} '
                             f'is not as expected: {expected_market_name}')
        actual_event_name = f'{betleg.event_name} {betleg.event_time}' if tab == vec.bet_history.OPEN_BETS_TAB_NAME \
            else f'{betleg.event_name}'
        self.assertEqual(actual_event_name, event_name,
                         msg=f'Actual event name: {actual_event_name} is not as expected: {event_name}')

        if tab == vec.bet_history.OPEN_BETS_TAB_NAME:
            self.assertTrue(betleg.event_time, msg='Can not find event time')
        else:
            self._logger.warning(f'*** There is no event time on "{tab}" tab')
            bet_receipt_info = self.forecast_tricast.bet_receipt_info
            placement_date = bet_receipt_info.date.name
            expected_date = datetime.strptime(placement_date, self.time_format_pattern).strftime(
                self.time_format_pattern)
            self.assertEquals(placement_date, expected_date,
                              msg=f'Actual date format: {placement_date} is not as expected: {expected_date}')
            self.assertTrue(bet_receipt_info.bet_receipt.value,
                            msg=f'Open Bet section: {self.forecast_tricast.name} bet receipt ID not found')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast, PROD: Find racing event with Tricast/Forecast
        DESCRIPTION: Log In and Place a Bet
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=3, forecast_available=True,
                                                                    tricast_available=True)
        self.__class__.event_start_time = event_params.event_date_time
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.selection_names = self.selection_ids.keys()
        self.__class__.event_off_time = event_params.event_off_time
        start_time_local = self.convert_time_to_local(date_time_str=self.event_start_time,
                                                      future_datetime_format=self.event_card_future_time_format_pattern)
        self.__class__.event_name = f'{self.event_off_time} {self.greyhound_autotest_name_pattern} {start_time_local}'
        self.__class__.event_id = event_params.event_id
        self.__class__.market_id = self.ob_config.market_ids[self.event_id]

        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        self.__class__.expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(
            sport_name='greyhound-racing', forecast=True)

        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_open_bets_tab_and_verify_bet_details_for_placed_forecast_tricast_bet(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        DESCRIPTION: Verify bet details for placed Forecast/Tricast bet
        EXPECTED: 'Open Bets' tab is opened
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "SINGLE - FORECAST")
        EXPECTED: * Selection names listed in a column one under another
        EXPECTED: * Market name user has bet on (e.g., "Win or Each Way")
        EXPECTED: * Event name and start time (e.g., "Greyville 3:00 PM")
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        EXPECTED: * 'Bet Receipt' label and its ID (e.g., O/15242822/0000017) are shown
        EXPECTED: * Stake (e.g., £10.00) and Est. Returns ("N/A" if not available)
        """
        self.site.open_my_bets_open_bets()
        bet_name, self.__class__.forecast_tricast = \
            self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.SINGLE_FORECAST_MY_BETS_NAME,
                                                                    event_names=self.event_name,
                                                                    number_of_bets=1)
        self.verify_bet_details_of_a_forecast_tricast_bet(bet_name=bet_name)

    def test_002_navigate_to_settled_bets_tab_and_verify_bet_details_for_settled_forecast_tricast_bet(self):
        """
        DESCRIPTION: Navigate to 'SETTLED BETS' tab
        DESCRIPTION: Verify bet details for 'Open' Forecast/Tricast bet in Settled Bets
        EXPECTED: 'SETTLED BETS' tab is opened
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "SINGLE - FORECAST")
        EXPECTED: * Selection names listed in a column one under another
        EXPECTED: * Market name user has bet on (e.g., "Win or Each Way")
        EXPECTED: * Event name and start time (e.g., "Greyville 3:00 PM")
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        EXPECTED: * 'Bet Receipt' label and its ID (e.g., O/15242822/0000017) are shown
        EXPECTED: * Stake (e.g., £10.00) and Est. Returns ("N/A" if not available)
        """
        self.result_event(selection_ids=list(self.selection_ids.values()), market_id=self.market_id,
                          event_id=self.event_id)

        self.site.open_my_bets_settled_bets()
        bet_name, self.__class__.forecast_tricast = \
            self.site.bet_history.tab_content.accordions_list.get_bet(
                bet_type='SINGLE - FORECAST',
                event_names=f'{self.greyhound_autotest_name_pattern}',
                number_of_bets=1
            )
        self.verify_bet_details_of_a_forecast_tricast_bet(bet_name=bet_name, tab=vec.bet_history.SETTLED_BETS_TAB_NAME)
